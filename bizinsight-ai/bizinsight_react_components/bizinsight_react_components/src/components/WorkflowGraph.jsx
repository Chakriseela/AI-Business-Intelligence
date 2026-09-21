import { useMemo } from "react";
import { ReactFlow, Background, Controls, Handle, Position } from "@xyflow/react";
import { Bot, Database, FileText, Server, Sparkles } from "lucide-react";

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
    <div className={`workflow-flow-node status-${data.status}`}>
      <Handle type="target" position={Position.Top} className="flow-handle" />
      <div className="flow-node-icon"><Icon size={17} /></div>
      <div className="flow-node-content">
        <strong>{data.label}</strong>
        <span title={data.detail}>{data.detail}</span>
        <small>
          {data.status === "running" ? "Running..." :
           data.status === "completed" ? "Completed" :
           data.status === "error" ? "Error" : "Waiting"}
        </small>
      </div>
      <Handle type="source" position={Position.Bottom} className="flow-handle" />
    </div>
  );
}

const nodeTypes = { workflow: WorkflowNode };

export default function WorkflowGraph({ route, agentStatus, sql, mcpTool, databaseRows, ragSources }) {
  const hasSQL = route === "SQL" || route === "BOTH";
  const hasRAG = route === "RAG" || route === "BOTH";

  const nodes = useMemo(() => [
    { id: "orchestrator", type: "workflow", position: { x: 410, y: 15 }, data: {
      type: "orchestrator", label: "Orchestrator", detail: route ? `Route → ${route}` : "Waiting for request",
      status: agentStatus.orchestrator,
    }},
    { id: "sql_agent", type: "workflow", position: { x: 60, y: 180 }, data: {
      type: "sql_agent", label: "SQL Agent", detail: hasSQL ? (sql ? "SQL generated" : "Analyzing structured data") : "Not selected",
      status: hasSQL ? agentStatus.sql_agent : "waiting",
    }},
    { id: "mcp", type: "workflow", position: { x: 60, y: 355 }, data: {
      type: "mcp", label: "MCP Server", detail: mcpTool || "Waiting for SQL tool",
      status: hasSQL && mcpTool ? "completed" : "waiting",
    }},
    { id: "sqlite", type: "workflow", position: { x: 60, y: 530 }, data: {
      type: "sqlite", label: "SQLite", detail: databaseRows > 0 ? `${databaseRows} rows returned` : "Business database",
      status: hasSQL && databaseRows > 0 ? "completed" : "waiting",
    }},
    { id: "rag_agent", type: "workflow", position: { x: 650, y: 180 }, data: {
      type: "rag_agent", label: "RAG Agent", detail: hasRAG ? (ragSources.length ? `${ragSources.length} sources` : "Searching knowledge base") : "Not selected",
      status: hasRAG ? agentStatus.rag_agent : "waiting",
    }},
    { id: "chroma", type: "workflow", position: { x: 650, y: 355 }, data: {
      type: "chroma", label: "ChromaDB", detail: ragSources.length ? `${ragSources.length} documents` : "Vector search",
      status: hasRAG && ragSources.length ? "completed" : "waiting",
    }},
    { id: "documents", type: "workflow", position: { x: 650, y: 530 }, data: {
      type: "documents", label: "Knowledge Base", detail: ragSources[0]?.document || "Company PDFs",
      status: hasRAG && ragSources.length ? "completed" : "waiting",
    }},
    { id: "response_agent", type: "workflow", position: { x: 410, y: 705 }, data: {
      type: "response_agent", label: "Response Agent", detail: agentStatus.response_agent === "completed" ? "Answer synthesized" : "Waiting for evidence",
      status: agentStatus.response_agent,
    }},
  ], [route, agentStatus, sql, mcpTool, databaseRows, ragSources, hasSQL, hasRAG]);

  const edges = useMemo(() => [
    { id: "orchestrator-sql", source: "orchestrator", target: "sql_agent", animated: hasSQL, className: hasSQL ? "flow-edge-active" : "" },
    { id: "sql-mcp", source: "sql_agent", target: "mcp", animated: hasSQL && !!mcpTool, className: hasSQL && mcpTool ? "flow-edge-active" : "" },
    { id: "mcp-sqlite", source: "mcp", target: "sqlite", animated: hasSQL && databaseRows > 0, className: hasSQL && databaseRows > 0 ? "flow-edge-active" : "" },
    { id: "sqlite-response", source: "sqlite", target: "response_agent", animated: hasSQL && databaseRows > 0, className: hasSQL && databaseRows > 0 ? "flow-edge-active" : "" },
    { id: "orchestrator-rag", source: "orchestrator", target: "rag_agent", animated: hasRAG, className: hasRAG ? "flow-edge-active" : "" },
    { id: "rag-chroma", source: "rag_agent", target: "chroma", animated: hasRAG && ragSources.length > 0, className: hasRAG && ragSources.length > 0 ? "flow-edge-active" : "" },
    { id: "chroma-documents", source: "chroma", target: "documents", animated: hasRAG && ragSources.length > 0, className: hasRAG && ragSources.length > 0 ? "flow-edge-active" : "" },
    { id: "documents-response", source: "documents", target: "response_agent", animated: hasRAG && ragSources.length > 0, className: hasRAG && ragSources.length > 0 ? "flow-edge-active" : "" },
  ], [hasSQL, hasRAG, mcpTool, databaseRows, ragSources]);

  return (
    <div className="workflow-flow-container">
      <ReactFlow
        nodes={nodes}
        edges={edges}
        nodeTypes={nodeTypes}
        fitView
        fitViewOptions={{ padding: 0.12 }}
        nodesDraggable={false}
        nodesConnectable={false}
        elementsSelectable={false}
      >
        <Background gap={20} size={1} />
        <Controls showInteractive={false} />
      </ReactFlow>
    </div>
  );
}
