import "./FlashCards.css";

const cards = [
  {
    icon: "🎯",
    title: "Smart Intent Detection",
    description:
      "Understands what customers need — order tracking, refunds, payments, and more — using NLP and TF-IDF similarity.",
  },
  {
    icon: "💬",
    title: "Emotion-Aware Replies",
    description:
      "Detects happy, neutral, confused, or frustrated tones so responses stay empathetic and on-brand.",
  },
  {
    icon: "⚡",
    title: "Instant 24/7 Support",
    description:
      "No wait times. Your AI assistant is always on, ready to help customers the moment they reach out.",
  },
  {
    icon: "📊",
    title: "Confidence Engine",
    description:
      "Scores every answer so the bot knows when it's sure — and when a human should step in.",
  },
  {
    icon: "🔄",
    title: "Self-Improving System",
    description:
      "Logs low-confidence and failed conversations to continuously improve support quality over time.",
  },
  {
    icon: "🔒",
    title: "Secure Accounts",
    description:
      "Sign up to keep your chat history tied to your profile, with conversations stored safely in SQLite.",
  },
];

export default function FlashCards() {
  return (
    <section className="flash-section" id="features">
      <div className="container">
        <div className="section-header">
          <p className="eyebrow">Why SupportAI</p>
          <h2 className="display-title section-title">
            Everything you need for modern customer support
          </h2>
          <p className="section-subtitle">
            A self-improving AI chatbot built with intent detection, emotion
            analysis, and real conversation logging — not just canned replies.
          </p>
        </div>

        <div className="flash-grid">
          {cards.map((card) => (
            <article key={card.title} className="flash-card">
              <span className="flash-icon" aria-hidden="true">
                {card.icon}
              </span>
              <h3>{card.title}</h3>
              <p>{card.description}</p>
            </article>
          ))}
        </div>
      </div>
    </section>
  );
}
