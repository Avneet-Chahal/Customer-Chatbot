import { Navigate } from "react-router-dom";
import { useAuth } from "../context/AuthContext";

export default function ProtectedRoute({
  children,
}: {
  children: React.ReactNode;
}) {
  const { username, loading } = useAuth();

  if (loading) {
    return (
      <div className="page-center">
        <p className="loading-text">Loading…</p>
      </div>
    );
  }

  if (!username) {
    return <Navigate to="/login" replace />;
  }

  return children;
}
