
import ReactMarkdown from "react-markdown";
import remarkGfm from "remark-gfm";
import rehypeHighlight from "rehype-highlight";

import "highlight.js/styles/github-dark.css";

export default function MarkdownRenderer({ content = "" }) {
  return (
    <article className="w-full min-w-0 break-words text-sm leading-7 !text-gray-200 sm:text-base">
      <ReactMarkdown
        remarkPlugins={[remarkGfm]}
        rehypePlugins={[rehypeHighlight]}
        components={{
          h1: ({ children }) => (
            <h1 className="mb-4 mt-7 text-2xl font-bold !text-white">
              {children}
            </h1>
          ),

          h2: ({ children }) => (
            <h2 className="mb-3 mt-7 border-b border-gray-700 pb-2 text-xl font-semibold !text-white">
              {children}
            </h2>
          ),

          h3: ({ children }) => (
            <h3 className="mb-2 mt-5 text-lg font-semibold !text-white">
              {children}
            </h3>
          ),

          p: ({ children }) => (
            <p className="mb-4 leading-7 !text-gray-200 last:mb-0">
              {children}
            </p>
          ),

          ul: ({ children }) => (
            <ul className="mb-4 list-disc space-y-2 pl-6 marker:text-orange-400">
              {children}
            </ul>
          ),

          ol: ({ children }) => (
            <ol className="mb-4 list-decimal space-y-2 pl-6 marker:text-orange-400">
              {children}
            </ol>
          ),

          li: ({ children }) => (
            <li className="pl-1 !text-gray-200">{children}</li>
          ),

          strong: ({ children }) => (
            <strong className="font-bold !text-white">{children}</strong>
          ),

          em: ({ children }) => (
            <em className="italic !text-gray-200">{children}</em>
          ),

          blockquote: ({ children }) => (
            <blockquote className="my-5 border-l-4 border-orange-500 bg-gray-800/60 py-3 pl-4 pr-3 !text-gray-200">
              {children}
            </blockquote>
          ),

          a: ({ href, children }) => (
            <a
              href={href}
              target="_blank"
              rel="noopener noreferrer"
              className="text-orange-400 underline underline-offset-4 hover:text-orange-300"
            >
              {children}
            </a>
          ),

          table: ({ children }) => (
            <div className="my-5 overflow-x-auto rounded-xl border border-gray-700">
              <table className="w-full border-collapse text-left text-sm">
                {children}
              </table>
            </div>
          ),

          thead: ({ children }) => (
            <thead className="bg-gray-800">{children}</thead>
          ),

          th: ({ children }) => (
            <th className="border-b border-gray-700 px-4 py-3 font-semibold !text-white">
              {children}
            </th>
          ),

          td: ({ children }) => (
            <td className="border-t border-gray-800 px-4 py-3 align-top !text-gray-200">
              {children}
            </td>
          ),

          pre: ({ children }) => (
            <pre className="my-5 overflow-x-auto rounded-xl border border-gray-700 bg-[#0d1117] p-4 text-sm leading-6">
              {children}
            </pre>
          ),

          code: ({ children, className, ...props }) =>
            className ? (
              <code className={className} {...props}>
                {children}
              </code>
            ) : (
              <code className="rounded bg-gray-800 px-1.5 py-0.5 font-mono text-sm text-orange-300">
                {children}
              </code>
            ),

          hr: () => <hr className="my-6 border-gray-700" />,
        }}
      >
        {typeof content === "string" ? content : ""}
      </ReactMarkdown>
    </article>
  );
}
