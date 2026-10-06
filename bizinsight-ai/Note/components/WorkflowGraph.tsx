import {

  Background,

  Controls,

  Handle,

  Position,

  ReactFlow,

} from "@xyflow/react";
 
import "@xyflow/react/dist/style.css";
 
import {

  Bot,

  Database,

  FileText,

  Server,

  Sparkles,

} from "lucide-react";
 
 
// =========================================================

// Custom Node

// =========================================================
 
function WorkflowNode({

  data,

}) {

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
 
  const Icon =

    iconMap[data.type] || Bot;
 
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
 
        <span>

          {data.detail}
</span>
 
        <small>

          {data.status === "running"

            ? "Running..."

            : data.status === "completed"

              ? "Completed"

              : data.status === "error"

                ? "Error"

                : "Waiting"}
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
 
 
// =========================================================

// Node Types

// =========================================================
 
const nodeTypes = {

  workflow: WorkflowNode,

};
 
 
// =========================================================

// Workflow Graph

// =========================================================
 
export default function WorkflowGraph({

  route,

  agentStatus,

  sql,

  mcpTool,

  databaseRows,

  ragSources,

}) {
 
  const isSQL =

    route === "SQL" ||

    route === "BOTH";
 
  const isRAG =

    route === "RAG" ||

    route === "BOTH";
 
 
  // =======================================================

  // Helper

  // =======================================================
 
  const statusFor = (

    key,

    selected = false

  ) => {
 
    if (!selected) {

      return "waiting";

    }
 
    return (

      agentStatus?.[key] ||

      "waiting"

    );

  };
 
 
  // =======================================================

  // Nodes

  // =======================================================
 
  const nodes = [

    {

      id: "orchestrator",

      type: "workflow",

      position: {

        x: 430,

        y: 0,

      },

      data: {

        type: "orchestrator",

        label: "Orchestrator",

        detail: route

          ? `Route → ${route}`

          : "Waiting for request",

        status:

          agentStatus?.orchestrator ||

          "waiting",

      },

    },
 
 
    // -----------------------------------------------------

    // SQL Branch

    // -----------------------------------------------------
 
    {

      id: "sql_agent",

      type: "workflow",

      position: {

        x: 80,

        y: 180,

      },

      data: {

        type: "sql_agent",

        label: "SQL Agent",

        detail: isSQL

          ? sql

            ? "SQL generated"

            : "Analyzing structured data"

          : "Not selected",

        status: statusFor(

          "sql_agent",

          isSQL

        ),

      },

    },
 
    {

      id: "mcp",

      type: "workflow",

      position: {

        x: 80,

        y: 350,

      },

      data: {

        type: "mcp",

        label: "MCP Server",

        detail: mcpTool

          ? mcpTool

          : "Waiting for SQL tool",

        status: isSQL && mcpTool

          ? "completed"

          : "waiting",

      },

    },
 
    {

      id: "sqlite",

      type: "workflow",

      position: {

        x: 80,

        y: 520,

      },

      data: {

        type: "sqlite",

        label: "SQLite",

        detail:

          databaseRows > 0

            ? `${databaseRows} rows returned`

            : "Business database",

        status:

          isSQL && databaseRows > 0

            ? "completed"

            : "waiting",

      },

    },
 
 
    // -----------------------------------------------------

    // RAG Branch

    // -----------------------------------------------------
 
    {

      id: "rag_agent",

      type: "workflow",

      position: {

        x: 650,

        y: 180,

      },

      data: {

        type: "rag_agent",

        label: "RAG Agent",

        detail: isRAG

          ? ragSources.length

            ? `${ragSources.length} sources`

            : "Searching knowledge base"

          : "Not selected",

        status: statusFor(

          "rag_agent",

          isRAG

        ),

      },

    },
 
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

          isRAG && ragSources.length > 0

            ? "completed"

            : "waiting",

      },

    },
 
    {

      id: "documents",

      type: "workflow",

      position: {

        x: 650,

        y: 520,

      },

      data: {

        type: "documents",

        label: "Knowledge Base",

        detail:

          ragSources.length > 0

            ? ragSources[0].document

            : "Company PDFs",

        status:

          isRAG && ragSources.length > 0

            ? "completed"

            : "waiting",

      },

    },
 
 
    // -----------------------------------------------------

    // Response

    // -----------------------------------------------------
 
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

          agentStatus?.response_agent ===

          "completed"

            ? "Answer synthesized"

            : "Waiting for evidence",

        status:

          agentStatus?.response_agent ||

          "waiting",

      },

    },

  ];
 
 
  // =======================================================

  // Edges

  // =======================================================
 
  const edges = [

    {

      id: "orchestrator-sql",

      source: "orchestrator",

      target: "sql_agent",

      animated: isSQL,

      className: isSQL

        ? "flow-edge-active"

        : "",

    },
 
    {

      id: "sql-mcp",

      source: "sql_agent",

      target: "mcp",

      animated:

        isSQL &&

        !!mcpTool,

      className:

        isSQL && mcpTool

          ? "flow-edge-active"

          : "",

    },
 
    {

      id: "mcp-sqlite",

      source: "mcp",

      target: "sqlite",

      animated:

        isSQL &&

        databaseRows > 0,

      className:

        isSQL && databaseRows > 0

          ? "flow-edge-active"

          : "",

    },
 
    {

      id: "sqlite-response",

      source: "sqlite",

      target: "response_agent",

      animated:

        isSQL &&

        databaseRows > 0,

      className:

        isSQL && databaseRows > 0

          ? "flow-edge-active"

          : "",

    },
 
 
    {

      id: "orchestrator-rag",

      source: "orchestrator",

      target: "rag_agent",

      animated: isRAG,

      className: isRAG

        ? "flow-edge-active"

        : "",

    },
 
    {

      id: "rag-chroma",

      source: "rag_agent",

      target: "chroma",

      animated:

        isRAG &&

        ragSources.length > 0,

      className:

        isRAG && ragSources.length > 0

          ? "flow-edge-active"

          : "",

    },
 
    {

      id: "chroma-documents",

      source: "chroma",

      target: "documents",

      animated:

        isRAG &&

        ragSources.length > 0,

      className:

        isRAG && ragSources.length > 0

          ? "flow-edge-active"

          : "",

    },
 
    {

      id: "documents-response",

      source: "documents",

      target: "response_agent",

      animated:

        isRAG &&

        ragSources.length > 0,

      className:

        isRAG && ragSources.length > 0

          ? "flow-edge-active"

          : "",

    },

  ];
 
 
  return (
<div className="workflow-flow-container">
 
      <ReactFlow

        nodes={nodes}

        edges={edges}

        nodeTypes={nodeTypes}

        fitView

        fitViewOptions={{

          padding: 0.18,

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

  );

}
 