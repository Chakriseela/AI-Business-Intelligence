import { useEffect, useState } from "react";
import { MessageSquare, RefreshCw } from "lucide-react";

const API_BASE_URL = "http://127.0.0.1:8000";

export default function ChatHistory({
  activeThreadId,
  onSelectConversation,
  refreshKey = 0,
}) {
  const [conversations, setConversations] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  useEffect(() => {
    const controller = new AbortController();

    async function fetchConversations() {
      try {
        setLoading(true);
        setError("");

        const response = await fetch(
          `${API_BASE_URL}/chat/conversations`,
          { signal: controller.signal }
        );

        if (!response.ok) {
          throw new Error(
            `Failed to load conversations (${response.status})`
          );
        }

        const data = await response.json();

        setConversations(
          Array.isArray(data.conversations)
            ? data.conversations
            : []
        );
      } catch (err) {
        if (err.name !== "AbortError") {
          setError(err.message || "Unable to load conversations.");
        }
      } finally {
        if (!controller.signal.aborted) {
          setLoading(false);
        }
      }
    }

    fetchConversations();

    return () => controller.abort();
  }, [refreshKey]);

  return (
    <div className="chat-history">
      <div className="chat-history-header">
        <h3>Recent Conversations</h3>

        <button
          type="button"
          className="chat-history-refresh"
          title="Refresh conversations"
          onClick={() => {
            // Refresh is handled by changing refreshKey from the parent.
            // The parent can also increment refreshKey after a new chat.
            window.location.reload();
          }}
        >
          <RefreshCw size={15} />
        </button>
      </div>

      {loading && (
        <p className="chat-history-message">
          Loading conversations...
        </p>
      )}

      {!loading && error && (
        <div className="chat-history-error">
          <p>{error}</p>
          <p>
            Check that the backend and conversation-list endpoint
            are available.
          </p>
        </div>
      )}

      {!loading && !error && conversations.length === 0 && (
        <p className="chat-history-message">
          No previous conversations.
        </p>
      )}

      {!loading && !error && conversations.length > 0 && (
        <div className="chat-history-list">
          {conversations.map((conversation) => {
            const isActive =
              conversation.thread_id === activeThreadId;

            return (
              <button
                key={conversation.thread_id}
                type="button"
                className={`chat-history-item ${
                  isActive ? "active" : ""
                }`}
                onClick={() =>
                  onSelectConversation(conversation.thread_id)
                }
                title={conversation.title || "Untitled conversation"}
              >
                <MessageSquare
                  size={16}
                  className="chat-history-icon"
                />

                <span className="chat-history-title">
                  {conversation.title || "Untitled conversation"}
                </span>
              </button>
            );
          })}
        </div>
      )}
    </div>
  );
}
