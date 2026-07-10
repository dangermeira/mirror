# Mirror — Architecture

> _Last verified: 2026-06-29 (canonical shape in `backend/models.py`, validated against a real OverFast response via `backend/adapters/overfast.py` in build step 3.)_

The durable "how the system works" doc. **Read this before any backend, adapter, or
data-shape work, or before adding a new game/source.**

## The data pipeline

The browser never talks to the third-party API directly. Our backend is the middleman.

```
Browser (React)  ->  Our Backend (FastAPI)  ->  Third-party API (OverFast)
  username                check cache:
                          - fresh hit? return saved copy
                          - miss? call API, run adapter, cache result
  show stats   <-         return clean, canonical data
  or friendly
  error state
```

## Three invariants (the load-bearing rules)

1. **Backend as middleman.** The browser never calls OverFast directly. The backend is
   the only caller — the one place we control caching, error handling, and (later)
   secret keys. Browsers can't keep secrets.
2. **Adapter → canonical shape.** Each source's messy format is translated by an
   *adapter* into *our own* standard shape. The frontend consumes only that shape and
   never knows which source/game produced it. This is what makes adding a game a
   slot-in, not a rewrite.
3. **Failures are first-class states.** not-found, private profile, source-down,
   rate-limited — each is a defined outcome with a friendly UI message, not an
   exception that crashes the app.

## The canonical shape

> ✅ Validated against a real OverFast response in build step 3 (2026-06-29).
>
> _Implemented as Pydantic models in `backend/models.py`: the universal `PlayerProfile`
> with a nested `OverwatchStats` sub-model. `win_rate` is nullable (a player with 0 games
> has no win rate). The OW2 adapter that produces this shape lives in
> `backend/adapters/overfast.py`._

Keep **universal** fields (true for any game) separate from **game-shaped** fields
(OW2-specific), so game #2 doesn't force a rewrite of the core:

- **Universal:** `username`, `display_name`, `avatar_url`, `source`, `game`, `last_updated`.
- **Game-shaped (OW2):** `ranks` (per role: tank / damage / support), `win_rate`,
  `top_heroes` (name + playtime/usage).

OW2 specifics (roles, SR tiers, hero names) live in the OW2 mapping, **not** baked into
the universal core.

## Canonical error taxonomy

Every adapter maps whatever the source returns into one of these fixed states:
`NOT_FOUND` · `PRIVATE` · `RATE_LIMITED` · `SOURCE_DOWN` (+ a generic `UNKNOWN`
fallback). The frontend has exactly one friendly message per state.

> Implemented in `backend/errors.py` (`SourceState`, `STATE_META`, `SourceError`, and the
> pure `classify_status`). Adapters raise `SourceError(state)`; a single exception handler
> in `backend/main.py` renders it as an HTTP error status + `{state, message}` JSON. OW2
> mapping: `404 → NOT_FOUND`; `429 → RATE_LIMITED`; `>=500` / network / timeout →
> `SOURCE_DOWN`; empty stats body → `PRIVATE` (heuristic — OverFast exposes no privacy flag).

## Adding a new game/source (future checklist)

1. Write a new adapter that maps the source → the canonical shape.
2. Map the source's errors → the canonical error taxonomy.
3. Add a game/source identifier; keep cache keys namespaced by game + source.
4. The frontend should need **no** changes for universal fields.

## Conventions

- **Structure:** `frontend/` (React + TS + Vite + Tailwind v4, scaffolded in step 5 — Vite
  serves/translates on :5173 with the `@tailwindcss/vite` plugin; the UI is a single static
  component in `src/App.tsx` for now; visual tokens live in [`style-guide.md`](style-guide.md)),
  `backend/` (FastAPI on :8000).
- **Config:** all environment-specific values in `.env` (git-ignored); a `.env.example`
  documents required keys.
- **Caching:** in-memory with a TTL for the MVP; may graduate to Redis if the app goes
  public. Implemented as a generic `TTLCache` (injectable clock) in `backend/cache.py`; the
  route caches successful lookups under `game:source:id` keys (5-min TTL).
- **Testing:** light/manual for the MVP; automated tests added as complexity grows.

## Build now vs. designed-for-later

- **Build now (Phase 1):** the pipeline, the OW2 adapter, the canonical shape + error
  states, the in-memory TTL cache, namespaced cache keys.
- **Designed-for, deferred:** a formal multi-source registry/abstraction, Redis,
  multiple adapters. The *seams* exist now; the machinery comes when a second game does.
