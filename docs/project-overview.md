# Mirror — Project Overview

> "Look into the mirror and you see yourself." Type a player's username and see their game stats reflected back.

## What Mirror is

Mirror is a local-first web app: you enter a player's username and Mirror shows that
player's current **Overwatch 2** career stats — name + avatar, rank (per role where
available), overall win rate, and top hero usage. It's a learning project (a first
full-stack app) and a portfolio piece.

## Why it's built this way

The long game is a *multi-game* stats viewer. We don't build that now — but every
decision keeps it possible. The core idea: a player's stats from any game get
translated into one shared shape, so the screen that displays them doesn't care which
game (or data source) they came from. Overwatch 2 is simply the first source we plug
in. (The technical "how" lives in [`architecture.md`](architecture.md).)

## The experience (happy path)

1. The user types a username and hits search.
2. A short loading state appears.
3. The stats come back and render in a clean dashboard.
4. If something's wrong (player not found, profile private, source down), the user sees
   a clear, friendly message — never a crash or a spinner that never ends.

A quality-of-life touch: recent searches are remembered (in the browser) so repeat
lookups are one click.

## The vibe & visual direction

Reference tracker.gg for **how it behaves** (search a player → clean stats dashboard),
**not** how it looks. We are not cloning anyone's visuals.

Goal: clean, modern, intentional — never cheap or "obviously AI-generated."

- **Theme:** polished **dark** mode; a deep neutral **slate** base (not pure black).
  Light mode is parked for later.
- **Accent:** a single warm, easy-on-the-eyes **orange**, used deliberately — one
  confident accent, not a rainbow.
- **Type:** an intentional size/weight hierarchy that creates visual order.
- **Spacing:** a consistent spacing scale; generous whitespace; let the stats breathe.
- **Avoid the AI-template tells:** no generic purple gradients, no emoji in the UI, no
  everything-centered layouts, no eyeballed/inconsistent spacing.

> Exact values (hex codes, the spacing/type scale, a concrete "don't" checklist) get
> pinned down in a `style-guide.md` when UI work begins (build step 5) — written then so
> they match real components instead of being guessed now.
