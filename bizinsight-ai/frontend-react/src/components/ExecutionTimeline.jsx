import { GitBranch } from "lucide-react";
import InspectorCard from "./InspectorCard";

export default function ExecutionTimeline({ logs }) {
  return (
    <InspectorCard icon={<GitBranch size={17} />} title="Execution Timeline" className="timeline-card">
      <div className="timeline">
        {logs?.length > 0 ? logs.map((log, index) => (
          <div className="timeline-item" key={`${log}-${index}`}>
            <span className="timeline-dot" />
            <span>{log}</span>
          </div>
        )) : <span className="empty-text">Execution events will appear here.</span>}
      </div>
    </InspectorCard>
  );
}