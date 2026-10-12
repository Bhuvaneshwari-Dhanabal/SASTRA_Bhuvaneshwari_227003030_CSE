import { useCallback, useEffect, useState } from "react";
import { ArrowLeft, Download, RefreshCw, Activity, CheckCircle2, XCircle, Clock3, FileSearch } from "lucide-react";
import { useNavigate } from "react-router-dom";
import api from "../services/api";

function formatDuration(value) {
  const ms = Number(value || 0);
  return ms >= 1000 ? `${(ms / 1000).toFixed(2)} s` : `${ms.toFixed(0)} ms`;
}

function EvaluationResults() {
  const navigate = useNavigate();
  const [summary, setSummary] = useState(null);
  const [evaluations, setEvaluations] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");
  const [exporting, setExporting] = useState(false);
  const [documents, setDocuments] = useState([]);

  const loadResults = useCallback(async () => {
  setLoading(true);
  setError("");

  try {
    const [evaluationResponse, documentResponse] = await Promise.all([
      api.get("/evaluations"),
      api.get("/documents"),
    ]);

    setSummary(evaluationResponse.data.summary || {});
    setEvaluations(evaluationResponse.data.evaluations || []);
    setDocuments(documentResponse.data.documents || []);
  } catch (err) {
    setError(
      err.response?.data?.error ||
        "Could not load evaluation results. Check that the backend is running and you are signed in."
    );
  } finally {
    setLoading(false);
  }
}, []);

  useEffect(() => { loadResults(); }, [loadResults]);

  const exportResults = async () => {
    setExporting(true);
    setError("");
    try {
      const response = await api.get("/evaluations/export", { responseType: "blob" });
      const url = URL.createObjectURL(new Blob([response.data], { type: "application/json" }));
      const link = document.createElement("a");
      link.href = url;
      link.download = "autosar-evaluation-results.json";
      document.body.appendChild(link);
      link.click();
      link.remove();
      URL.revokeObjectURL(url);
    } catch (err) {
      setError(err.response?.data?.error || "Could not export evaluation results.");
    } finally { setExporting(false); }
  };

  const cards = [
    { label: "Total chat turns", value: summary?.total_runs ?? 0, icon: Activity },
    { label: "Completed", value: summary?.completed_runs ?? 0, icon: CheckCircle2 },
    { label: "Failed", value: summary?.failed_runs ?? 0, icon: XCircle },
    { label: "Average latency", value: formatDuration(summary?.average_latency_ms), icon: Clock3 },
  ];

  return (
    <div className="min-h-screen bg-gray-950 text-white">
      <header className="flex items-center justify-between border-b border-gray-800 px-5 py-4">
        <div className="flex items-center gap-3">
          <button onClick={() => navigate("/chat")} className="rounded-lg p-2 text-gray-400 hover:bg-gray-800 hover:text-white" aria-label="Back to chat"><ArrowLeft size={20} /></button>
          <div><h1 className="text-lg font-semibold">Evaluation Results</h1><p className="text-xs text-gray-500">Runtime and retrieval records for your account</p></div>
        </div>
        <div className="flex gap-2">
          <button onClick={loadResults} disabled={loading} className="flex items-center gap-2 rounded-lg border border-gray-700 px-3 py-2 text-sm text-gray-300 hover:bg-gray-800 disabled:opacity-50"><RefreshCw size={16} /> Refresh</button>
          <button onClick={exportResults} disabled={exporting} className="flex items-center gap-2 rounded-lg bg-orange-500 px-3 py-2 text-sm font-medium text-white hover:bg-orange-600 disabled:opacity-50"><Download size={16} /> {exporting ? "Exporting…" : "Export JSON"}</button>
        </div>
      </header>
      <main className="mx-auto max-w-7xl space-y-6 px-5 py-6">
        {error && <div className="rounded-xl border border-red-900 bg-red-950/40 p-4 text-sm text-red-300">{error}</div>}
        <div className="grid grid-cols-1 gap-3 sm:grid-cols-2 xl:grid-cols-4">
          {cards.map(({ label, value, icon: Icon }) => <div key={label} className="rounded-2xl border border-gray-800 bg-gray-900/50 p-5"><div className="flex items-center justify-between text-sm text-gray-400"><span>{label}</span><Icon size={18} className="text-orange-400" /></div><p className="mt-3 text-2xl font-semibold">{value}</p></div>)}
        </div>
        <div className="rounded-xl border border-blue-900/60 bg-blue-950/20 p-4 text-sm text-blue-200">
          <strong>How to interpret these results:</strong> completed/failed status, latency, retrieval count, and citations are logged automatically. Semantic correctness is not automatically assumed; each result remains <strong>Not reviewed</strong> until you evaluate its answer against the source document.
        </div>
        <section className="overflow-hidden rounded-2xl border border-gray-800 bg-gray-900/30">
          <div className="border-b border-gray-800 px-5 py-4"><h2 className="font-semibold">Chat evaluation log</h2><p className="mt-1 text-xs text-gray-500">Each row belongs to the signed-in user and its conversation.</p></div>
{loading ? (
  <p className="p-8 text-center text-sm text-gray-400">
    Loading evaluation records…
  </p>
) : evaluations.length === 0 ? (
  <div className="p-10 text-center">
    <FileSearch className="mx-auto mb-3 text-gray-600" size={32} />
    <p className="font-medium text-gray-300">No evaluation records yet</p>
    <p className="mt-1 text-sm text-gray-500">
      Ask a question in Chat. New requests will appear here automatically.
    </p>
    <button
      onClick={() => navigate("/chat")}
      className="mt-4 rounded-lg bg-orange-500 px-4 py-2 text-sm font-medium hover:bg-orange-600"
    >
      Go to Chat
    </button>
  </div>
) : (
  <div className="overflow-x-auto">
    <table className="w-full min-w-[900px] text-left text-sm">
      <thead className="bg-gray-900 text-xs uppercase tracking-wide text-gray-500">
        <tr>
          <th className="px-5 py-3">Date</th>
          <th className="px-5 py-3">Conversation</th>
          <th className="px-5 py-3">Question / Answer</th>
          <th className="px-5 py-3">Retrieval</th>
          <th className="px-5 py-3">Latency</th>
          <th className="px-5 py-3">Status</th>
          <th className="px-5 py-3">Quality</th>
        </tr>
      </thead>

      <tbody className="divide-y divide-gray-800">
        {evaluations.map((item) => {
          const document = documents.find(
            (doc) => Number(doc.id) === Number(item.document_id)
          );

          return (
            <tr
              key={item.id}
              className="align-top hover:bg-gray-900/50"
            >
              <td className="whitespace-nowrap px-5 py-4 text-xs text-gray-400">
                {item.created_at}
              </td>

              <td className="px-5 py-4 text-gray-300">
                {item.conversation_id
                  ? `Chat #${item.conversation_id}`
                  : "Unlinked"}

                <p className="mt-1 text-xs text-gray-500">
                  {item.document_id == null
                    ? "No document linked"
                    : document
                      ? document.display_name ||
                        `Document ${document.document_number}`
                      : "Document deleted"}
                </p>
              </td>

              <td className="max-w-xl px-5 py-4">
                <p className="font-medium text-gray-200">
                  {item.question}
                </p>

                {item.answer && (
                  <p className="mt-2 line-clamp-3 whitespace-pre-wrap text-xs text-gray-400">
                    {item.answer}
                  </p>
                )}

                {item.error_message && (
                  <p className="mt-2 text-xs text-red-300">
                    {item.error_message}
                  </p>
                )}
              </td>

              <td className="whitespace-nowrap px-5 py-4 text-gray-300">
                {item.retrieved_count} passages
                <p className="mt-1 text-xs text-gray-500">
                  {item.citations?.length ?? 0} citations
                </p>
              </td>

              <td className="whitespace-nowrap px-5 py-4 text-gray-300">
                {formatDuration(item.latency_ms)}
              </td>

              <td className="px-5 py-4">
                <span
                  className={`rounded-full px-2 py-1 text-xs ${
                    item.status === "completed"
                      ? "bg-green-950 text-green-300"
                      : "bg-red-950 text-red-300"
                  }`}
                >
                  {item.status}
                </span>
              </td>

              <td className="whitespace-nowrap px-5 py-4 text-xs text-amber-300">
                Not reviewed
              </td>
            </tr>
          );
        })}
      </tbody>
    </table>
  </div>
)}        </section>
      </main>
    </div>
  );
}

export default EvaluationResults;
