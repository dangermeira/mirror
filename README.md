# Mirror

> "Look into the mirror and you see yourself." Type a player's username and see their game stats reflected back.

A local-first web app where you enter a player username and see that player's current
**Overwatch 2** career stats — rank, win rate, and top hero usage. Built so additional
games can be slotted in later, but the current focus is Overwatch 2 only.

## Stack

- **Frontend:** React + TypeScript (Vite), Tailwind CSS
- **Backend:** Python + FastAPI, httpx
- **Data source:** OverFast API (public OW2 profiles), behind a swappable adapter layer

## Structure

```
mirror/
├── frontend/   # React + TypeScript app (the UI)
└── backend/    # FastAPI app (API + caching + the data adapter)
```

## Status

🚧 Phase 1 — Overwatch 2 MVP, in active development.

---

This is a learning project: my first full-stack app, built to understand each piece as it's made.
