import { FormEvent, useEffect, useRef, useState } from "react";
import { api } from "../api/client";
import { useAuth } from "../context/AuthContext";
import "./Chat.css";

interface Message {
  id: number;
  role: "user" | "bot";
  text: string;
  intent?: string;
  emotion?: string;
  confidence?: string;
}

export default function Chat() {
  const { username } = useAuth();
  const [messages, setMessages] = useState<Message[]>([
    {
      id: 0,
      role: "bot",
      text: `Hi${username ? ` ${username}` : ""}! I'm SupportAI. Ask me about orders, refunds, payments, or anything else.`,
    },
  ]);
  const [input, setInput] = useState("");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");
  const bottomRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    bottomRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages]);

  async function handleSubmit(e: FormEvent) {
    e.preventDefault();
    const text = input.trim();
    if (!text || loading) return;

    setError("");
    setInput("");
    const userMsg: Message = {
      id: Date.now(),
      role: "user",
      text,
    };
    setMessages((prev) => [...prev, userMsg]);
    setLoading(true);

    try {
      const data = await api.chat(text);
      setMessages((prev) => [
        ...prev,
        {
          id: Date.now() + 1,
          role: "bot",
          text: data.response,
          intent: data.intent,
          emotion: data.emotion,
          confidence: data.confidence,
        },
      ]);
    } catch (err) {
      setError(err instanceof Error ? err.message : "Failed to send message.");
    } finally {
      setLoading(false);
    }
  }

  function clearChat() {
    setMessages([
      {
        id: 0,
        role: "bot",
        text: "Conversation cleared. How can I help you today?",
      },
    ]);
    setError("");
  }

  return (
    <div className="chat-page container">
      <header className="chat-header">
        <div>
          <h1>Support Chat</h1>
          <p>Logged in as <strong>{username}</strong></p>
        </div>
        <button type="button" className="btn btn-ghost btn-sm" onClick={clearChat}>
          Clear chat
        </button>
      </header>

      <div className="chat-panel">
        <div className="chat-messages" role="log" aria-live="polite">
          {messages.map((msg) => (
            <article
              key={msg.id}
              className={`chat-bubble ${msg.role}`}
            >
              <span className="bubble-label">
                {msg.role === "user" ? "You" : "SupportAI"}
              </span>
              <p>{msg.text}</p>
              {msg.role === "bot" && msg.intent && (
                <ul className="meta-tags">
                  <li>Intent: {msg.intent}</li>
                  <li>Emotion: {msg.emotion}</li>
                  <li>Confidence: {msg.confidence}</li>
                </ul>
              )}
            </article>
          ))}
          {loading && (
            <article className="chat-bubble bot typing">
              <span className="bubble-label">SupportAI</span>
              <p>Thinking…</p>
            </article>
          )}
          <div ref={bottomRef} />
        </div>

        {error && <p className="chat-error">{error}</p>}

        <form className="chat-input-row" onSubmit={handleSubmit}>
          <input
            type="text"
            placeholder="Type your message… e.g. Where is my order?"
            value={input}
            onChange={(e) => setInput(e.target.value)}
            disabled={loading}
            aria-label="Message"
          />
          <button
            type="submit"
            className="btn btn-primary"
            disabled={loading || !input.trim()}
          >
            Send
          </button>
        </form>
      </div>
    </div>
  );
}
