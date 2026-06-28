# Mirror — Decisions Log

A lightweight record of *why* we made each significant choice (an informal "ADR" —
Architecture Decision Record). Newest on top. Append a new entry whenever a real
architectural decision is made; don't rewrite old ones.

Format: **Date — Decision.** Options considered · why · what I learned.

---

**2026-06-27 — Split the docs: a tiny `CLAUDE.md` router + a `/docs` folder.**
Options: one big CLAUDE.md (original) · split into a router + on-demand docs.
Why: `CLAUDE.md` auto-loads every session, so a big one wastes context on every turn; a
small router plus on-demand `/docs` keeps each session lean while keeping depth
available. Load-triggers in the router tell the AI *when* to read each doc.
Learned: in AI-assisted projects, *what auto-loads* is a budget you spend every turn.

**2026-06-27 — Working-style canonical in `CLAUDE.md` (repo); memory points to it.**
Options: keep it in private Claude memory · keep it in the repo.
Why: putting it in the repo makes the project portable — a fresh clone or another tool
sees how to work on it. The memory file is slimmed to a pointer to prevent drift.

**2026-06-27 — MIT license.**
Options: no license · MIT · other.
Why: a public portfolio repo with no license is legally "all rights reserved" and
signals inexperience; MIT is the standard permissive choice.

**(design phase) — Backend as middleman.**
Why: browsers can't keep secrets and can't do server-side caching / CORS handling
cleanly; a small backend is the only safe place for keys, caching, and error shaping.

**(design phase) — Adapter layer + one canonical shape.**
Why: isolates each messy source behind a translator so adding a game/source is a
slot-in, not a rewrite. The whole multi-game vision rides on this.

**(design phase) — OverFast as the first data source.**
Options: official OW API (doesn't exist) · tracker.gg (needs a key/approval) · OverFast
(free, keyless).
Why: free and keyless lets us build now; the adapter means we can swap to tracker.gg
later without touching the frontend.

**(design phase) — In-memory TTL cache (not Redis) for the MVP.**
Why: the simplest thing that protects against rate limits and makes repeat searches
instant; Redis is overkill until the app is public / multi-instance.

**(design phase) — FastAPI (async) + Pydantic.**
Why: async fits an app whose main job is awaiting a third-party API; Pydantic gives us
the canonical shape + validation for free; auto-docs aid learning.

**(design phase) — Monorepo: one repo, `frontend/` + `backend/`.**
Why: simplest to manage and reason about for a solo first project.
