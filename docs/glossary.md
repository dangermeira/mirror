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
- **HTTP** — the web's request/response protocol: how separate programs (like our
  frontend and backend) send messages to each other over a network.
- **JSON** — a lightweight text data format (e.g. `{"username": "Ash"}`) that both Python
  and JavaScript can read; the neutral format the frontend and backend exchange data in.
- **Web framework** — a toolkit (ours is FastAPI) that handles the repetitive plumbing of
  receiving requests and sending responses, so you write only the app-specific logic.
- **ASGI server** — the always-on program (ours is uvicorn) that listens for incoming
  HTTP requests and hands each to the web framework. The framework *describes* responses;
  the server *runs and listens*.
- **Build tool** — a program (ours is Vite) that bundles and transpiles frontend source
  (TypeScript/React) into the plain JavaScript a browser runs; in dev it also serves the
  app with instant reload.
- **Transpile** — auto-translate code from one language into a closely related one (e.g.
  TypeScript → plain JavaScript) so a target like the browser can run it.
- **Component** — a reusable, self-contained piece of UI in React (a search bar, a stat
  card) that you compose with other components to build a page.

_(More React / Tailwind / TypeScript terms — props, state, hook, utility class, Pydantic
model, async — get added here as we meet them.)_
