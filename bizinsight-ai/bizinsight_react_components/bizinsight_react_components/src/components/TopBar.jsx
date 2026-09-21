import { GitBranch } from "lucide-react";

export default function TopBar() {
  return (
    <header className="topbar">
      <div>
        <div className="eyebrow">AI OPERATIONS CONSOLE</div>
        <h2>Ask your business anything</h2>
      </div>
      <div className="architecture-badge"><GitBranch size={16} /> Multi-Agent Workflow</div>
    </header>
  );
}
