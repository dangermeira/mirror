# Mirror — Decisions Log

A lightweight record of *why* we made each significant choice (an informal "ADR" —
Architecture Decision Record). Newest on top. Append a new entry whenever a real
architectural decision is made; don't rewrite old ones.

Format: **Date — Decision.** Options considered · why · what I learned.

---

**2026-07-21 — Step 6: frontend error-copy pass-through; conscious deferrals.**
Options for UI failure text: re-map `state` to frontend-owned copy vs pass the backend's
`message` through. Chose pass-through: `STATE_META` stays the one home of failure copy,
and the frontend adds only the two sentences the backend can't speak (unreachable, and an
unreadable failure body). Deferred on purpose (recorded, not dropped): frontend runtime
response validation (zod etc.) — `response_model` guarantees the wire shape and the TS
types hold our code to it; `AbortController`/stale-response handling for rapid
re-searches — the overlap window is small and same-key results are identical (revisit
with Step 7 UX); username normalization beyond `.trim()` (still deferred from Step 4).
Learned: an error message is data with one home — pass it along, never copy it.

**2026-07-21 — Step 6: cache stampede closed with a per-key lock (Step-4 deferral).**
Options: leave deferred · one global lock · per-key `asyncio.Lock` with double-checked
caching · an in-flight future map. Chose the per-key lock + re-check: cache hits never
touch a lock; only same-key cold misses queue; and the re-check inside the lock is what
converts "two serialized duplicate trips" into "one trip + one reader." Method: observed
live first (two parallel curls on a cold key → two `fetching … from OverFast` log lines),
fixed, re-observed (→ one line); pinned by `test_main.py`, which forces real overlap with
a zero-second yield inside the fake fetch — a test that would pass without the lock proves
nothing. Corrected along the way: the original deferral's trigger ("StrictMode will double
the first fetch") was wrong for our design — StrictMode doubles renders and effects, not
event handlers, and our fetch runs in a submit handler. The lock dict grows one entry per
key (same accepted unbounded-growth family as the cache). Also added permanently: one INFO
log line per upstream trip in the adapter — the observability that made the stampede
visible at all.
Learned: concurrent cold misses can't see each other's in-flight work; locks without
re-checks only serialize waste; observe a bug before fixing it, and make the regression
test force the exact overlap it claims to test.

**2026-07-21 — Step 6: CORS middleware over a Vite proxy; frontend env config.**
Options: `CORSMiddleware` on the backend with an explicit origin allowlist vs a Vite dev
proxy (`/api` → `:8000`) that sidesteps cross-origin entirely. Chose the middleware: it is
the production-real mechanism (a proxy hides the browser's same-origin policy in dev-only
config), and the allowlist names exactly who may read us — `localhost:5173` and
`127.0.0.1:5173` are listed separately because an origin is a string triple
(scheme+host+port), not a network address. GET only (least privilege). Config:
`VITE_API_BASE_URL` in `frontend/.env` (git-ignored; documented by a committed
`.env.example`), substituted into the JavaScript at build time — so frontend env files
hold configuration only, never secrets. Learned (observed live, not read): the browser
sends the cross-origin request and the server answers it — the block happens at *reading*
the response; and from the page code's view a CORS block is indistinguishable from a dead
backend (both are a rejected fetch), which is why the block must be lifted rather than
handled in code.

**2026-07-07 — Step 5: Tailwind v4 via Vite plugin; single-file static shell; built-in tokens.**
Options: the old v3 flow (`tailwind.config.js` + PostCSS + `@tailwind` directives) vs the v4
setup (`@tailwindcss/vite` plugin + one `@import "tailwindcss";`) · components/state now vs a
single-file static shell · custom theme tokens vs Tailwind's built-in `slate`/`orange`.
Why: v4 is the currently documented setup — two wires instead of three config files (most
online tutorials still show the outdated v3 flow). The shell stays one component (`App.tsx`)
with zero handlers or state, because nothing is interactive yet — components and state arrive
in Step 6 when the search earns them. Exact visual tokens are pinned in `docs/style-guide.md`
(authored now, against real components): slate-950/900/800 surfaces, one orange accent, dark
text on orange (white fails contrast), 4px-grid spacing, left-aligned `max-w-2xl` column.
Learned: Tailwind is a build-time *scanner* (class labels in source → generated CSS out); the
browser only ever receives plain CSS and has never heard of Tailwind.

**2026-07-04 — Step 4 code review: fixed 2, deferred 5.**
Three independent reviewers ran on the diff. Fixed now: (1) `classify_status` maps the whole
4xx band to `NOT_FOUND` (was: only 404; any other 4xx fell through to `UNKNOWN → 502`, a
*client* problem shown as a *server* error); (2) guarded `.json()` so a 200 with a non-JSON
body becomes `SOURCE_DOWN` instead of an uncaught 500 that escapes the taxonomy. A live probe
*refuted* the reviewers' headline scenario (OverFast returns 404, not 422, for malformed
names), but the mapping hardening stands on its own. Deferred (recorded, not dropped): cache
**stampede** (concurrent cold misses both fetch — a per-key lock / in-flight future fixes it;
matters once the React frontend double-renders); **no negative cache / backoff** (a 429/503
isn't cached, so we keep hammering a throttled source); **unbounded cache growth** (no
LRU/sweep; hits also share one object by reference — safe today, freeze models later);
**username normalization** (whitespace/case → duplicate cache keys; centralize the `#`→`-`
transform); and route-level **HTTP-mocked tests** for `fetch_player`'s raising paths.
Learned: verify a finding's concrete scenario before fixing (the 422 wasn't real), but a
robustness fix can still be worth keeping; record deferrals so they're decisions, not misses.

**2026-07-04 — Step 4: canonical error taxonomy + in-memory TTL cache.**
Options: failures as **real HTTP error statuses** + a typed `{state, message}` body vs an
"always-200 envelope". Chose HTTP statuses (404/403/429/503/502) — standard REST, tools and
devtools understand the status, and a browser `fetch` doesn't crash on 4xx/5xx. Adapters
raise `SourceError(SourceState)`; one FastAPI exception handler is the single place a state
becomes an HTTP response. Kept the tricky logic in **pure** functions (`classify_status`,
`is_private`) so it's unit-tested with no network. Cache: a generic `TTLCache` with an
**injectable clock** (testable without waiting), keys namespaced `game:source:id`, only
successes cached, 5-min TTL. PRIVATE is a **heuristic** — OverFast exposes no privacy flag
(verified live), so an empty stats body reads as private, which can't be told apart from a
brand-new public account with zero stats. Deferred: httpx connection pooling via lifespan,
HTTP-mocked adapter tests, config externalization.
Learned: model failures as first-class data, and keep the clock/network at the edges so the
decision logic stays pure and testable.

**2026-07-01 — Step 3 code review: fixed 4 findings, consciously deferred 2.**
A high-effort `/code-review` (3 independent reviewers) surfaced ~8 items. Fixed now:
null-safe hero sort (+ regression test); require both OverFast calls to be 200 so a failed
stats call can't fake an empty-but-"successful" profile; concurrent calls via
`asyncio.gather`; made `_to_canonical` pure (timestamp passed in, not read from the clock)
so the full mapping is unit-testable. Deferred on purpose: (a) `BASE_URL`/timeout stay
hardcoded constants — OverFast is keyless so no secret is exposed; externalize to config
when the app goes public. (b) Ranks are PC-competitive only (console-only players show
none) — accepted MVP scope. The full error taxonomy + cache remain Step 4.
Learned: review surfaces *decisions*, not just bugs — deferrals get recorded, not dropped.

**2026-06-29 — Real OverFast adapter: `adapters/` package, pure mapping split from I/O, validated live.**
Options: flat module vs an `adapters/` package · "overall" (all gamemodes) vs
competitive-only stats · write a test now vs defer.
Why: an `adapters/` package makes the swappable-source seam *physical* (game #2 = a new
file, no rewrite); "overall" matches the project's "overall win rate" wording; a unit test
on the *pure* `_to_canonical` (no network) was cheap and pins the mapping. Split
`fetch_player` (async I/O) from `_to_canonical` (pure mapping) so the logic is testable
offline — verified by 4 passing tests **and** a live call against `TeKrop-2217`.
Learned: `async`/`await` earns its keep when work is **I/O-bound** (awaiting the network),
and isolating pure logic from I/O is exactly what makes it unit-testable.

**2026-06-28 — Canonical shape implemented as nested Pydantic models.**
Options: one flat model with all fields · a universal core model with a nested
game-shaped sub-model.
Why: nesting the OW2 fields inside a `stats` sub-model on the universal
`PlayerProfile` keeps universal and game-specific fields separate, so adding a
second game means adding a stats sub-model (and later a union) — not reshaping
the core. This is the multi-game "seam" built early; machinery comes with game #2.
Lives in `backend/models.py`.

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
