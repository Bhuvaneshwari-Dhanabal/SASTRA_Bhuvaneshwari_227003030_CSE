import json
import sqlite3

from app.database import get_db


def record_evaluation_run(
    *, user_id, conversation_id, document_id, question, answer=None,
    citations=None, retrieved_count=0, top_k=5, chunking_strategy="fixed",
    embedding_model="minilm", generation_model=None, status="completed",
    latency_ms=0.0, error_message=None,
):
    """Persist one chat turn's runtime/evidence metadata for its owner.

    Semantic quality is intentionally not inferred from request success.
    Every new run starts with review_status='not_reviewed'.
    """
    connection = get_db()
    try:
        connection.execute(
            """
            INSERT INTO evaluation_runs (
                user_id, conversation_id, document_id, question, answer,
                citations_json, retrieved_count, top_k, chunking_strategy,
                embedding_model, generation_model, status, review_status,
                latency_ms, error_message
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, 'not_reviewed', ?, ?)
            """,
            (
                user_id, conversation_id, document_id, question, answer,
                json.dumps(citations or [], ensure_ascii=False),
                int(retrieved_count or 0), int(top_k or 5),
                str(chunking_strategy or "fixed"),
                str(embedding_model or "minilm"), generation_model, status,
                max(0.0, float(latency_ms or 0.0)), error_message,
            ),
        )
        connection.commit()
    except (sqlite3.Error, TypeError, ValueError):
        connection.rollback()
        raise
    finally:
        connection.close()


def serialize_evaluation(row):
    try:
        citations = json.loads(row["citations_json"] or "[]")
    except (json.JSONDecodeError, TypeError):
        citations = []
    return {
        "id": row["id"],
        "user_id": row["user_id"],
        "conversation_id": row["conversation_id"],
        "document_id": row["document_id"],
        "question": row["question"],
        "answer": row["answer"],
        "citations": citations,
        "retrieved_count": row["retrieved_count"],
        "top_k": row["top_k"],
        "chunking_strategy": row["chunking_strategy"],
        "embedding_model": row["embedding_model"],
        "generation_model": row["generation_model"],
        "status": row["status"],
        "review_status": row["review_status"],
        "latency_ms": row["latency_ms"],
        "error_message": row["error_message"],
        "created_at": row["created_at"],
    }
