import { Cpu } from "lucide-react";

export default function ModelSelector({ provider, model, onChange, disabled }) {
  return (
    <div className="model-selector">
      <div className="model-label"><Cpu size={14} /> Model</div>
      <select
        value={provider}
        disabled={disabled}
        onChange={(event) => onChange(event.target.value)}
      >
        <option value="gemini">Gemini · {model}</option>
        <option value="ollama">Ollama · {model}</option>
      </select>
    </div>
  );
}