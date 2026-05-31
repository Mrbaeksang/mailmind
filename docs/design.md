# MailMind — Design System

Reference tone: **Linear/Notion-style SaaS** (dark, minimal, information-dense,
single accent). Design tokens below were collected from real design-system
analyses on [getdesign.md](https://getdesign.md) as *inspiration* (not copied
code), then adapted for MailMind.

Sources collected (2026-05-31):
- **Linear** — https://getdesign.md/linear.app/design-md (primary reference)
- **Claude** — https://getdesign.md/claude/design-md (warm-accent alternative;
  fitting since MailMind is an Anthropic-style agent)

> Component/effect libraries are used **only when OSI-licensed**, source recorded here.
> **shadcn/ui (MIT) is the component base** — safe to copy into our MIT repo.
>
> **License finding (2026-05-31):** **React Bits** (reactbits.dev) is licensed
> **"MIT + Commons Clause"**, which is *not* OSI-approved (Commons Clause
> restricts selling as SaaS). Copying its component code into this MIT-submission
> repo would create a license conflict and risk the hackathon's open-source
> requirement. **Decision: do NOT copy React Bits / 21st.dev code.** We take
> visual inspiration only; all components are built on shadcn/ui (MIT) + the
> Linear-derived tokens below.

## Direction

MailMind uses the **Linear** foundation: a near-black canvas, a single indigo
accent used sparingly, tight spacing, small refined type, hairline borders
instead of heavy shadows. This reads as a fast, professional "agent console"
and maximizes the Design judging criterion without decoration for its own sake.

## Color tokens (Linear-derived, dark)

| Token | Value | Usage |
| --- | --- | --- |
| `--bg-primary` | `#08090A` | App background (near-black) |
| `--bg-secondary` | `#0F1011` | Sidebar, elevated surfaces |
| `--bg-tertiary` | `#1C1D1F` | Cards, popovers, hover |
| `--border` | `#23252A` | Hairline borders, dividers |
| `--text-primary` | `#F7F8F8` | Primary text |
| `--text-secondary` | `#8A8F98` | Muted text |
| `--text-tertiary` | `#62666D` | Disabled, placeholders |
| `--accent` | `#5E6AD2` | Primary accent (indigo) |
| `--accent-hover` | `#6872E5` | Accent hover |
| `--success` | `#4CB782` | Success |
| `--warning` | `#F2C94C` | Warning |
| `--error` | `#EB5757` | Error / destructive |

### Category chip colors (MailMind-specific, mapped to the palette)
| Category | Color | Rationale |
| --- | --- | --- |
| Urgent | `#EB5757` (error red) | Demands attention |
| Action | `#5E6AD2` (accent indigo) | Needs a response |
| Newsletter | `#8A8F98` (muted) | Low priority, informational |
| Spam | `#62666D` (tertiary) | De-emphasized |

## Typography

- Font: **Inter Variable** (fallback: -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif).
- Scale: xs 12/16, sm 13/20, base 14/21, md 15/24, lg 17/24, xl 21/28, 2xl 28/34.
- Weights: body **510**, medium emphasis **538**, headings **600** (never 700+).

## Spacing & shape

- Base unit **4px**: 1=4, 2=8, 3=12, 4=16, 5=24, 6=32, 8=48.
- Radius: sm 4px (inputs/buttons), md 6px (cards), lg 8px (modals), full 9999px (pills/avatars).
- Shadows minimal — rely on background steps + hairline borders, not elevation.

## Components

- **Buttons**: primary = accent bg + white text, 32px tall, 6px radius, sm/510.
  Secondary = tertiary bg + hairline border. Ghost = transparent + hover bg.
- **Inputs**: 32px tall, secondary bg, 1px border, accent focus ring.
- **Cards**: tertiary bg, 6px radius, hairline border, no shadow. Compact.
- Information density is a feature — tight spacing, small type.

## Principles (adapted from Linear)

1. **Speed is the product** — interactions feel instant; never block the UI.
2. **Keyboard-first** — Cmd+K palette, shortcuts for key actions.
3. **Purposeful minimalism** — monochrome + one accent; no decoration without function.
4. **Information density** — show more without clutter.
5. **Consistency** — same patterns everywhere.

## MailMind screens (apply the above)

1. **Inbox** — message list with category chips + category filter; compact rows.
2. **Thread detail** — 3-line summary, to-do checklist, editable reply draft
   (no send button — drafts only).
3. **Search** — natural-language box → vector-search results (the demo finale).
4. **Process** — a single "Process inbox" action that runs the agent.
