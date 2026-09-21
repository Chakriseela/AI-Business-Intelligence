import { useEffect, useRef, useState } from "react";
import { FileText } from "lucide-react";

import Sidebar from "./components/Sidebar";
import TopBar from "./components/TopBar";
import QuestionPanel from "./components/QuestionPanel";
import WorkflowGraph from "./components/WorkflowGraph";
import SQLInspector from "./components/SQLInspector";
import MCPInspector from "./components/MCPInspector";
import RAGInspector from "./components/RAGInspector";
import ExecutionTimeline from "./components/ExecutionTimeline";
import RAGContext from "./components/RAGContext";
import FinalAnswer from "./components/FinalAnswer";

import "./index.css";

const MODEL_CONFIG = {
  gemini: "gemini-3.6-flash",
  ollama: "qwen3.5",
};

export default function App() {
  const socketRef = useRef(null);

  const [question, setQuestion] = useState("");
  const [loading, setLoading] = useState(false);
  const [route, setRoute] = useState(null);
  const [sql, setSql] = useState(null);
  const [mcpTool, setMcpTool] = useState(null);
  const [databaseRows, setDatabaseRows] = useState(0);
  const [databaseData, setDatabaseData] = useState([]);
  const [ragSources, setRagSources] = useState([]);
  const [ragContext, setRagContext] = useState("");
  const [answer, setAnswer] = useState("");
  const [logs, setLogs] = useState([]);
  const [modelProvider, setModelProvider] = useState("gemini");
  const [agentStatus, setAgentStatus] = useState({
    orchestrator: "waiting",
    sql_agent: "waiting",
    rag_agent: "waiting",
    response_agent: "waiting",
  });

  const modelName = MODEL_CONFIG[modelProvider];

  useEffect(() => () => socketRef.current?.close(), []);

  const resetWorkflow = () => {
    setRoute(null); setSql(null); setMcpTool(null); setDatabaseRows(0); setDatabaseData([]);
    setRagSources([]); setRagContext(""); setAnswer(""); setLogs([]);
    setAgentStatus({ orchestrator: "waiting", sql_agent: "waiting", rag_agent: "waiting", response_agent: "waiting" });
  };

  const askQuestion = () => {
    if (!question.trim() || loading) return;
    socketRef.current?.close();
    resetWorkflow(); setLoading(true);

    const socket = new WebSocket("ws://127.0.0.1:8000/ws/chat");
    socketRef.current = socket;

    socket.onopen = () => socket.send(JSON.stringify({ question: question.trim(), model_provider: modelProvider, model_name: modelName }));

    socket.onmessage = (event) => {
      try {
        const data = JSON.parse(event.data);

        if (data.type === "workflow_started") { setLogs(["Workflow started"]); return; }

        if (data.type === "agent_status") {
          if (data.agent) setAgentStatus((prev) => ({ ...prev, [data.agent]: data.status }));
          if (data.agent === "orchestrator" && data.route) setRoute(data.route);
          return;
        }

        if (data.type === "agent" && data.agent === "orchestrator") {
          setRoute(data.route || null);
          setAgentStatus((prev) => ({ ...prev, orchestrator: "completed" }));
          return;
        }

        if (data.type === "agent" && data.agent === "sql_agent") {
          setAgentStatus((prev) => ({ ...prev, sql_agent: "completed" }));
          setSql(data.sql || null); setMcpTool(data.mcp_tool || null);
          setDatabaseRows(data.database_rows || 0); setDatabaseData(data.database_data || []);
          return;
        }

        if (data.type === "agent" && data.agent === "rag_agent") {
          setAgentStatus((prev) => ({ ...prev, rag_agent: "completed" }));
          setRagSources(data.sources || []); setRagContext(data.context || "");
          return;
        }

        if (data.type === "agent" && data.agent === "response_agent") {
          setAgentStatus((prev) => ({ ...prev, response_agent: "completed" }));
          if (data.answer !== undefined && data.answer !== null) setAnswer(String(data.answer));
          return;
        }

        if (data.type === "logs") { setLogs(Array.isArray(data.logs) ? data.logs : []); return; }

        if (data.type === "error") { setAnswer(data.message || "Workflow failed."); setLoading(false); return; }

        if (data.type === "workflow_completed") {
          setRoute(data.route || null);
          if (data.answer !== undefined && data.answer !== null && String(data.answer).trim()) setAnswer(String(data.answer));
          setSql(data.sql || null); setMcpTool(data.mcp_tool || null);
          setDatabaseRows(data.database_rows || 0); setDatabaseData(Array.isArray(data.database_data) ? data.database_data : []);
          setRagSources(Array.isArray(data.retrieved_documents) ? data.retrieved_documents : []);
          setRagContext(data.rag_context || ""); setLogs(Array.isArray(data.logs) ? data.logs : []);
          setLoading(false); socket.close();
        }
      } catch (error) { console.error("Failed to parse WebSocket event:", error); }
    };

    socket.onerror = () => { setAnswer("Unable to connect to the BizInsight backend."); setLoading(false); };
    socket.onclose = () => setLoading(false);
  };

  return (
    <div className="app">
      <Sidebar onNewAnalysis={() => { socketRef.current?.close(); setQuestion(""); resetWorkflow(); setLoading(false); }} />
      <main className="main">
        <TopBar />
        <QuestionPanel
          question={question}
          setQuestion={setQuestion}
          onSubmit={askQuestion}
          loading={loading}
          modelProvider={modelProvider}
          modelName={modelName}
          onModelChange={setModelProvider}
        />

        <section className="workflow-section">
          <div className="section-heading">
            <div><span>EXECUTION</span><h3>Agent Workflow</h3></div>
            {route && <div className="route-badge">ROUTE: {route}</div>}
          </div>
          <WorkflowGraph route={route} agentStatus={agentStatus} sql={sql} mcpTool={mcpTool} databaseRows={databaseRows} ragSources={ragSources} />
        </section>

        <section className="details-grid">
          <SQLInspector sql={sql} databaseRows={databaseRows} databaseData={databaseData} />
          <MCPInspector mcpTool={mcpTool} />
          <RAGInspector sources={ragSources} />
          <ExecutionTimeline logs={logs} />
        </section>

        <RAGContext context={ragContext} />
        <FinalAnswer answer={answer} loading={loading} />
      </main>
    </div>
  );
}
