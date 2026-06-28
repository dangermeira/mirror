# Mirror — Development Plan

> **Current status:** Phase 1, Step 1 (skeleton & Git) ✅ done. **Next:** Step 2 — backend, one fake-data endpoint.
> _Last reviewed: 2026-06-27_

This doc holds **intent and ordering** — what we're building and in what sequence. It
does *not* describe how the code currently works (that's [`architecture.md`](architecture.md)).
**Read this before starting or finishing a build step;** check the box and update the
status line when a step is done.

## Phase 1 — Overwatch 2 MVP (current)

The core loop, end to end: type a username → backend fetches via the OverFast adapter →
cache → return canonical data → frontend displays **name + avatar, rank (per role if
available), overall win rate, top hero usage**. Friendly failure messages. Recent
searches via localStorage. Match history is a *maybe*, depending on what the free source
provides.

**Build order** (each step: small, explained, verified before moving on):

- [x] **1. Project skeleton & Git** — `frontend/` + `backend/`, repo initialized, pushed
  to GitHub. *Done when: the repo is on GitHub with the structure in place.*
- [ ] **2. Backend: one fake endpoint** — FastAPI running, returns *hardcoded* stats.
  *Done when: the auto-docs page returns fake stats for a username.*
- [ ] **3. Backend: the real adapter** — wire in OverFast, map its data into the
  canonical shape. *Done when: a real username returns real, canonical-shaped stats.*
- [ ] **4. Backend: caching + failure handling** — TTL cache + the four error states.
  *Done when: repeat calls hit cache and each failure returns its friendly state.*
- [ ] **5. Frontend: React + Tailwind shell** — scaffold the app, Tailwind working,
  search bar + empty dark layout. *Done when: the shell renders and Tailwind styles apply.*
- [ ] **6. Frontend: connect to backend** — fetch + display real stats; loading + error
  states. *Done when: searching a username shows real stats in the UI.*
- [ ] **7. Frontend: recent searches** — localStorage QoL. *Done when: recent searches
  persist across reloads.*
- [ ] **8. Polish pass** — apply the design tokens so it looks intentional. *Done when:
  it matches the style-guide and the "don't" list.*

## Later phases (parked — not now)

- Light-mode toggle (low priority).
- Recent match history (if not feasible in Phase 1).
- Charts / data visualizations.
- Multiple games (architecture designed now, activated later).
- Automated testing as complexity grows.
- Public deployment (Redis, accounts/auth if needed, hardening).
- Player comparison.

## Out of scope for the MVP

Everything in the parked list. When these come up mid-Phase-1, note them and redirect.
