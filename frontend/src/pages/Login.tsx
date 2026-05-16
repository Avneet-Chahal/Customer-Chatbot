import { FormEvent, useState } from "react";
import { Link, useNavigate } from "react-router-dom";
import { useAuth } from "../context/AuthContext";

export default function Login() {
  const { login } = useAuth();
  const navigate = useNavigate();
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");
  const [submitting, setSubmitting] = useState(false);

  async function handleSubmit(e: FormEvent) {
    e.preventDefault();
    setError("");
    setSubmitting(true);
    try {
      await login(username, password);
      navigate("/chat");
    } catch (err) {
      setError(err instanceof Error ? err.message : "Login failed.");
    } finally {
      setSubmitting(false);
    }
  }

  return (
    <div className="page-center">
      <form className="form-card" onSubmit={handleSubmit}>
        <h1>Welcome back</h1>
        <p className="subtitle">Log in to continue your support conversations.</p>

        {error && <div className="form-error">{error}</div>}

        <div className="form-group">
          <label htmlFor="username">Username</label>
          <input
            id="username"
            type="text"
            autoComplete="username"
            value={username}
            onChange={(e) => setUsername(e.target.value)}
            required
            minLength={3}
          />
        </div>

        <div className="form-group">
          <label htmlFor="password">Password</label>
          <input
            id="password"
            type="password"
            autoComplete="current-password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            required
            minLength={6}
          />
        </div>

        <button
          type="submit"
          className="btn btn-primary"
          style={{ width: "100%" }}
          disabled={submitting}
        >
          {submitting ? "Logging in…" : "Log in"}
        </button>

        <p className="form-footer">
          Don&apos;t have an account? <Link to="/signup">Sign up</Link>
        </p>
      </form>
    </div>
  );
}
