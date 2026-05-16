const API_BASE = "http://localhost:8000/v1";
const AUTH_TOKEN = "Bearer enterprise-demo-key";

export async function submitSearch(query) {
  const response = await fetch(`${API_BASE}/search`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      Authorization: AUTH_TOKEN,
    },
    body: JSON.stringify({ query, top_k: 5 }),
  });
  return response.json();
}

export async function submitChat(message) {
  const response = await fetch(`${API_BASE}/chat`, {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
      Authorization: AUTH_TOKEN,
    },
    body: JSON.stringify({ user_id: "enterprise-user", session_id: "demo-session", conversation: [{ role: "user", content: message }] }),
  });
  return response.json();
}
