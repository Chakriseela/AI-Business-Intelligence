import { Sparkles } from "lucide-react";
import ReactMarkdown from "react-markdown";

export default function FinalAnswer({ answer, loading }) {
  return (
    <section className="answer-panel">
      <div className="answer-title"><Sparkles size={18} /> Final Answer</div>
      <div className="answer-content">
        {loading && !answer && <div className="loading">Agents are working...</div>}
        {answer && <div className="answer-text"><ReactMarkdown>{answer}</ReactMarkdown></div>}
        {!loading && !answer && <div className="empty-answer">Your final business answer will appear here.</div>}
      </div>
    </section>
  );
}
