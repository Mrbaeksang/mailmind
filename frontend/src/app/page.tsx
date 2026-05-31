"use client";

import { useEffect, useMemo, useState } from "react";
import { api } from "@/lib/api";
import type { Category, Email, SearchHit } from "@/lib/types";
import { CategoryChip } from "@/components/CategoryChip";
import { Sidebar } from "@/components/Sidebar";
import { SearchBar } from "@/components/SearchBar";

export default function Home() {
  const [emails, setEmails] = useState<Email[]>([]);
  const [filter, setFilter] = useState<Category | "all">("all");
  const [selected, setSelected] = useState<Email | null>(null);
  const [results, setResults] = useState<SearchHit[] | null>(null);
  const [processing, setProcessing] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const load = async () => {
    try {
      setError(null);
      setEmails(await api.listEmails());
    } catch (e) {
      setError(`Couldn't reach the API on :8000. (${(e as Error).message})`);
    }
  };

  useEffect(() => {
    load();
  }, []);

  const counts = useMemo(() => {
    const c: Record<string, number> = { all: emails.length };
    for (const e of emails) if (e.category) c[e.category] = (c[e.category] ?? 0) + 1;
    return c;
  }, [emails]);

  const visible = filter === "all" ? emails : emails.filter((e) => e.category === filter);

  const onProcess = async () => {
    setProcessing(true);
    try {
      await api.process();
      await load();
    } catch (e) {
      setError((e as Error).message);
    } finally {
      setProcessing(false);
    }
  };

  const onSearch = async (q: string) => {
    if (!q) {
      setResults(null);
      return;
    }
    try {
      setResults(await api.search(q));
    } catch (e) {
      setError((e as Error).message);
    }
  };

  return (
    <div className="flex h-screen">
      <Sidebar
        active={filter}
        counts={counts}
        onSelect={(k) => {
          setFilter(k);
          setResults(null);
        }}
        onProcess={onProcess}
        processing={processing}
      />

      <div className="flex w-[28rem] shrink-0 flex-col border-r border-border">
        <header className="flex h-14 items-center border-b border-border px-4">
          <SearchBar onSearch={onSearch} />
        </header>

        {error && (
          <div className="m-3 rounded-md border border-error/40 bg-error/10 p-3 text-xs text-error">
            {error}
          </div>
        )}

        <div className="flex-1 overflow-y-auto">
          {results !== null ? (
            <SearchResults results={results} emails={emails} onPick={setSelected} />
          ) : (
            visible.map((e) => (
              <button
                key={e._id}
                onClick={() => setSelected(e)}
                className={`flex w-full flex-col gap-1 border-b border-border px-4 py-3 text-left transition-colors hover:bg-bg-secondary ${
                  selected?._id === e._id ? "bg-bg-secondary" : ""
                }`}
              >
                <div className="flex items-center justify-between gap-2">
                  <span className="truncate text-sm text-text-primary">{e.subject}</span>
                  <CategoryChip category={e.category} />
                </div>
                <span className="truncate text-xs text-text-secondary">{e.from}</span>
                <span className="line-clamp-1 text-xs text-text-tertiary">{e.body}</span>
              </button>
            ))
          )}
          {results === null && visible.length === 0 && (
            <div className="p-6 text-center text-sm text-text-tertiary">
              No mail here yet. Click &ldquo;Process inbox&rdquo;.
            </div>
          )}
        </div>
      </div>

      <main className="flex-1 overflow-y-auto">
        {selected ? (
          <EmailDetail email={selected} />
        ) : (
          <div className="flex h-full items-center justify-center text-sm text-text-tertiary">
            Select a message to read it.
          </div>
        )}
      </main>
    </div>
  );
}

function SearchResults({
  results,
  emails,
  onPick,
}: {
  results: SearchHit[];
  emails: Email[];
  onPick: (e: Email) => void;
}) {
  if (results.length === 0)
    return <div className="p-6 text-center text-sm text-text-tertiary">No matches.</div>;
  return (
    <div>
      <div className="px-4 py-2 text-xs uppercase tracking-wide text-text-tertiary">
        Semantic results
      </div>
      {results.map((r) => {
        const full = emails.find((e) => e._id === r._id);
        return (
          <button
            key={r._id}
            onClick={() => full && onPick(full)}
            className="flex w-full items-center justify-between gap-2 border-b border-border px-4 py-3 text-left hover:bg-bg-secondary"
          >
            <div className="flex min-w-0 flex-col">
              <span className="truncate text-sm text-text-primary">{r.subject}</span>
              <span className="truncate text-xs text-text-secondary">{r.from}</span>
            </div>
            {typeof r.score === "number" && (
              <span className="shrink-0 text-xs text-accent">{(r.score * 100).toFixed(0)}%</span>
            )}
          </button>
        );
      })}
    </div>
  );
}

function EmailDetail({ email }: { email: Email }) {
  return (
    <article className="mx-auto max-w-2xl p-8">
      <div className="mb-2 flex items-center gap-2">
        <CategoryChip category={email.category} />
      </div>
      <h1 className="mb-1 text-2xl font-semibold tracking-tight">{email.subject}</h1>
      <div className="mb-6 text-sm text-text-secondary">{email.from}</div>
      <p className="whitespace-pre-wrap text-sm leading-relaxed text-text-primary">{email.body}</p>
    </article>
  );
}
