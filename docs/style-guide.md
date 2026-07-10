# Mirror — Style Guide

> Authored in build step 5 — the first moment real components existed to match (per
> [`project-overview.md`](project-overview.md)). These are the exact values behind the visual
> direction: **polished dark slate + one deliberate orange**. We use Tailwind's built-in
> palette for now; promote to named theme tokens when repetition earns it.

## Surfaces (slate — deep neutral, never pure black)

| Role                          | Class       | Hex       |
| ----------------------------- | ----------- | --------- |
| Page background               | `slate-950` | `#020617` |
| Raised surface (inputs, cards)| `slate-900` | `#0f172a` |
| Borders / dividers            | `slate-800` | `#1e293b` |

Three levels, one hue. Elevation = one step lighter, never a shadow-and-glow party.

## Text (on dark)

| Role                         | Class       |
| ---------------------------- | ----------- |
| Primary text                 | `slate-100` |
| Secondary (taglines, hints)  | `slate-400` |
| Muted (placeholders, empty)  | `slate-500` |

`slate-500` is for *muted* roles only — never body copy (contrast).

## Accent (exactly one)

| Role                    | Class        |
| ----------------------- | ------------ |
| Primary action          | `orange-500` |
| Action hover            | `orange-400` |
| Focus rings             | `orange-500` |
| Text **on** orange      | `slate-950`  |

Rules: orange appears in at most **two roles per screen** (the primary action + focus/active
highlights). Text on orange is dark (`slate-950`) — white on `orange-500` fails contrast.

## Type scale (pick from these five, nothing else)

| Step | Classes                                | Use                       |
| ---- | -------------------------------------- | ------------------------- |
| XL   | `text-3xl font-semibold tracking-tight`| App/page title (one max)  |
| L    | `text-lg font-medium`                  | Section headings          |
| M    | `text-base`                            | Body copy                 |
| S    | `text-sm`                              | Controls, secondary text  |
| XS   | `text-xs`                              | Meta / fine print         |

Default font stack for the MVP — no custom font.
**One sanctioned variant:** control labels (button text) use `text-sm font-medium` — the S
step plus medium weight, for controls only.

## Spacing & shape

Everything sits on Tailwind's 4px grid. Project rhythm:

- **Gaps between siblings:** `gap-2` / `gap-3`.
- **Control sizing:** height `h-10`, horizontal padding `px-4` (inputs) / `px-5` (buttons).
- **Section rhythm:** `mt-10` between header and content, `mt-16` before major zones;
  page frame `px-6 py-16`.
- **Layout:** a single **left-aligned column**, `max-w-2xl mx-auto`. Centered *column*,
  left-aligned *content*.
- **Radius:** `rounded-md` controls, `rounded-lg` panels.
- **Never** arbitrary values (`mt-[13px]`) — if it's not on the grid, it's wrong.

## The "don't" checklist (the AI-template tells)

- ❌ No purple/indigo, no gradients, no gradient hero.
- ❌ No emoji in the UI.
- ❌ No centering everything — the layout is a left-aligned column. (Centering *inside* a
  deliberate empty-state panel is allowed.)
- ❌ No eyeballed spacing, no arbitrary `[]` values.
- ❌ No second accent color — orange is alone on purpose.
- ❌ No glassmorphism, backdrop blur, or glow effects.
- ❌ No white text on orange (contrast) — use `slate-950`.
