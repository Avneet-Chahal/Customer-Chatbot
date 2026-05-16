import { Link } from "react-router-dom";
import FlashCards from "../components/FlashCards";
import { useAuth } from "../context/AuthContext";
import "./Home.css";

export default function Home() {
  const { username } = useAuth();

  return (
    <>
      <section className="hero">
        <div className="container hero-inner">
          <div className="hero-content">
            <p className="hero-badge">AI Customer Support</p>
            <h1 className="display-title hero-title">
              Support that understands your customers
            </h1>
            <p className="hero-desc">
              SupportAI is a self-improving chatbot that detects intent and
              emotion, scores its own confidence, and learns from every
              conversation — so your team can focus on what matters most.
            </p>
            <div className="hero-cta">
              {username ? (
                <Link to="/chat" className="btn btn-primary">
                  Open Chat →
                </Link>
              ) : (
                <>
                  <Link to="/signup" className="btn btn-primary">
                    Get started free
                  </Link>
                  <Link to="/login" className="btn btn-ghost">
                    Log in
                  </Link>
                </>
              )}
            </div>
            <ul className="hero-stats">
              <li>
                <strong>6+</strong>
                <span>Intent categories</span>
              </li>
              <li>
                <strong>4</strong>
                <span>Emotion states</span>
              </li>
              <li>
                <strong>24/7</strong>
                <span>Availability</span>
              </li>
            </ul>
          </div>

          <div className="hero-visual" aria-hidden="true">
            <div className="chat-preview">
              <div className="preview-header">
                <span className="dot" />
                <span className="dot" />
                <span className="dot" />
                <span>SupportAI</span>
              </div>
              <div className="preview-messages">
                <div className="preview-msg user">
                  Where is my order #4821?
                </div>
                <div className="preview-msg bot">
                  I can help track that. Your package is out for delivery
                  today.
                  <small>Intent: order_status · Confidence: High</small>
                </div>
                <div className="preview-msg user">
                  Thanks, that helps!
                </div>
                <div className="preview-msg bot">
                  Glad I could help! Anything else?
                  <small>Emotion: happy</small>
                </div>
              </div>
            </div>
          </div>
        </div>
      </section>

      <FlashCards />

      <section className="cta-band">
        <div className="container cta-inner">
          <h2 className="display-title cta-title">Ready to try the chatbot?</h2>
          <p>
            Create an account and start a conversation — ask about orders,
            refunds, or payments.
          </p>
          <Link
            to={username ? "/chat" : "/signup"}
            className="btn btn-primary"
          >
            {username ? "Go to chat" : "Sign up now"}
          </Link>
        </div>
      </section>
    </>
  );
}
