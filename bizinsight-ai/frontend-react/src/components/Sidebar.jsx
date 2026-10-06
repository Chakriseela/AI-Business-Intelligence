import { Sparkles, Plus, Settings2 } from "lucide-react";

export default function Sidebar({ onNewAnalysis }) {
  return (
    <aside className="sidebar">
      <div className="brand">
        <div className="brand-icon"><Sparkles size={20} /></div>
        <div>
          <h1>BizInsight AI</h1>
          <span>Business Intelligence Copilot</span>
        </div>
      </div>

      <button className="new-chat" onClick={onNewAnalysis}>
        <Plus size={15} />
        New Analysis
      </button>

      <div className="sidebar-section">
        <p className="sidebar-label">RECENT ANALYSIS</p>
        <div className="history-item active">Platinum Customers</div>
        <div className="history-item">Sales Analysis</div>
        <div className="history-item">Refund Policy</div>
      </div>

      <div className="sidebar-section sidebar-capabilities">
        <p className="sidebar-label">CAPABILITIES</p>
        <div className="capability-item"><span>LangGraph</span><span>Orchestration</span></div>
        <div className="capability-item"><span>MCP</span><span>Tools</span></div>
        <div className="capability-item"><span>RAG</span><span>Knowledge</span></div>
      </div>

      <div className="sidebar-footer">
        <div className="system-status"><span className="status-dot" /> Systems Online</div>
        <div className="stack-label"><Settings2 size={12} /> Local AI Workspace</div>
      </div>
    </aside>
  );
}