import json

from flask import Blueprint, jsonify, request, Response

from app.auth import token_required
from app.database import get_db
from app.evaluation_service import serialize_evaluation

evaluations_bp = Blueprint("evaluations", __name__, url_prefix="/api/evaluations")


def _load_runs(user_id, conversation_id=None):
    connection = get_db()
    try:
        if conversation_id is None:
            rows = connection.execute(
                "SELECT * FROM evaluation_runs WHERE user_id = ? ORDER BY id DESC",
                (user_id,),
            ).fetchall()
        else:
            # Validate ownership first, including conversations with no evaluations.
            owned = connection.execute(
                "SELECT id FROM conversations WHERE id = ? AND user_id = ?",
                (conversation_id, user_id),
            ).fetchone()
            if owned is None:
                return None
            rows = connection.execute(
                "SELECT * FROM evaluation_runs WHERE user_id = ? AND conversation_id = ? ORDER BY id DESC",
                (user_id, conversation_id),
            ).fetchall()
        return [serialize_evaluation(row) for row in rows]
    finally:
        connection.close()


def _summary(runs):
    completed = sum(item["status"] == "completed" for item in runs)
    failed = sum(item["status"] == "failed" for item in runs)
    average_latency = (sum(item["latency_ms"] for item in runs) / len(runs)) if runs else 0.0
    citations = sum(len(item["citations"]) for item in runs)
    return {
        "total_runs": len(runs),
        "completed_runs": completed,
        "failed_runs": failed,
        "average_latency_ms": round(average_latency, 2),
        "runs_with_citations": sum(bool(item["citations"]) for item in runs),
        "total_citations": citations,
        "not_reviewed_runs": sum(item["review_status"] == "not_reviewed" for item in runs),
        "note": "These are runtime and retrieval observability metrics. Semantic answer quality has not been judged automatically.",
    }


@evaluations_bp.get("")
@token_required
def list_evaluations(user_id):
    raw_conversation_id = request.args.get("conversation_id")
    conversation_id = None
    if raw_conversation_id is not None:
        try:
            conversation_id = int(raw_conversation_id)
            if conversation_id < 1:
                raise ValueError
        except ValueError:
            return jsonify({"error": "conversation_id must be a positive integer."}), 400
    runs = _load_runs(user_id, conversation_id)
    if runs is None:
        return jsonify({"error": "Conversation not found."}), 404
    return jsonify({"summary": _summary(runs), "evaluations": runs}), 200


@evaluations_bp.get("/export")
@token_required
def export_evaluations(user_id):
    raw_conversation_id = request.args.get("conversation_id")
    conversation_id = None
    if raw_conversation_id is not None:
        try:
            conversation_id = int(raw_conversation_id)
            if conversation_id < 1:
                raise ValueError
        except ValueError:
            return jsonify({"error": "conversation_id must be a positive integer."}), 400
    runs = _load_runs(user_id, conversation_id)
    if runs is None:
        return jsonify({"error": "Conversation not found."}), 404
    payload = {"summary": _summary(runs), "evaluations": runs}
    filename = f"autosar-evaluation-user-{user_id}.json"
    return Response(
        json.dumps(payload, ensure_ascii=False, indent=2),
        mimetype="application/json",
        headers={"Content-Disposition": f'attachment; filename="{filename}"'},
    )
