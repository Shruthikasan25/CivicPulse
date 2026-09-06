// Frontend/src/services/api.js
const API_BASE_URL = import.meta.env.VITE_API_BASE_URL || "http://localhost:8000";

async function request(path, options = {}) {
  const res = await fetch(`${API_BASE_URL}${path}`, {
    headers: { "Content-Type": "application/json" },
    ...options,
  });
  if (!res.ok) {
    const body = await res.text();
    throw new Error(`API ${path} failed (${res.status}): ${body}`);
  }
  return res.json();
}

export const getLiveIncidents = () => request("/incidents/live");
export const runPipeline = () => request("/incidents/run-pipeline", { method: "POST" });
export const createReport = ({ description, latitude, longitude }) =>
  request("/reports/", { method: "POST", body: JSON.stringify({ description, latitude, longitude }) });