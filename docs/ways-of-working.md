# Mirror — Ways of Working

> How we *build* Mirror: the per-step loop, the git workflow, the engineering
> practices, and how we use AI assistance deliberately. **Read this before starting a
> build step.** The terse version lives in `CLAUDE.md` ("How we work"); this is the
> expanded playbook. (Personal learning preferences are tracked separately, outside the
> repo.)

## The build loop (run this every step)

```
  PLAN ──► BUILD ──► VERIFY ──► REVIEW ──► EXPLAIN ──► SHIP
   │        │         │          │          │          │
  plan     small     run it &   /code-     teach it   branch → PR →
  mode     explained see it     review     back in    merge; docs in
  first    increments work      the diff   own words  the same commit
```

1. **Plan** — for anything non-trivial, enter **Plan Mode** (`Shift+Tab`) first. Claude
   researches and proposes an approach; *you approve before any file is edited.* This
   separates "understand" from "change" — the whole point of building to learn.
2. **Build** — small, explained increments. One new concept at a time.
3. **Verify** — run it. A passing test, a live endpoint at `/docs`, a screenshot. Proof,
   not vibes.
4. **Review** — run `/code-review` on the diff before committing. You learn what
   reviewers actually look for.
5. **Explain (teach-back)** — before shipping, explain in your own words *what* changed
   and *why*. Gaps found here are the real learning; they go on the concept ledger.
6. **Ship** — work on a branch, open a PR, merge. Update the relevant `docs/` file in the
   **same commit** as the change.

## Git workflow

- **Branch per step.** `git switch -c step-3-overfast-adapter`. Keeps `main`
  always-working and the history readable.
- **Conventional Commits.** `type(scope): subject` — `feat:`, `fix:`, `docs:`,
  `refactor:`, `test:`, `chore:`.
  e.g. `feat(backend): map OverFast response into the canonical shape`.
- **Pull Requests, even solo.** Open a PR per step. It's a portfolio artifact, a clean
  review surface, and the industry-standard unit of change. Self-review the diff, then
  merge.

## Engineering practices (phased in at the right step)

| Practice | What / why | When |
|---|---|---|
| Manual verify | Hit the auto-docs at `/docs`, eyeball the response | now |
| Automated tests | `pytest` + FastAPI `TestClient`; the adapter is pure logic → ideal to unit-test | step 3–4 |
| Linter / formatter | `ruff` — fast, catches mistakes, auto-formats to one style | step 3 |
| Type checking | `mypy` (backend) + TS `strict` (frontend); types catch bugs before runtime | step 3 / 5 |
| CI | GitHub Actions runs lint + tests on every PR | step 4–5 |
| Direct dependencies | Declare what you `import` (e.g. `pydantic`, `httpx`) explicitly in `requirements.txt` — don't rely on it arriving transitively | ongoing |

## Using AI deliberately

- **Plan Mode before code** for anything you want to actually understand.
- **Explore subagent** to research an unfamiliar API/library *without* flooding the main
  conversation — it reads and reports back a summary.
- **`/code-review`** on every diff; **`/security-review`** before anything public-facing.
- **Effort dial** (`/effort`): high/max for hard design and debugging, low for mechanical
  edits. It's a time-and-cost control, not a quality switch to leave maxed.
- **Output styles** (`/output-style`): *Explanatory* (Claude annotates the "why" as it
  works) and *Learning* (Claude leaves `TODO(human)` markers for **you** to implement the
  key logic).
- **Verify, don't trust.** AI output can be confidently wrong. Run it, read it, and ask
  Claude to point at the file/line or the docs behind a claim. Verifying *is* the
  learning.

## The golden rule

If you can't explain a piece of code or a decision in your own words, it isn't done — it's
just *present*. The teach-back step exists to catch exactly that.
