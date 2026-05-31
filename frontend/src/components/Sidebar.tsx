"use client";

import type { Category } from "@/lib/types";

const FILTERS: { key: Category | "all"; label: string }[] = [
  { key: "all", label: "All mail" },
  { key: "urgent", label: "Urgent" },
  { key: "action", label: "Action needed" },
  { key: "newsletter", label: "Newsletters" },
  { key: "spam", label: "Spam" },
];

export function Sidebar({
  active,
  counts,
  onSelect,
  onProcess,
  processing,
}: {
  active: Category | "all";
  counts: Record<string, number>;
  onSelect: (k: Category | "all") => void;
  onProcess: () => void;
  processing: boolean;
}) {
  return (
    <aside className="flex w-60 shrink-0 flex-col gap-1 border-r border-border bg-bg-secondary p-3">
      <div className="mb-3 flex items-center gap-2 px-2 py-1">
        <div className="flex h-6 w-6 items-center justify-center rounded-md bg-accent text-xs font-semibold text-white">
          M
        </div>
        <span className="text-md font-semibold tracking-tight">MailMind</span>
      </div>

      <button
        onClick={onProcess}
        disabled={processing}
        className="mb-3 flex h-9 items-center justify-center gap-2 rounded-md bg-accent text-sm font-medium text-white transition-colors hover:bg-accent-hover disabled:opacity-60"
      >
        {processing ? "Processing…" : "Process inbox"}
      </button>

      <div className="px-2 pb-1 text-xs uppercase tracking-wide text-text-tertiary">Folders</div>
      {FILTERS.map((f) => (
        <button
          key={f.key}
          onClick={() => onSelect(f.key)}
          className={`flex items-center justify-between rounded-md px-2 py-1.5 text-sm transition-colors ${
            active === f.key
              ? "bg-bg-tertiary text-text-primary"
              : "text-text-secondary hover:bg-bg-tertiary/60 hover:text-text-primary"
          }`}
        >
          <span>{f.label}</span>
          <span className="text-xs text-text-tertiary">{counts[f.key] ?? 0}</span>
        </button>
      ))}

      <div className="mt-auto px-2 pt-3 text-xs text-text-tertiary">
        Drafts only · never auto-sent
      </div>
    </aside>
  );
}
