# Mirror

Local-first, AI-assisted stats app: type a username, see a player's career stats reflected back. **Game-agnostic by design — Overwatch 2 is the first source, behind a swappable adapter.** Phase 1 (MVP).

## Invariants (never break)
- Browser never calls the stats API directly — the FastAPI backend is the only caller.
- All external data flows through the adapter into one canonical shape the frontend consumes — never a source's raw format.
- Failure modes (not-found, private, API-down, rate-limited) are first-class states.
- Config and secrets live in `.env`, never hardcoded.

## How we work
- User directs and approves; Claude drives and executes in small, explained increments.
- Define new terms in plain language on first use.
- Go extra slow on React and Tailwind (both new).
- Check in before architectural decisions; push back on out-of-phase requests.

## Stack
React, TypeScript, Vite, Tailwind (frontend); FastAPI, httpx, Pydantic (backend); OverFast via adapter; in-memory TTL cache; browser localStorage.

## Docs (read on demand)
- `docs/project-overview.md` — what/why/vibe/visual-design.
- `docs/architecture.md` — pipeline, canonical shape, adapter, adding a game. **Read before backend/data work.**
- `docs/development-plan.md` — phases and build order. **Read before starting/finishing a step.**
- `docs/ways-of-working.md` — the build loop, git/PR workflow, engineering practices, deliberate AI use. **Read before starting a step.**
- `docs/decisions.md` — the "why" behind choices; append on each decision.
- `docs/glossary.md` — plain-language terms.

## Rules
Update the relevant `docs/` file in the same commit as the change. `docs/` is canonical for project facts; filenames kebab-case. Phase 1 now — note and redirect out-of-scope asks.
