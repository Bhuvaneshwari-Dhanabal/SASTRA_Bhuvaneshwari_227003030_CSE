# Evaluation Results

Evaluation records are created automatically by the backend in the SQLite database at `Code/dmbackend/data/autosar.db`. The authenticated `/api/evaluations` endpoint shows only records owned by the current user. `/api/evaluations/export` exports that same user's records as JSON.

The dashboard records runtime/retrieval observability (success/failure, latency, retrieved passages, citations, model/settings, question and answer). It intentionally does **not** claim semantic correctness automatically. For capstone accuracy/faithfulness results, create a labelled test set with expected answers/evidence and run a separate repeatable evaluation; do not report HTTP success as answer accuracy. Runtime database/log data should not be committed to Git.

## API endpoints

- `GET /api/evaluations` — list the signed-in user's evaluation records and summary.
- `GET /api/evaluations?conversation_id=123` — list records for one conversation owned by the signed-in user.
- `GET /api/evaluations/export` — download that user's records as JSON.
- `GET /api/evaluations/export?conversation_id=123` — export one owned conversation's records.

All endpoints require `Authorization: Bearer <access-token>`. The user ID is derived from the validated token, not a client-supplied user ID.

## Smoke test

1. Sign in and ask a question in a new chat.
2. Open **Evaluation Results** from the sidebar. Confirm a new row shows the same chat ID, question, retrieval count, citation count, status, and latency.
3. Click **Export JSON** and inspect the downloaded report.
4. Sign in as a different user. Confirm the first user's rows are not returned.
5. Request `/api/evaluations?conversation_id=<other-user-chat-id>` using the second user's token; it should return `404`.
6. Stop Ollama or use an unavailable index, ask a question, and confirm the failed request is logged when the failure reaches the chat processing stage.
