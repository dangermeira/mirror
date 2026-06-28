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
├── backend/    # FastAPI app (API + caching + the data adapter)
└── docs/       # project overview, architecture, plan, decisions, glossary
```

## Docs

- [Project overview](docs/project-overview.md) — what it is, why, and the visual direction
- [Architecture](docs/architecture.md) — the data pipeline and how it stays multi-game-ready
- [Development plan](docs/development-plan.md) — phases and build order
- [Decisions](docs/decisions.md) — why the key choices were made

## Status

Phase 1 — Overwatch 2 MVP, in active development. (Quickstart and a screenshot land once there's a running app.)

## License

MIT — see [LICENSE](LICENSE).
