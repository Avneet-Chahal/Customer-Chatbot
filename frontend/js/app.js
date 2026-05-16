const TOKEN_KEY = "supportai_token";
const USER_KEY = "supportai_username";

function getToken() {
  return localStorage.getItem(TOKEN_KEY);
}

function setAuth(token, username) {
  localStorage.setItem(TOKEN_KEY, token);
  localStorage.setItem(USER_KEY, username);
}

function clearAuth() {
  localStorage.removeItem(TOKEN_KEY);
  localStorage.removeItem(USER_KEY);
}

function getUsername() {
  return localStorage.getItem(USER_KEY);
}

function initTheme() {
  const stored = localStorage.getItem("supportai_theme");
  const theme =
    stored === "light" || stored === "dark"
      ? stored
      : window.matchMedia("(prefers-color-scheme: dark)").matches
        ? "dark"
        : "light";
  document.documentElement.setAttribute("data-theme", theme);

  const btn = document.getElementById("theme-toggle");
  if (btn) {
    btn.textContent = theme === "light" ? "🌙" : "☀️";
    btn.addEventListener("click", () => {
      const next = document.documentElement.getAttribute("data-theme") === "light" ? "dark" : "light";
      document.documentElement.setAttribute("data-theme", next);
      localStorage.setItem("supportai_theme", next);
      btn.textContent = next === "light" ? "🌙" : "☀️";
    });
  }
}

function initHeader() {
  const username = getUsername();
  const token = getToken();

  document.querySelectorAll(".auth-guest").forEach((el) => {
    el.classList.toggle("hidden", !!(token && username));
  });
  document.querySelectorAll(".auth-user").forEach((el) => {
    el.classList.toggle("hidden", !(token && username));
  });

  const badge = document.getElementById("user-badge");
  if (badge && username) badge.textContent = `Hi, ${username}`;

  const logoutBtn = document.getElementById("logout-btn");
  if (logoutBtn) {
    logoutBtn.addEventListener("click", () => {
      clearAuth();
      window.location.href = "/";
    });
  }
}

async function api(path, options = {}) {
  const headers = { "Content-Type": "application/json" };
  const token = getToken();
  if (token) headers.Authorization = `Bearer ${token}`;

  const res = await fetch(path, { ...options, headers });
  const data = await res.json().catch(() => ({}));
  if (!res.ok) throw new Error(data.error || "Something went wrong.");
  return data;
}

function initLoginForm() {
  const form = document.getElementById("login-form");
  if (!form) return;

  form.addEventListener("submit", async (e) => {
    e.preventDefault();
    const errorEl = document.getElementById("form-error");
    const btn = form.querySelector('button[type="submit"]');
    errorEl.classList.add("hidden");
    btn.disabled = true;

    try {
      const fd = new FormData(form);
      const data = await api("/api/auth/login", {
        method: "POST",
        body: JSON.stringify({
          username: fd.get("username"),
          password: fd.get("password"),
        }),
      });
      setAuth(data.token, data.username);
      window.location.href = "/chat.html";
    } catch (err) {
      errorEl.textContent = err.message;
      errorEl.classList.remove("hidden");
    } finally {
      btn.disabled = false;
    }
  });
}

function initSignupForm() {
  const form = document.getElementById("signup-form");
  if (!form) return;

  form.addEventListener("submit", async (e) => {
    e.preventDefault();
    const errorEl = document.getElementById("form-error");
    const btn = form.querySelector('button[type="submit"]');
    errorEl.classList.add("hidden");

    const fd = new FormData(form);
    if (fd.get("password") !== fd.get("confirm")) {
      errorEl.textContent = "Passwords do not match.";
      errorEl.classList.remove("hidden");
      return;
    }

    btn.disabled = true;
    try {
      const data = await api("/api/auth/signup", {
        method: "POST",
        body: JSON.stringify({
          username: fd.get("username"),
          password: fd.get("password"),
        }),
      });
      setAuth(data.token, data.username);
      window.location.href = "/chat.html";
    } catch (err) {
      errorEl.textContent = err.message;
      errorEl.classList.remove("hidden");
    } finally {
      btn.disabled = false;
    }
  });
}

function addBubble(container, role, text, meta) {
  const article = document.createElement("article");
  article.className = `chat-bubble ${role}`;
  article.innerHTML = `
    <span class="bubble-label">${role === "user" ? "You" : "SupportAI"}</span>
    <p></p>
  `;
  article.querySelector("p").textContent = text;

  if (meta) {
    const ul = document.createElement("ul");
    ul.className = "meta-tags";
    ul.innerHTML = `
      <li>Intent: ${meta.intent}</li>
      <li>Emotion: ${meta.emotion}</li>
      <li>Confidence: ${meta.confidence}</li>
    `;
    article.appendChild(ul);
  }

  container.appendChild(article);
  article.scrollIntoView({ behavior: "smooth" });
}

function initChatPage() {
  const page = document.getElementById("chat-page");
  if (!page) return;

  if (!getToken()) {
    window.location.href = "/login.html";
    return;
  }

  const username = getUsername();
  const userLabel = document.getElementById("chat-username");
  if (userLabel) userLabel.textContent = username || "";

  const messages = document.getElementById("chat-messages");
  const form = document.getElementById("chat-form");
  const input = document.getElementById("chat-input");
  const errorEl = document.getElementById("chat-error");
  const clearBtn = document.getElementById("clear-chat");

  addBubble(
    messages,
    "bot",
    `Hi${username ? ` ${username}` : ""}! I'm SupportAI. Ask me about orders, refunds, payments, or anything else.`
  );

  clearBtn.addEventListener("click", () => {
    messages.innerHTML = "";
    addBubble(messages, "bot", "Conversation cleared. How can I help you today?");
    errorEl.classList.add("hidden");
  });

  form.addEventListener("submit", async (e) => {
    e.preventDefault();
    const text = input.value.trim();
    if (!text) return;

    errorEl.classList.add("hidden");
    input.value = "";
    addBubble(messages, "user", text);

    const sendBtn = form.querySelector('button[type="submit"]');
    sendBtn.disabled = true;
    input.disabled = true;

    try {
      const data = await api("/api/chat", {
        method: "POST",
        body: JSON.stringify({ message: text }),
      });
      addBubble(messages, "bot", data.response, {
        intent: data.intent,
        emotion: data.emotion,
        confidence: data.confidence,
      });
    } catch (err) {
      errorEl.textContent = err.message;
      errorEl.classList.remove("hidden");
    } finally {
      sendBtn.disabled = false;
      input.disabled = false;
      input.focus();
    }
  });
}

document.addEventListener("DOMContentLoaded", () => {
  initTheme();
  initHeader();
  initLoginForm();
  initSignupForm();
  initChatPage();
});
