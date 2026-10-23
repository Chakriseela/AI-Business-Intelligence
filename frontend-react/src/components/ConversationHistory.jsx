
import { useEffect, useRef } from "react";
import { Bot, User, LoaderCircle } from "lucide-react";
import ReactMarkdown from "react-markdown";
// import Markdown from 'markdown-to-jsx';


export default function ConversationHistory({
  messages = [],
  loading = false,
}) {
  const bottomRef = useRef(null);

  useEffect(() => {
    bottomRef.current?.scrollIntoView({
      behavior: "smooth",
    });
  }, [messages, loading]);

  if (messages.length === 0 && !loading) {
    return (
      <section className="conversation-history empty">
        <h3>BizInsight AI</h3>
        <p>Ask a question to start your conversation.</p>
      </section>
    );
  }

  return (
    <section className="conversation-history">
      {messages.map((message, index) => (
        <div
          className="conversation-turn"
          key={message.id ?? index}
        >
          {/* User question */}
          <div className="conversation-message user-message">
            <div className="conversation-avatar user-avatar">
              <User size={18} />
            </div>

            <div className="conversation-message-content">
              <strong>You</strong>
              <p>{message.question}</p>
            </div>
          </div>

          {/* Assistant answer */}
          <div className="conversation-message assistant-message">
            <div className="conversation-avatar assistant-avatar">
              <Bot size={18} />
            </div>

            <div className="conversation-message-content">
              <strong>BizInsight AI</strong>
                <ReactMarkdown>
                    {/* <p className="conversation-answer"> */}
                        {message.answer ||
                        "No answer was saved for this turn."}
                    {/* </p> */}
                </ReactMarkdown>
            </div>
          </div>
        </div>
      ))}

      {/* Loading indicator */}
      {loading && (
        <div className="conversation-message assistant-message">
          <div className="conversation-avatar assistant-avatar">
            <Bot size={18} />
          </div>

          <div className="conversation-message-content">
            <strong>BizInsight AI</strong>
            <p className="conversation-answer">
              <LoaderCircle
                className="conversation-loading-icon"
                size={16}
              />
              {" "}Analyzing your question...
            </p>
          </div>
        </div>
      )}

      <div ref={bottomRef} />
    </section>
  );
}
