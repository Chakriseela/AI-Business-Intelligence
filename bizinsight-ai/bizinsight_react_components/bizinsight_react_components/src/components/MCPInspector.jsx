import { Wrench } from "lucide-react";
import InspectorCard from "./InspectorCard";

export default function MCPInspector({ mcpTool }) {
  return (
    <InspectorCard icon={<Wrench size={17} />} title="MCP Tool">
      <div className="mcp-tool">
        <span className="tool-status">●</span>
        <div>
          <strong>{mcpTool || "No MCP tool used"}</strong>
          <span>Read-only database access</span>
        </div>
      </div>
    </InspectorCard>
  );
}
