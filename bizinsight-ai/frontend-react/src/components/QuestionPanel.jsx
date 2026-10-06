import { Send, Sparkles } from "lucide-react";
import ModelSelector from "./ModelSelector";

export default function QuestionPanel({
  question,
  setQuestion,
  onSubmit,
  loading,
  modelProvider,
  modelName,
  onModelChange,
}) {
  const examples = [
    "What are our total sales?",
    "What is our refund policy?",
    "Which customers qualify for Platinum membership and what benefits do they receive?",
  ];

  return (
    <section className="question-panel">
      <div className="question-box">
        <div className="prompt-hint"><Sparkles size={14} /> Business Query</div>
        <textarea
          value={question}
          onChange={(event) => setQuestion(event.target.value)}
          onKeyDown={(event) => {
            if (event.key === "Enter" && !event.shiftKey) {
              event.preventDefault();
              onSubmit();
            }
          }}
          placeholder="Ask a business question..."
          rows={3}
          disabled={loading}
        />

        <div className="question-actions">
          <ModelSelector
            provider={modelProvider}
            model={modelName}
            onChange={onModelChange}
            disabled={loading}
          />

          <button
            className="send-button"
            onClick={onSubmit}
            disabled={loading || !question.trim()}
          >
            {loading ? "Running..." : <><Send size={16} /> Run Analysis</>}
          </button>
        </div>
      </div>

      <div className="example-questions">
        {examples.map((example) => (
          <button key={example} onClick={() => setQuestion(example)}>
            {example.length > 50 ? "Platinum customers" : example.replace("What are our ", "").replace("What is our ", "")}
          </button>
        ))}
      </div>
    </section>
  );
}