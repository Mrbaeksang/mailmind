"use client";

import { useState } from "react";

export function SearchBar({ onSearch }: { onSearch: (q: string) => void }) {
  const [q, setQ] = useState("");
  return (
    <form
      onSubmit={(e) => {
        e.preventDefault();
        onSearch(q.trim());
      }}
      className="flex items-center gap-2"
    >
      <input
        value={q}
        onChange={(e) => setQ(e.target.value)}
        placeholder="Search your mail by meaning — e.g. “the vendor contract”"
        className="h-8 w-96 rounded-md border border-border bg-bg-secondary px-3 text-sm text-text-primary placeholder:text-text-tertiary outline-none focus:border-accent focus:ring-1 focus:ring-accent"
      />
      <button
        type="submit"
        className="h-8 rounded-md border border-border bg-bg-tertiary px-3 text-sm text-text-secondary transition-colors hover:text-text-primary"
      >
        Search
      </button>
    </form>
  );
}
