# Mirror — Glossary

Plain-language definitions, grown as new terms appear. (The *behavior* "define new terms
on first use" lives in our working style, not here.)

- **MVP** — Minimum Viable Product: the smallest version that actually works and is useful.
- **Frontend** — the browser side; what the user sees.
- **Backend** — our own server; the logic and the middleman.
- **API** — a service you send requests to and get data back from.
- **Endpoint** — a specific URL on an API for a specific thing.
- **Rate limit** — the cap on how often you can call an API before it temporarily blocks you.
- **Caching** — saving an answer so you don't have to re-fetch it (remember the answer).
- **TTL** — time-to-live: how long a cached answer stays valid before it's stale.
- **CORS** — a browser security rule about which sites may call which APIs (a reason the
  backend middleman helps).
- **Adapter** — a translation layer that converts an external format into our own
  standard shape, so sources are swappable.
- **Canonical shape** — our single standard data format that every adapter must produce;
  the frontend only ever sees this.
- **Environment variables / `.env`** — config kept outside the code, so going public is
  safe and easy.
- **localStorage** — simple key-value storage in the browser that persists across page
  reloads.

_(React / Tailwind / TypeScript terms — component, props, state, hook, utility class,
Pydantic model, async — get added here as we meet them.)_
