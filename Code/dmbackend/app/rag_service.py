from app.ollama_service import generate_completion
from app.retrieval_service import search_document

from app.config_loader import (
    load_model_config,
    load_rag_prompt,
)


def build_evidence_context(sources):
    """Format passages and build matching source citation objects."""
    blocks = []
    citations = []

    for source in sources:
        text = (source.get("text") or "").strip()

        if not text:
            continue

        # Use the citation number of the actual included passage.
        source_id = len(citations) + 1
        label = f"[{source_id}]"

        filename = source.get("filename") or "Unknown document"
        page_number = source.get("page_number")
        section_title = source.get("section_title")

        location = f"{filename}, page {page_number}"

        if section_title:
            location += f", section: {section_title}"

        blocks.append(
            f"SOURCE {label}\n"
            f"Location: {location}\n"
            f"Passage:\n{text}"
        )

        citations.append({
            "source_id": source_id,
            "label": label,
            "document_id": source.get("document_id"),
            "filename": filename,
            "page_number": page_number,
            "section_title": section_title,
            "chunk_id": source.get("chunk_id"),
            "similarity_score": source.get("similarity_score"),
            "rerank_score": source.get("rerank_score"),
            "excerpt": text[:500],
        })

    return "\n\n---\n\n".join(blocks), citations


def answer_question(
    document_id,
    user_id,
    question,
    top_k=None,
    chunking_strategy=None,
    embedding_model=None,
):
    """Retrieve evidence, generate an answer, and return source metadata."""

    if not isinstance(question, str) or not question.strip():
        raise ValueError("Question must not be empty.")

    question = question.strip()

    # Load the central configuration.
    config = load_model_config()

    embedding_config = config.get("embeddings", {})
    retrieval_config = config.get("retrieval", {})

    # Resolve defaults without overriding explicitly supplied arguments.
    if embedding_model is None:
        embedding_model = embedding_config.get("default", "minilm")

    if top_k is None:
        top_k = retrieval_config.get("default_top_k", 5)

    if chunking_strategy is None:
        chunking_strategy = retrieval_config.get(
            "default_chunking_strategy",
            "fixed",
        )

    if not isinstance(top_k, int) or isinstance(top_k, bool) or top_k < 1:
        raise ValueError("top_k must be a positive integer.")

    # Load the RAG system prompt from the external text file.
    system_prompt = load_rag_prompt()

    if not system_prompt.strip():
        raise ValueError("The RAG system prompt must not be empty.")

    # Retrieve relevant passages using the selected settings.
    sources = search_document(
        document_id=document_id,
        user_id=user_id,
        question=question,
        top_k=top_k,
        chunking_strategy=chunking_strategy,
        embedding_model=embedding_model,
    )

    if not sources:
        return {
            "answer": (
                "I couldn't find sufficiently relevant passages in "
                "this document to answer your question. Try rephrasing "
                "the question or verify that the document is indexed."
            ),
            "citations": [],
            "model": None,
            "retrieved_count": 0,
            "chunking_strategy": chunking_strategy,
            "embedding_model": embedding_model,
        }

    context, citations = build_evidence_context(sources)

    if not context:
        return {
            "answer": (
                "Relevant passages were retrieved, but they did not "
                "contain usable text to answer the question."
            ),
            "citations": [],
            "model": None,
            "retrieved_count": 0,
            "chunking_strategy": chunking_strategy,
            "embedding_model": embedding_model,
        }

    prompt = f"""
QUESTION:
{question}

RETRIEVED DOCUMENT EVIDENCE:
The following passages were retrieved from the selected PDF.
Each passage has a source label and location.

<document_evidence>
{context}
</document_evidence>

Answer the question directly using the evidence above.
Use citations such as [1] and [2] for factual claims.
Do not invent citation labels.
If the evidence does not answer the question adequately,
state what information is missing.
"""

    generation = generate_completion(
        system_prompt=system_prompt,
        user_prompt=prompt,
    )

    return {
        "answer": generation["answer"],
        "citations": citations,
        "model": generation["model"],
        "retrieved_count": len(sources),
        "chunking_strategy": chunking_strategy,
        "embedding_model": embedding_model,
        "usage": {
            "prompt_tokens": generation.get("prompt_eval_count"),
            "completion_tokens": generation.get("eval_count"),
            "total_duration_ns": generation.get("total_duration"),
        },
    }
