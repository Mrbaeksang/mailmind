import type { Email, SearchHit, ThreadInsight } from "./types";

const BASE = process.env.NEXT_PUBLIC_API_URL ?? "http://localhost:8011";

async function get<T>(path: string): Promise<T> {
  const res = await fetch(`${BASE}${path}`, { cache: "no-store" });
  if (!res.ok) throw new Error(`${path} → ${res.status}`);
  return res.json() as Promise<T>;
}

export const api = {
  listEmails: (category?: string) =>
    get<Email[]>(`/emails${category ? `?category=${encodeURIComponent(category)}` : ""}`),

  getThread: (threadId: string) => get<ThreadInsight>(`/threads/${threadId}`),

  search: (q: string) => get<SearchHit[]>(`/search?q=${encodeURIComponent(q)}`),

  process: async (): Promise<{ processed: number }> => {
    const res = await fetch(`${BASE}/process`, { method: "POST" });
    if (!res.ok) throw new Error(`/process → ${res.status}`);
    return res.json();
  },
};
