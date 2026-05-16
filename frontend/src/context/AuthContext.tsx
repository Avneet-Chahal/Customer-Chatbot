import {
  createContext,
  useCallback,
  useContext,
  useEffect,
  useMemo,
  useState,
  type ReactNode,
} from "react";
import { api, clearToken, getToken, setToken } from "../api/client";

interface AuthContextValue {
  username: string | null;
  loading: boolean;
  login: (username: string, password: string) => Promise<void>;
  signup: (username: string, password: string) => Promise<void>;
  logout: () => void;
}

const AuthContext = createContext<AuthContextValue | null>(null);

export function AuthProvider({ children }: { children: ReactNode }) {
  const [username, setUsername] = useState<string | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const token = getToken();
    if (!token) {
      setLoading(false);
      return;
    }

    api
      .me()
      .then((data) => setUsername(data.username))
      .catch(() => clearToken())
      .finally(() => setLoading(false));
  }, []);

  const login = useCallback(async (user: string, password: string) => {
    const data = await api.login(user, password);
    setToken(data.token);
    setUsername(data.username);
  }, []);

  const signup = useCallback(async (user: string, password: string) => {
    const data = await api.signup(user, password);
    setToken(data.token);
    setUsername(data.username);
  }, []);

  const logout = useCallback(() => {
    clearToken();
    setUsername(null);
  }, []);

  const value = useMemo(
    () => ({ username, loading, login, signup, logout }),
    [username, loading, login, signup, logout]
  );

  return (
    <AuthContext.Provider value={value}>{children}</AuthContext.Provider>
  );
}

export function useAuth() {
  const ctx = useContext(AuthContext);
  if (!ctx) throw new Error("useAuth must be used within AuthProvider");
  return ctx;
}
