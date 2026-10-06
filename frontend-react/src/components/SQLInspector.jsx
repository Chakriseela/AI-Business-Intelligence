import { Database } from "lucide-react";
import InspectorCard from "./InspectorCard";

export default function SQLInspector({ sql, databaseRows, databaseData }) {
  return (
    <InspectorCard icon={<Database size={17} />} title="SQL Inspector">
      <div className="code-panel">{sql || "No SQL query executed yet."}</div>
      <div className="metric"><span>Rows Returned</span><strong>{databaseRows}</strong></div>
      {databaseData?.length > 0 && (
        <details className="inspector-details">
          <summary>View returned data</summary>
          <pre>{JSON.stringify(databaseData, null, 2)}</pre>
        </details>
      )}
    </InspectorCard>
  );
}