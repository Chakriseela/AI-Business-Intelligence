import { FileText } from "lucide-react";

export default function RAGContext({ context }) {
  if (!context) return null;

  return (
    <section className="detail-card rag-context-card">
      <div className="card-title"><FileText size={17} /> Retrieved Knowledge</div>
      <details className="retrieved-knowledge" open>
        <summary>Show retrieved context</summary>
        <div className="code-panel">{context}</div>
      </details>
    </section>
  );
}
