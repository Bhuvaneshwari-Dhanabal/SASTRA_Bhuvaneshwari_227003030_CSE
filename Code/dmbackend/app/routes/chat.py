
from flask import Blueprint, jsonify, request
import time

from app.database import get_db
from app.evaluation_service import record_evaluation_run

from app.auth import token_required
from app.ollama_service import OllamaError
from app.rag_service import answer_question


chat_bp = Blueprint(
    "chat",
    __name__,
    url_prefix="/api/chat",
)


def authenticated_user_id(current_user):
    """Extract the ID from a dictionary, row, or user object."""
    if isinstance(current_user, dict):
        user_id = current_user.get("id")
    else:
        try:
            user_id = current_user["id"]
        except (TypeError, KeyError, IndexError):
            user_id = getattr(current_user, "id", None)

    if user_id is None:
        raise ValueError("Authenticated user ID is unavailable.")

    return user_id


@chat_bp.route("/ask", methods=["POST"])
@token_required
def ask_question(user_id):
    payload = request.get_json(silent=True) or {}

    question = payload.get("question")
    document_id = payload.get("document_id")
    top_k = payload.get("top_k", 5)
    chunking_strategy = payload.get("chunking_strategy", "fixed")
    embedding_model = payload.get("embedding_model", "minilm")
    conversation_id = payload.get("conversation_id")

    if not isinstance(question, str) or not question.strip():
        return jsonify({
            "error": "A non-empty question is required."
        }), 400

    try:
        document_id = int(document_id)
        if document_id < 1:
            raise ValueError
    except (ValueError, TypeError):
        return jsonify({
            "error": "document_id must be a positive integer."
        }), 400

    if (
        not isinstance(top_k, int)
        or isinstance(top_k, bool)
        or not 1 <= top_k <= 10
    ):
        return jsonify({
            "error": "top_k must be an integer from 1 to 10."
        }), 400

    if not isinstance(chunking_strategy, str):
        return jsonify({
            "error": "chunking_strategy must be a string."
        }), 400

    if not isinstance(embedding_model, str):
        return jsonify({
            "error": "embedding_model must be a string."
        }), 400

    if conversation_id is not None:
        try:
            conversation_id = int(conversation_id)
            if conversation_id < 1:
                raise ValueError
        except (ValueError, TypeError):
            return jsonify({
                "error": "conversation_id must be a positive integer."
            }), 400
        connection = get_db()
        try:
            owned_conversation = connection.execute(
                "SELECT id FROM conversations WHERE id = ? AND user_id = ?",
                (conversation_id, user_id),
            ).fetchone()
        finally:
            connection.close()
        if owned_conversation is None:
            return jsonify({"error": "Conversation not found."}), 404

    started_at = time.perf_counter()

    try:

        result = answer_question(
            document_id=document_id,
            user_id=user_id,
            question=question,
            top_k=top_k,
            chunking_strategy=chunking_strategy,
            embedding_model=embedding_model,
        )

        latency_ms = (time.perf_counter() - started_at) * 1000
        evaluation_logged = False
        try:
            record_evaluation_run(
                user_id=user_id,
                conversation_id=conversation_id,
                document_id=document_id,
                question=question.strip(),
                answer=result.get("answer"),
                citations=result.get("citations", []),
                retrieved_count=result.get("retrieved_count", 0),
                top_k=top_k,
                chunking_strategy=result.get("chunking_strategy", chunking_strategy),
                embedding_model=result.get("embedding_model", embedding_model),
                generation_model=result.get("model"),
                status="completed",
                latency_ms=latency_ms,
            )
            evaluation_logged = True
        except Exception:
            # Evaluation logging must never break the existing chat response.
            pass
        result["evaluation"] = {
            "logged": evaluation_logged,
            "review_status": "not_reviewed",
            "latency_ms": round(latency_ms, 2),
        }
        return jsonify(result), 200

    except LookupError as exc:
        _record_failed_run(user_id, conversation_id, document_id, question, top_k, chunking_strategy, embedding_model, started_at, str(exc))
        return jsonify({"error": str(exc)}), 404

    except ValueError as exc:
        _record_failed_run(user_id, conversation_id, document_id, question, top_k, chunking_strategy, embedding_model, started_at, str(exc))
        return jsonify({"error": str(exc)}), 400

    except FileNotFoundError:
        error_message = (
            "The document index was not found. Check that this document has been indexed "
            "using the selected chunking and embedding settings."
        )
        _record_failed_run(user_id, conversation_id, document_id, question, top_k, chunking_strategy, embedding_model, started_at, error_message)
        return jsonify({"error": error_message}), 409

    except OllamaError as exc:
        _record_failed_run(user_id, conversation_id, document_id, question, top_k, chunking_strategy, embedding_model, started_at, str(exc))
        return jsonify({
            "error": "Answer generation failed.",
            "details": str(exc),
        }), 502

    except Exception as exc:
        # Unexpected failures are logged too, while keeping a JSON API response.
        _record_failed_run(user_id, conversation_id, document_id, question, top_k, chunking_strategy, embedding_model, started_at, str(exc))
        return jsonify({"error": "An unexpected error occurred while answering the question."}), 500


def _record_failed_run(user_id, conversation_id, document_id, question, top_k, chunking_strategy, embedding_model, started_at, error_message):
    """Best-effort failure logging; never masks the original API error."""
    try:
        record_evaluation_run(
            user_id=user_id,
            conversation_id=conversation_id,
            document_id=document_id,
            question=question.strip() if isinstance(question, str) else str(question or ""),
            top_k=top_k if isinstance(top_k, int) and not isinstance(top_k, bool) else 5,
            chunking_strategy=chunking_strategy if isinstance(chunking_strategy, str) else "fixed",
            embedding_model=embedding_model if isinstance(embedding_model, str) else "minilm",
            status="failed",
            latency_ms=(time.perf_counter() - started_at) * 1000,
            error_message=error_message[:1000],
        )
    except Exception:
        pass
