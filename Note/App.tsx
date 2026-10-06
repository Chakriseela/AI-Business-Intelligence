import { useEffect, useMemo, useRef, useState } from "react";
 
import {

  ReactFlow,

  Background,

  Controls,

  Handle,

  Position,

} from "@xyflow/react";
 
import "@xyflow/react/dist/style.css";
 
import {

  Bot,

  Database,

  FileText,

  GitBranch,

  Send,

  Server,

  Sparkles,

  Wrench,

} from "lucide-react";
 
import "./index.css";
 
 
// =========================================================

// Custom React Flow Node

// =========================================================
 
function WorkflowNode({ data }) {

  const iconMap = {

    orchestrator: Bot,

    sql_agent: Database,

    mcp: Server,

    sqlite: Database,

    rag_agent: FileText,

    chroma: Database,

    documents: FileText,

    response_agent: Sparkles,

  };
 
  const Icon = iconMap[data.type] || Bot;
 
  return (
<div

      className={`workflow-flow-node status-${data.status}`}
>
<Handle

        type="target"

        position={Position.Top}

        className="flow-handle"

      />
 
      <div className="flow-node-icon">
<Icon size={17} />
</div>
 
      <div className="flow-node-content">
<strong>{data.label}</strong>
 
        <span>{data.detail}</span>
 
        <small>

          {data.status === "running" &&

            "Running..."}
 
          {data.status === "completed" &&

            "Completed"}
 
          {data.status === "error" &&

            "Error"}
 
          {data.status === "waiting" &&

            "Waiting"}
</small>
</div>
 
      <Handle

        type="source"

        position={Position.Bottom}

        className="flow-handle"

      />
</div>

  );

}
 
 
const nodeTypes = {

  workflow: WorkflowNode,

};
 
 
// =========================================================

// APP

// =========================================================
 
function App() {

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
  const [agentStatus, setAgentStatus] = useState({
    orchestrator: "waiting",
    sql_agent: "waiting",
    rag_agent: "waiting",
    response_agent: "waiting",
  });
  const [modelProvider, setModelProvider] = useState("gemini");
  const [modelName, setModelName] = useState("gemini-3.6-flash");
 
 
  // =========================================================
  // Cleanup WebSocket
  // =========================================================
 
  useEffect(() => {
    return () => {

      if (socketRef.current) {
        socketRef.current.close();
      }
    };
  }, []);
 
  // =========================================================
  // Reset Workflow
  // =========================================================
 
  const resetWorkflow = () => {
    setRoute(null);
    setSql(null);
    setMcpTool(null);
    setDatabaseRows(0);
    setDatabaseData([]);
    setRagSources([]);
    setRagContext("");
    setAnswer("");
    setLogs([]);
    setAgentStatus({

      orchestrator: "waiting",
      sql_agent: "waiting",
      rag_agent: "waiting",
      response_agent: "waiting",
    });

  };
 
 
  // =========================================================
  // Run Workflow
  // =========================================================
 
  const askQuestion = () => {
    if (!question.trim() || loading) {
      return;
    }
 
    // Close any previous connection

    if (socketRef.current) {
      socketRef.current.close();
      socketRef.current = null;
    }
 
    resetWorkflow();
    setLoading(true);
 
    // -------------------------------------------------------
    // Open WebSocket
    // -------------------------------------------------------
 
    const socket = new WebSocket(
      "ws://127.0.0.1:8000/ws/chat"
    );
 
    socketRef.current = socket;

    // =======================================================
    // Connected
    // =======================================================

    socket.onopen = () => {
      console.log(
        "Connected to BizInsight WebSocket"
      );
      socket.send(
        JSON.stringify({
          question: question.trim(),
          model_provider: modelProvider,
          model_name: modelName,
        })
      );
    };
 
 
    // =======================================================
    // Receive Events
    // =======================================================
 
    socket.onmessage = (event) => {
      try {
        const data = JSON.parse(event.data);
        console.log(
          "WebSocket event:",
          data
        );
 
 
        // ===================================================

        // Workflow Started

        // ===================================================
 
        if (
          data.type === "workflow_started"
        ) {
          setLogs(["Workflow started"]);

          return;
        }
 
 
        // ===================================================
        // Agent Status
        // ===================================================
        if (
          data.type === "agent_status"
        ) {

          const agent = data.agent;
          const status = data.status;

          if (agent) {
            setAgentStatus((prev) => ({
              ...prev,
              [agent]: status,
            }));
          }
 
          if (
            agent === "orchestrator" &&
            data.route
          ) {

            setRoute(data.route);
          }
          return;
        }
 
 
        // ===================================================
        // Orchestrator
        // ===================================================
 
        if (
          data.type === "agent" &&
          data.agent === "orchestrator"
        ) {

          setRoute(
            data.route || null
          );
 
          setAgentStatus((prev) => ({
            ...prev,
            orchestrator: "completed",
          }));
          return;
        }
 
        // ===================================================
        // SQL Agent
        // ===================================================
 
        if (
          data.type === "agent" &&
          data.agent === "sql_agent"
        ) {

          setAgentStatus((prev) => ({
            ...prev,
            sql_agent: "completed",
          }));
 
          setSql(
            data.sql || null
          );
 
          setMcpTool(
            data.mcp_tool || null
          );
 
          setDatabaseRows(
            data.database_rows || 0
          );
 
          setDatabaseData(
            data.database_data || []
          );
          return;
        }
 
 
        // ===================================================
        // RAG Agent
        // ===================================================
 
        if (
          data.type === "agent" &&
          data.agent === "rag_agent"
        ) {

          setAgentStatus((prev) => ({
            ...prev,
            rag_agent: "completed",
          }));

          setRagSources(
            data.sources || []
          );
 
          setRagContext(
            data.context || ""
          );
 
          return;
        }
 
 
        // ===================================================
        // Response Agent
        // ===================================================
 
        if (
          data.type === "agent" &&
          data.agent === "response_agent"
        ) {

          setAgentStatus((prev) => ({
            ...prev,
            response_agent: "completed",
          }));
 
          // IMPORTANT:
          // Keep the answer in state.

          if (
            data.answer !== undefined &&
            data.answer !== null
          ) {
            setAnswer(
              String(data.answer)
            );
          }
 
          return;
        }
 
        // ===================================================
        // Logs
        // ===================================================
 
        if (
          data.type === "logs"
        ) {

          setLogs(
            Array.isArray(data.logs)
              ? data.logs
              : []
          );
 
          return;
        }
 
        // ===================================================
        // Generic Node Update
        // ===================================================
 
        if (
          data.type === "node_update"
        ) {

          return;

        }
 
 
        // ===================================================

        // Error

        // ===================================================
 
        if (

          data.type === "error"

        ) {

          setAnswer(

            data.message ||

              "Workflow failed."

          );
 
          setLoading(false);
 
          return;

        }
 
 
        // ===================================================

        // Workflow Completed

        // ===================================================
 
        if (

          data.type ===

          "workflow_completed"

        ) {

          setRoute(

            data.route || null

          );
 
          // IMPORTANT:

          // Only update answer if backend actually

          // returned an answer.

          if (

            data.answer !== undefined &&

            data.answer !== null &&

            String(data.answer).trim()

          ) {

            setAnswer(

              String(data.answer)

            );

          }
 
          setSql(

            data.sql || null

          );
 
          setMcpTool(

            data.mcp_tool || null

          );
 
          setDatabaseRows(

            data.database_rows || 0

          );
 
          setDatabaseData(

            Array.isArray(

              data.database_data

            )

              ? data.database_data

              : []

          );
 
          setRagSources(

            Array.isArray(

              data.retrieved_documents

            )

              ? data.retrieved_documents

              : []

          );
 
          setRagContext(

            data.rag_context || ""

          );
 
          setLogs(

            Array.isArray(data.logs)

              ? data.logs

              : []

          );
 
          setLoading(false);
 
          // Close only after processing the

          // completed payload.

          socket.close();
 
          return;

        }
 
      } catch (error) {

        console.error(

          "Failed to parse WebSocket event:",

          error

        );

      }

    };
 
 
    // =======================================================

    // WebSocket Error

    // =======================================================
 
    socket.onerror = (error) => {

      console.error(

        "WebSocket error:",

        error

      );
 
      setAnswer(

        "Unable to connect to the BizInsight backend."

      );
 
      setLoading(false);

    };
 
 
    // =======================================================

    // WebSocket Closed

    // =======================================================
 
    socket.onclose = () => {

      console.log(

        "BizInsight WebSocket closed"

      );
 
      // Do NOT clear answer/result here.

      // The workflow result should remain visible.

      setLoading(false);

    };

  };
 
 
  // =========================================================

  // Enter Key

  // =========================================================
 
  const handleKeyDown = (event) => {

    if (

      event.key === "Enter" &&

      !event.shiftKey

    ) {

      event.preventDefault();
 
      askQuestion();

    }

  };
 
 
  // =========================================================

  // Route Helpers

  // =========================================================
 
  const hasSQL =

    route === "SQL" ||

    route === "BOTH";
 
  const hasRAG =

    route === "RAG" ||

    route === "BOTH";
 
 
  // =========================================================

  // React Flow Nodes

  // =========================================================
 
  const flowNodes = useMemo(() => {

    return [

      // -----------------------------------------------

      // Orchestrator

      // -----------------------------------------------
 
      {

        id: "orchestrator",
 
        type: "workflow",
 
        position: {

          x: 430,

          y: 20,

        },
 
        data: {

          type: "orchestrator",
 
          label: "Orchestrator",
 
          detail:

            route

              ? `Route → ${route}`

              : "Waiting for request",
 
          status:

            agentStatus.orchestrator,

        },

      },
 
 
      // -----------------------------------------------

      // SQL Agent

      // -----------------------------------------------
 
      {

        id: "sql_agent",
        type: "workflow",
        position: {
          x: 100,
          y: 190,
        },

        data: {
          type: "sql_agent",
          label: "SQL Agent",
          detail:
            hasSQL
              ? sql
                ? "SQL generated"
                : "Analyzing structured data"
              : "Not selected",
          status:
            hasSQL
              ? agentStatus.sql_agent

              : "waiting",

        },

      },
 
      // -----------------------------------------------
      // MCP Server
      // -----------------------------------------------
 
      {
        id: "mcp",
        type: "workflow",
        position: {
          x: 100,
          y: 350,
        },
        data: {
          type: "mcp",
          label: "MCP Server",
          detail:
            mcpTool ||
            "Waiting for SQL tool",
          status:
            hasSQL && mcpTool
              ? "completed"
              : "waiting",
        },
      },
 
 
      // -----------------------------------------------
      // SQLite
      // -----------------------------------------------
 
      {
        id: "sqlite",
        type: "workflow",
        position: {
          x: 100,
          y: 510,
        },
        data: {
          type: "sqlite",
          label: "SQLite",
          detail:
            databaseRows > 0
              ? `${databaseRows} rows returned`
              : "Business database",
          status:
            hasSQL &&
            databaseRows > 0
              ? "completed"
              : "waiting",
        },
      },
 
      // -----------------------------------------------
      // RAG Agent
      // -----------------------------------------------
      {
        id: "rag_agent",
        type: "workflow",
        position: {
          x: 650,
          y: 190,
        },
        data: {
          type: "rag_agent",
          label: "RAG Agent",
          detail:
            hasRAG
              ? ragSources.length > 0
                ? `${ragSources.length} sources`
                : "Searching knowledge base"
              : "Not selected",
          status:
            hasRAG
              ? agentStatus.rag_agent
              : "waiting",
        },
      },
 
      // -----------------------------------------------
      // ChromaDB
      // -----------------------------------------------
 
      {
        id: "chroma",
        type: "workflow",
        position: {
          x: 650,
          y: 350,
        },
        data: {
          type: "chroma",
          label: "ChromaDB",
          detail:
            ragSources.length > 0
              ? `${ragSources.length} documents`
              : "Vector search",
          status:
            hasRAG &&
            ragSources.length > 0
              ? "completed"
              : "waiting",
        },
      },
 
      // -----------------------------------------------
      // Knowledge Base
      // -----------------------------------------------
      {
        id: "documents",
        type: "workflow",
        position: {
          x: 650,
          y: 510,
        },
        data: {
          type: "documents",
          label: "Knowledge Base",
          detail:
            ragSources.length > 0
              ? ragSources[0].document
              : "Company PDFs",
          status:
            hasRAG &&
            ragSources.length > 0
              ? "completed"
              : "waiting",
        },
      },
 
      // -----------------------------------------------
      // Response Agent
      // -----------------------------------------------

      {
        id: "response_agent",
        type: "workflow",
        position: {

          x: 430,

          y: 700,

        },
 
        data: {

          type: "response_agent",
 
          label: "Response Agent",
 
          detail:

            answer

              ? "Answer synthesized"

              : "Waiting for evidence",
 
          status:

            agentStatus.response_agent,

        },

      },

    ];

  }, [

    route,

    sql,

    mcpTool,

    databaseRows,

    ragSources,

    answer,

    hasSQL,

    hasRAG,

    agentStatus,

  ]);
 
 
  // =========================================================

  // React Flow Edges

  // =========================================================
 
  const flowEdges = useMemo(() => {

    return [

      {

        id: "orchestrator-sql",

        source: "orchestrator",

        target: "sql_agent",
 
        animated: hasSQL,
 
        className:

          hasSQL

            ? "flow-edge-active"

            : "",

      },
 
      {

        id: "sql-mcp",

        source: "sql_agent",

        target: "mcp",
 
        animated:

          hasSQL &&

          !!mcpTool,
 
        className:

          hasSQL && mcpTool

            ? "flow-edge-active"

            : "",

      },
 
      {

        id: "mcp-sqlite",

        source: "mcp",

        target: "sqlite",
 
        animated:

          hasSQL &&

          databaseRows > 0,
 
        className:

          hasSQL &&

          databaseRows > 0

            ? "flow-edge-active"

            : "",

      },
 
      {

        id: "sqlite-response",

        source: "sqlite",

        target: "response_agent",
 
        animated:

          hasSQL &&

          databaseRows > 0,
 
        className:

          hasSQL &&

          databaseRows > 0

            ? "flow-edge-active"

            : "",

      },
 
      {

        id: "orchestrator-rag",

        source: "orchestrator",

        target: "rag_agent",
 
        animated: hasRAG,
 
        className:

          hasRAG

            ? "flow-edge-active"

            : "",

      },
 
      {

        id: "rag-chroma",

        source: "rag_agent",

        target: "chroma",
 
        animated:

          hasRAG &&

          ragSources.length > 0,
 
        className:

          hasRAG &&

          ragSources.length > 0

            ? "flow-edge-active"

            : "",

      },
 
      {

        id: "chroma-documents",

        source: "chroma",

        target: "documents",
 
        animated:

          hasRAG &&

          ragSources.length > 0,
 
        className:

          hasRAG &&

          ragSources.length > 0

            ? "flow-edge-active"

            : "",

      },
 
      {

        id: "documents-response",

        source: "documents",

        target: "response_agent",
 
        animated:

          hasRAG &&

          ragSources.length > 0,
 
        className:

          hasRAG &&

          ragSources.length > 0

            ? "flow-edge-active"

            : "",

      },

    ];

  }, [

    hasSQL,

    hasRAG,

    mcpTool,

    databaseRows,

    ragSources,

  ]);
 
 
  // =========================================================

  // Render

  // =========================================================
 
  return (
<div className="app">
 
      {/* ================================================= */}

      {/* SIDEBAR */}

      {/* ================================================= */}
 
      <aside className="sidebar">
 
        <div className="brand">
 
          <div className="brand-icon">
<Sparkles size={20} />
</div>
 
          <div>
<h1>BizInsight AI</h1>
 
            <span>

              Business Intelligence Copilot
</span>
</div>
 
        </div>
 
 
        <button

          className="new-chat"

          onClick={() => {

            if (socketRef.current) {

              socketRef.current.close();

            }
 
            setQuestion("");

            resetWorkflow();

            setLoading(false);

          }}
>

          + New Analysis
</button>
 
 
        <div className="sidebar-section">
 
          <p className="sidebar-label">

            RECENT ANALYSIS
</p>
 
          <div className="history-item active">

            Platinum Customers
</div>
 
          <div className="history-item">

            Sales Analysis
</div>
 
          <div className="history-item">

            Refund Policy
</div>
 
        </div>
 
 
        <div className="sidebar-footer">
 
          <div className="system-status">
<span className="status-dot" />
 
            Systems Online
</div>
 
          <div className="stack-label">

            LangGraph · MCP · RAG
</div>
 
        </div>
 
      </aside>
 
 
      {/* ================================================= */}

      {/* MAIN */}

      {/* ================================================= */}
 
      <main className="main">
 
        <header className="topbar">
 
          <div>
 
            <div className="eyebrow">

              AI OPERATIONS CONSOLE
</div>
 
            <h2>

              Ask your business anything
</h2>
 
          </div>
 
 
          <div className="architecture-badge">
 
            <GitBranch size={16} />
 
            Multi-Agent Workflow
 
          </div>
 
        </header>
 
 
        {/* ================================================= */}

        {/* QUESTION */}

        {/* ================================================= */}
 
        <section className="question-panel">
 
          <div className="question-box">
 
            <textarea
              value={question}
              onChange={(e) =>
                setQuestion(
                  e.target.value
                )
              }
              onKeyDown={
                handleKeyDown
              }
              placeholder="Ask a business question..."
              rows={3}
              disabled={loading}
            />

            <div className="model-selector">
              <label>
                Model
              </label>
              <select
                value={modelProvider}
                onChange={(e) => {
                  const provider = e.target.value;
                  setModelProvider(provider);
                  if (provider === "gemini") {
                    setModelName("gemini-3.6-flash");
                  } else {
                    setModelName("qwen3.5:0.8b");
                  }
                }}
                disabled={loading}
              >
                <option value="gemini">
                  Gemini
                </option>
                <option value="ollama">
                  Ollama
                </option>
              </select>
            </div>
 
 
            <button
              className="send-button"
              onClick={askQuestion}
              disabled={
                loading ||
                !question.trim()
              }
            >
              {loading ? (
                "Running..."
              ) : (
              <>
              <Send size={16} />
                                Run Analysis
              </>
              )}
            </button>
          </div>
 
 
          <div className="example-questions">
 
            <button

              onClick={() =>

                setQuestion(

                  "What are our total sales?"

                )

              }
>

              Total sales
</button>
 
 
            <button

              onClick={() =>

                setQuestion(

                  "What is our refund policy?"

                )

              }
>

              Refund policy
</button>
 
 
            <button

              onClick={() =>

                setQuestion(

                  "Which customers qualify for Platinum membership and what benefits do they receive?"

                )

              }
>

              Platinum customers
</button>
 
          </div>
 
        </section>
 
 
        {/* ================================================= */}

        {/* WORKFLOW GRAPH */}

        {/* ================================================= */}
 
        <section className="workflow-section">
 
          <div className="section-heading">
 
            <div>
 
              <span>

                EXECUTION
</span>
 
              <h3>

                Agent Workflow
</h3>
 
            </div>
 
 
            {route && (
<div className="route-badge">

                ROUTE: {route}
</div>

            )}
 
          </div>
 
 
          <div className="workflow-flow-container">
 
            <ReactFlow

              nodes={flowNodes}

              edges={flowEdges}

              nodeTypes={nodeTypes}

              fitView

              fitViewOptions={{

                padding: 0.15,

              }}

              nodesDraggable={false}

              nodesConnectable={false}

              elementsSelectable={false}
>
 
              <Background

                gap={20}

                size={1}

              />
 
              <Controls

                showInteractive={false}

              />
 
            </ReactFlow>
 
          </div>
 
        </section>
 
 
        {/* ================================================= */}

        {/* DETAILS */}

        {/* ================================================= */}
 
        <section className="details-grid">
 
 
          {/* ================================================= */}

          {/* SQL INSPECTOR */}

          {/* ================================================= */}
 
          <div className="detail-card">
 
            <div className="card-title">
 
              <Database size={17} />
 
              SQL Inspector
 
            </div>
 
 
            <div className="code-panel">
 
              {sql ||

                "No SQL query executed yet."}
 
            </div>
 
 
            <div className="metric">
 
              <span>

                Rows Returned
</span>
 
              <strong>

                {databaseRows}
</strong>
 
            </div>
 
          </div>
 
 
          {/* ================================================= */}

          {/* MCP */}

          {/* ================================================= */}
 
          <div className="detail-card">
 
            <div className="card-title">
 
              <Wrench size={17} />
 
              MCP Tool
 
            </div>
 
 
            <div className="mcp-tool">
 
              <span className="tool-status">

                ●
</span>
 
 
              <div>
 
                <strong>

                  {mcpTool ||

                    "No MCP tool used"}
</strong>
 
                <span>

                  Read-only database access
</span>
 
              </div>
 
            </div>
 
          </div>
 
 
          {/* ================================================= */}

          {/* RAG */}

          {/* ================================================= */}
 
          <div className="detail-card">
 
            <div className="card-title">
 
              <FileText size={17} />
 
              RAG Sources
 
            </div>
 
 
            <div className="sources">
 
              {ragSources.length > 0 ? (
 
                ragSources.map(

                  (doc, index) => (
 
                    <div

                      className="source-item"

                      key={`${doc.document}-${index}`}
>
 
                      <FileText size={15} />
 
                      <div>
 
                        <strong>

                          {doc.document}
                        </strong>
 
                        <span>

                          Page {doc.page}
                        </span>
 
                      </div>
 
                    </div>
 
                  )

                )
 
              ) : (
 
                <span className="empty-text">

                  No documents retrieved.
                </span>
 
              )}
 
            </div>
 
          </div>
 
 
          {/* ================================================= */}

          {/* TIMELINE */}

          {/* ================================================= */}
 
          <div className="detail-card timeline-card">
 
            <div className="card-title">
 
              <GitBranch size={17} />
 
              Execution Timeline
 
            </div>
 
 
            <div className="timeline">
 
              {logs.length > 0 ? (
 
                logs.map(

                  (log, index) => (
 
                    <div

                      className="timeline-item"

                      key={`${log}-${index}`}
>
 
                      <span className="timeline-dot" />
 
                      <span>

                        {log}
</span>
 
                    </div>
 
                  )

                )
 
              ) : (
 
                <span className="empty-text">

                  Execution events will appear here.
</span>
 
              )}
 
            </div>
 
          </div>
 
        </section>
 
 
        {/* ================================================= */}

        {/* RAG CONTEXT */}

        {/* ================================================= */}
 
        {ragContext && (
 
          <section className="detail-card rag-context-card">
 
            <div className="card-title">
 
              <FileText size={17} />
 
              Retrieved Knowledge
 
            </div>
 
 
            <div className="code-panel">
 
              {ragContext}
 
            </div>
 
          </section>
 
        )}
 
 
        {/* ================================================= */}

        {/* FINAL ANSWER */}

        {/* ================================================= */}
 
        <section className="answer-panel">
 
          <div className="answer-title">
 
            <Sparkles size={18} />
 
            Final Answer
 
          </div>
 
 
          <div className="answer-content">
 
            {loading && !answer && (
 
              <div className="loading">
 
                Agents are working...
 
              </div>
 
            )}
 
 
            {answer && (
 
              <div className="answer-text">
 
                {answer}
 
              </div>
 
            )}
 
 
            {!loading && !answer && (
 
              <div className="empty-answer">
 
                Your final business answer will appear here.
 
              </div>
 
            )}
 
          </div>
 
        </section>
 
      </main>
 
    </div>

  );

}
 
 
export default App;
 