import { FileText } from "lucide-react";
import InspectorCard from "./InspectorCard";

export default function RAGInspector({ sources }) {
  return (
    <InspectorCard icon={<FileText size={17} />} title="RAG Sources">
      <div className="sources">
        {sources?.length > 0 ? sources.map((doc, index) => (
          <div className="source-item" key={`${doc.document}-${doc.page}-${index}`}>
            <FileText size={15} />
            <div><strong>{doc.document}</strong><span>Page {doc.page}</span></div>
          </div>
        )) : <span className="empty-text">No documents retrieved.</span>}
      </div>
    </InspectorCard>
  );
}
