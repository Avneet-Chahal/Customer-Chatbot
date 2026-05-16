const TOKEN_KEY = "supportai_token";

export function getToken(): string | null {
  return localStorage.getItem(TOKEN_KEY);
}

export function setToken(token: string) {
  localStorage.setItem(TOKEN_KEY, token);
}

export function clearToken() {
  localStorage.removeItem(TOKEN_KEY);
}

async function request<T>(
  path: string,
  options: RequestInit = {}
): Promise<T> {
  const headers: Record<string, string> = {
    "Content-Type": "application/json",
    ...(options.headers as Record<string, string>),
  };

  const token = getToken();
  if (token) {
    headers.Authorization = `Bearer ${token}`;
  }

  const res = await fetch(path, { ...options, headers });
  const data = await res.json().catch(() => ({}));

  if (!res.ok) {
    throw new Error(data.error || "Something went wrong.");
  }

  return data as T;
}

export const api = {
  signup: (username: string, password: string) =>
    request<{ token: string; username: string; message: string }>(
      "/api/auth/signup",
      {
        method: "POST",
        body: JSON.stringify({ username, password }),
      }
    ),

  login: (username: string, password: string) =>
    request<{ token: string; username: string; message: string }>(
      "/api/auth/login",
      {
        method: "POST",
        body: JSON.stringify({ username, password }),
      }
    ),

  me: () => request<{ username: string }>("/api/auth/me"),

  chat: (message: string) =>
    request<{
      response: string;
      intent: string;
      emotion: string;
      confidence: string;
      failed: boolean;
    }>("/api/chat", {
      method: "POST",
      body: JSON.stringify({ message }),
    }),
};
