import type { Category } from "@/lib/types";

const STYLES: Record<Category, { label: string; color: string; bg: string }> = {
  urgent: { label: "Urgent", color: "#eb5757", bg: "rgba(235,87,87,0.12)" },
  action: { label: "Action", color: "#8b93f0", bg: "rgba(94,106,210,0.14)" },
  newsletter: { label: "Newsletter", color: "#8a8f98", bg: "rgba(138,143,152,0.12)" },
  spam: { label: "Spam", color: "#62666d", bg: "rgba(98,102,109,0.12)" },
};

export function CategoryChip({ category }: { category: Category | null }) {
  if (!category) {
    return (
      <span className="rounded-full px-2 py-0.5 text-xs text-text-tertiary border border-border">
        unprocessed
      </span>
    );
  }
  const s = STYLES[category];
  return (
    <span
      className="rounded-full px-2 py-0.5 text-xs font-medium"
      style={{ color: s.color, background: s.bg }}
    >
      {s.label}
    </span>
  );
}
