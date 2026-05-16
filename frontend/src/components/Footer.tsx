import { Link } from "react-router-dom";
import "./Footer.css";

export default function Footer() {
  const year = new Date().getFullYear();

  return (
    <footer className="site-footer">
      <div className="container footer-grid">
        <div className="footer-brand">
          <p className="footer-logo">
            Support<span>AI</span>
          </p>
          <p className="footer-tagline">
            Intelligent customer support powered by NLP, emotion detection, and
            self-improving AI.
          </p>
        </div>

        <div className="footer-links">
          <h4>Product</h4>
          <Link to="/">Home</Link>
          <Link to="/chat">Live Chat</Link>
          <Link to="/signup">Get Started</Link>
        </div>

        <div className="footer-links">
          <h4>Account</h4>
          <Link to="/login">Log in</Link>
          <Link to="/signup">Sign up</Link>
        </div>

        <div className="footer-links">
          <h4>Capabilities</h4>
          <span>Intent detection</span>
          <span>Emotion analysis</span>
          <span>Confidence scoring</span>
        </div>
      </div>

      <div className="container footer-bottom">
        <p>© {year} SupportAI. Built for smarter customer support.</p>
      </div>
    </footer>
  );
}
