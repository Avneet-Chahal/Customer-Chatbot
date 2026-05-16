import { Link, NavLink } from "react-router-dom";
import { useAuth } from "../context/AuthContext";
import { useTheme } from "../context/ThemeContext";
import "./Header.css";

export default function Header() {
  const { username, logout } = useAuth();
  const { theme, toggleTheme } = useTheme();

  return (
    <header className="site-header">
      <div className="container header-inner">
        <Link to="/" className="logo">
          Support<span className="logo-accent">AI</span>
        </Link>

        <nav className="nav-links" aria-label="Main">
          <NavLink to="/" end>
            Home
          </NavLink>
          {username && (
            <NavLink to="/chat">Chat</NavLink>
          )}
        </nav>

        <div className="header-actions">
          <button
            type="button"
            className="theme-toggle btn btn-ghost btn-sm"
            onClick={toggleTheme}
            aria-label={`Switch to ${theme === "light" ? "dark" : "light"} mode`}
          >
            {theme === "light" ? "🌙" : "☀️"}
          </button>

          {username ? (
            <>
              <span className="user-badge">Hi, {username}</span>
              <button
                type="button"
                className="btn btn-ghost btn-sm"
                onClick={logout}
              >
                Log out
              </button>
            </>
          ) : (
            <>
              <Link to="/login" className="btn btn-ghost btn-sm">
                Log in
              </Link>
              <Link to="/signup" className="btn btn-primary btn-sm">
                Sign up
              </Link>
            </>
          )}
        </div>
      </div>
    </header>
  );
}
