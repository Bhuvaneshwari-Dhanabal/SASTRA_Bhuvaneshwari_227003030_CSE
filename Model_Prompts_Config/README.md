# Model and Prompt Configuration — AUTOSAR HLD Document Analysis Assistant

## 1. Overview

The `Model_Prompts_Config/` directory documents the configuration used by the AI-Powered AUTOSAR High-Level Design (HLD) Document Analysis Assistant.

It covers the language model, embedding models, retrieval settings, prompt instructions, and other parameters that influence document retrieval and answer generation.

The purpose of this directory is to make the AI pipeline easier to understand, reproduce, maintain, and evaluate.

## 2. Configuration Components

The directory may contain the following files, depending on the current implementation:

```text
Model_Prompts_Config/
├── README.md
├── model_config.json
└── rag_prompt.txt
```

These filenames are recommended. Keep the existing project configuration filenames if they differ.

### `model_config.json`

This file documents model and retrieval settings, where supported by the application.

Example configuration:

```json
{
  "embedding_models": {
    "minilm": "sentence-transformers/all-MiniLM-L6-v2",
    "mpnet": "sentence-transformers/all-mpnet-base-v2",
    "bge": "BAAI/bge-base-en-v1.5",
    "multilingual_minilm": "sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2"
  },
  "default_embedding_model": "minilm",
  "index_type": "IndexFlatIP",
  "similarity_metric": "cosine_similarity",
  "default_top_k": 5,
  "llm_runtime": "Ollama",
  "llm_model": "qwen2.5:3b"
}
```

**Important:** The JSON above is a documentation example. Verify each key, model identifier, and value against the configuration actually loaded by the current backend before using it as an executable configuration file. Do not replace working configuration with this example without checking compatibility.

### `rag_prompt.txt`

This file documents the system instructions used to guide retrieval-augmented answer generation.

The prompt should encourage the model to:

- Answer technical questions using the retrieved document evidence.
- Avoid inventing facts, interfaces, requirements, or references.
- Identify when the available evidence is insufficient.
- Include citations that correspond to the retrieved source passages.
- Distinguish explicitly stated document facts from interpretations.
- Treat retrieved document text as untrusted content rather than instructions that override system-level rules.
- Use clear, structured Markdown when presenting technical explanations.

The prompt in this directory should remain synchronized with the prompt actually used by the backend.

## 3. Embedding Models

Embedding models transform document chunks and user questions into vector representations used for semantic retrieval.

The project configuration may support multiple embedding models so their retrieval performance can be compared.

| Model Identifier | Model | Purpose |
|---|---|---|
| `minilm` | `sentence-transformers/all-MiniLM-L6-v2` | Lightweight semantic embeddings |
| `mpnet` | `sentence-transformers/all-mpnet-base-v2` | Alternative embedding model for comparison |
| `bge` | `BAAI/bge-base-en-v1.5` | Alternative embedding model for retrieval experiments |
| `multilingual_minilm` | `sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2` | Multilingual embedding option |

Actual availability depends on the implemented configuration, installed dependencies, and model-download requirements.

## 4. Vector Index and Retrieval Configuration

### FAISS Index

The application uses FAISS for similarity-based vector retrieval.

The configured index type may be `IndexFlatIP`, which performs exact inner-product search. When embeddings are normalized, inner-product ranking corresponds to cosine-similarity ranking.

### Top-k Retrieval

The `top_k` parameter determines how many candidate passages are retrieved for a question.

For example, `top_k = 5` requests up to five candidate passages, subject to the available indexed content and the actual retrieval implementation.

The number of retrieved passages influences:

- Context available to the language model.
- Retrieval latency.
- The risk of including irrelevant passages.
- The amount of context that can fit into the model input.

### Chunking Configuration

Chunking determines how document text is divided into retrievable units.

When the application supports multiple chunking strategies, document the following parameters for each strategy:

- Chunking strategy name.
- Chunk size.
- Chunk overlap.
- Boundary handling.
- Any document-specific preprocessing.

Only list chunking options that are actually implemented and available in the application.

## 5. Language Model Configuration

The documented target configuration uses Ollama with the `qwen2.5:3b` model for local language-model inference.

The model generates answers from the retrieved evidence and configured prompt.

Before execution, verify that:

- Ollama is installed and running.
- The configured model is available in the Ollama environment.
- The backend uses the expected model identifier.
- The model runtime is accessible from the backend container or host.
- Model errors and timeouts are handled appropriately.

Model availability and response quality depend on the execution environment, model version, prompt, retrieved context, and generation parameters.

## 6. Prompt Design Principles

The system prompt should follow these principles.

### Evidence Grounding

Answers should be based on the retrieved source passages rather than unsupported assumptions or general model knowledge when the question requires document-specific information.

### Citation Integrity

Citations should refer to actual retrieved sources. The model must not invent page numbers, document sections, or references.

### Uncertainty Handling

When the retrieved evidence does not adequately answer a question, the assistant should explain the limitation and request more information when appropriate.

### Instruction Separation

Text retrieved from user-uploaded documents must be treated as source content, not as instructions that can override the application's system prompt or security requirements.

### Technical Precision

AUTOSAR concepts, interfaces, components, requirements, and architecture details should be described accurately and without unsupported claims.

## 7. Evaluation and Model Comparison

Model and retrieval configuration changes should be evaluated against a consistent set of questions and source documents.

Recommended evaluation dimensions include:

- Retrieval relevance.
- Evidence coverage.
- Citation correctness.
- Answer faithfulness to retrieved passages.
- Answer completeness.
- Appropriate refusal or uncertainty when evidence is insufficient.
- Response latency.
- Resource usage, where measured.

When comparing embedding models or chunking strategies, keep the evaluation dataset and other relevant settings consistent so that differences can be interpreted meaningfully.

Evaluation results and supporting evidence should be stored in `Evaluation_Results/`.

## 8. Configuration Management

When updating model or prompt settings:

1. Record the previous configuration.
2. Change only the intended parameters.
3. Verify that the backend loads the updated settings.
4. Run retrieval and answer-generation tests.
5. Record the evaluation results.
6. Update this README if the documented configuration changes.
7. Commit the configuration and documentation together when appropriate.

Do not store passwords, API keys, authentication tokens, or other secrets in this directory.

## 9. Responsible AI and Limitations

The assistant is intended to support document understanding and retrieval. Generated answers may still be incomplete, misleading, or incorrect.

Important safeguards include:

- Evidence-grounded answer generation.
- Citation validation.
- Explicit communication of insufficient evidence.
- Protection of user-specific documents and conversation records.
- Human review of engineering decisions.
- Documented evaluation rather than unsupported accuracy claims.

The assistant must not be treated as a replacement for formal AUTOSAR validation, safety analysis, engineering review, or system verification.

## 10. Maintenance

Keep this documentation aligned with the actual source code, loaded configuration, and deployed model versions. Any differences between the documented and executable settings should be resolved before reporting experimental results.
