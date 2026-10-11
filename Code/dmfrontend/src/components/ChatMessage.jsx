
import { Bot, Copy, RefreshCw, User, FileText } from "lucide-react";
import { useState } from "react";
import MarkdownRenderer from "./MarkdownRenderer";

function ChatMessage({ message, onRegenerate }) {
  const [copied, setCopied] = useState(false);

  const isUser = message.role === "user";
  const content = message.content || "";

  // Read source metadata attached to the message.
  const sources = message.citations || message.sources || [];

  const pdfNames = [
    ...new Set(
      sources
        .map((item) => {
          if (typeof item === "string") return item;

          return (
            item?.filename ||
            item?.file_name ||
            item?.source_file ||
            item?.source ||
            item?.metadata?.source ||
            null
          );
        })
        .filter(Boolean)
        .map((name) => String(name).split(/[\\/]/).pop())
        .filter((name) => name.toLowerCase().endsWith(".pdf"))
    ),
  ];

  const copyMessage = async () => {
    try {
      await navigator.clipboard.writeText(content);
      setCopied(true);
      setTimeout(() => setCopied(false), 1500);
    } catch {
      console.error("Unable to copy message.");
    }
  };

  return (
    <div
      className={`w-full border-b border-gray-800/50 ${
        isUser ? "bg-gray-950" : "bg-gray-900/50"
      }`}
    >
      <div className="mx-auto flex max-w-4xl gap-4 px-4 py-6">
        <div
          className={`flex h-8 w-8 shrink-0 items-center justify-center rounded-full ${
            isUser ? "bg-orange-500" : "bg-gray-700"
          }`}
        >
          {isUser ? (
            <User size={17} className="text-white" />
          ) : (
            <Bot size={17} className="text-white" />
          )}
        </div>

        <div className="min-w-0 flex-1">
          <p className="mb-3 text-sm font-semibold text-gray-300">
            {isUser ? "You" : "AUTOSAR AI"}
          </p>

          <div className="break-words text-sm leading-7 text-gray-200">
            <MarkdownRenderer
              key={`${message.id}-${message.role}`}
              content={String(message.content ?? "")}
            />
          </div>

          {/* PDF source footer */}
          {!isUser && pdfNames.length > 0 && (
            <div className="mt-4 border-t border-gray-800 pt-3">
              <div className="flex items-start gap-2 text-xs text-gray-400">
                <FileText size={14} className="mt-0.5 shrink-0" />
                <div>
                  <span className="font-medium">Source PDF: </span>
                  {pdfNames.map((name, index) => (
                    <span key={name}>
                      {index > 0 && ", "}
                      {name}
                    </span>
                  ))}
                </div>
              </div>
            </div>
          )}

          <div className="mt-4 flex items-center gap-2">
            <button
              type="button"
              onClick={copyMessage}
              className="flex items-center gap-1.5 rounded-md px-2 py-1.5 text-xs text-gray-500 transition-colors hover:bg-gray-800 hover:text-gray-300"
              aria-label="Copy message"
            >
              <Copy size={14} />
              {copied ? "Copied" : "Copy"}
            </button>

            {!isUser && onRegenerate && (
              <button
                type="button"
                onClick={() => onRegenerate(message)}
                className="flex items-center gap-1.5 rounded-md px-2 py-1.5 text-xs text-gray-500 transition-colors hover:bg-gray-800 hover:text-gray-300"
              >
                <RefreshCw size={14} />
                Regenerate
              </button>
            )}
          </div>
        </div>
      </div>
    </div>
  );
}

export default ChatMessage;
