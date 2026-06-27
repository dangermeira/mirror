# Mirror

> "Look into the mirror and you see yourself." Type a player's username and see their game stats reflected back.

A local-first web app where a user enters a player username and sees that player's current **Overwatch 2** career stats — rank, win rate, top hero usage, and (if available) recent matches. Architected so additional games can be added in later phases, but the MVP is **Overwatch 2 only**.

---

## How we work together

This project is a learning vehicle. The user is a rising junior CS major building his first real full-stack app, and learns best by building while understanding what he's building.

- **The user directs and approves; Claude drives and executes.** The user steers; Claude does the hands-on work.
- **Build in small, digestible increments.** Never dump a large block of code without context.
- **Explain what's being built and why, inline, as it's built.** When a new term or concept appears, define it in plain language the first time. The user wants a *high-level* understanding — enough to evaluate and confirm that what's produced is correct and what he wants. Treat "the user can follow and verify this" as a success criterion, not a nice-to-have.
- **Go extra slow and thorough on React and Tailwind CSS** — both are new to him. Narrate *why* a component or class is shaped the way it is, not just what it does. He has some CSS familiarity and is learning TypeScript.
- **Stop and explain** at a high level when he's stuck on a concept before continuing.
- **Check in before significant architectural decisions.** He's steering.
- **Push back and redirect** when he asks for something out of scope for the current phase. Staying focused is part of the job.

---

## Tech stack

**Frontend**
- **React + TypeScript** — component-based UI with type safety.
- **Vite** — build tool and dev server (fast live-reload while developing).
- **Tailwind CSS** — utility-class styling.

**Backend**
- **Python + FastAPI** — async API framework. Auto-generated interactive docs, type hints, and Pydantic models (used as our data-shaping / adapter layer).
- **httpx** — async HTTP client for calling the third-party stats API.

**Data source**
- **OverFast API** — free, keyless source for public OW2 profiles. Accessed **only** through our own adapter layer so it can be swapped for another source (e.g. tracker.gg) later without rewriting the app. Availability/behavior to be verified when we reach that step.

**Caching & storage**
- **In-memory cache with a TTL (time-to-live)** on the backend — protects against rate limits and makes repeat searches instant. May graduate to Redis if/when the app goes public.
- **Browser localStorage** — for the "recent searches" quality-of-life feature.

**Plumbing**
- **One repo, two folders:** `frontend/` and `backend/`.
- **Git + GitHub** (`dangermeira`) from day one.
- **Environment variables / `.env` files** for all config — keeps the app deploy-ready and keeps any future secrets out of the code and out of the browser.

---

## Architecture — the data pipeline

The browser never talks to the third-party API directly. Our own backend is the middleman.

```
Browser (React)  ->  Our Backend (FastAPI)  ->  Third-party API (OverFast)
  username                check cache:
                          - fresh hit? return saved copy
                          - miss? call API, shape data, cache it
  show stats   <-         return clean, standard data
  or friendly
  error screen
```

Key principles baked in from day one:
- **Backend as middleman** — the one place we control caching, error handling, and (later) secret keys. Browsers can't keep secrets.
- **Adapter layer** — the backend translates each source's messy format into *our own* standard data shape. The frontend never knows or cares where the data came from. This is what makes adding games/sources a slot-in change, not a rewrite.
- **Failure modes are first-class states**, not afterthoughts: player not found, profile private, API down/slow, rate-limited. Each gets a clear, friendly UI message instead of a crash.

---

## Design principles

Reference tracker.gg for **how it behaves** (search a player → clean stats dashboard), **not for how it looks**. We are not cloning its visuals.

Goal: clean, modern, intentional — never cheap or "obviously AI-generated."

- **Theme:** polished **dark** mode. Deep neutral slate base (not pure black). (Light-mode toggle is parked for a future low-priority phase.)
- **Accent:** a single warm, easy-on-the-eyes **orange**. One confident accent, used deliberately.
- **Type hierarchy:** intentional sizes/weights that create visual order.
- **Spacing:** a consistent spacing scale, not eyeballed margins.
- **Whitespace:** generous; let stats breathe.
- **Avoid the AI-template tells:** no generic purple gradients, no emoji headers, no everything-centered layouts, no inconsistent spacing.

---

## Conventions

- **Structure:** `mirror/frontend/` (React+TS+Vite+Tailwind) and `mirror/backend/` (FastAPI).
- **Git:** meaningful commits as each small piece is completed; pushed to GitHub. The workflow gets taught as we go.
- **Config:** anything environment-specific lives in `.env`, never hardcoded. `.env` is git-ignored; a `.env.example` documents required keys.
- **Data shape:** the backend defines the canonical stats shape (Pydantic); the frontend consumes only that shape.
- **Testing:** light/manual for the MVP (run the app, check by eye). Automated tests introduced in a later phase as complexity warrants.

---

## Phases

**Phase 1 — Overwatch 2 MVP (current).** The core loop, end to end: type a username → backend fetches via the OverFast adapter → cache → return standard data → frontend displays **name + avatar, rank (per role if available), overall win rate, top hero usage**. Handle the key failure states with friendly messages. Recent searches via localStorage. Match history is a *maybe*, depending on what the free source actually provides.

Build order (each step small, explained, and verified before moving on):
1. **Project skeleton & Git** — create `frontend/` and `backend/`, init the repo, push to GitHub.
2. **Backend: one working endpoint** — FastAPI running, returning *fake* stats first to prove the plumbing (meet the auto-docs page).
3. **Backend: the real adapter** — wire in OverFast through the adapter, shape its data into our standard format.
4. **Backend: caching + failure handling** — TTL cache + friendly error states (not found, private, API down).
5. **Frontend: React + Tailwind shell** — scaffold React app, get Tailwind working, build search bar + empty dark layout.
6. **Frontend: connect to backend** — fetch and display real stats; wire loading + error states.
7. **Frontend: recent searches** — localStorage QoL feature.
8. **Polish pass** — apply design principles so it looks intentional.

**Later phases (parked — not now):**
- Light-mode toggle (low priority).
- Recent match history (if not feasible in Phase 1).
- Charts / data visualizations.
- Multiple games (the multi-game architecture is designed for now, activated later).
- Automated testing as complexity grows.
- Public deployment (Redis caching, accounts/auth if needed, hardening).
- Player comparison.

**Out of scope for the MVP:** anything in the parked list above. When these come up mid-Phase-1, note them and redirect.

---

## Glossary (plain-language)

- **MVP** — Minimum Viable Product: the smallest version that actually works and is useful. Finish the thin core slice before adding extras.
- **Frontend** — the browser side; what the user sees.
- **Backend** — our own server; the logic and the middleman.
- **API** — a service you send requests to and get data back from.
- **Endpoint** — a specific URL on an API for a specific thing.
- **Rate limit** — the cap on how often you can call an API before it temporarily blocks you.
- **Caching** — saving an answer so you don't have to re-fetch it (remember the answer).
- **TTL** — time-to-live: how long a cached answer stays valid before it's considered stale.
- **CORS** — a browser security rule about which sites may call which APIs (a reason the backend middleman helps).
- **Adapter** — a translation layer that converts an external format into our own standard shape, so sources are swappable.
- **Environment variables / `.env`** — config kept outside the code, so going public is safe and easy.
- **localStorage** — simple key-value storage in the browser that persists across page reloads.
