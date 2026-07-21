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
- **Origin** — a page's identity for the browser: scheme + host + port, all three.
- **Same-origin policy** — the browser rule that a page's JavaScript may only *read*
  responses from its own origin. The request still goes out; the *reading* is blocked.
- **CORS** — Cross-Origin Resource Sharing: the response headers by which a server grants
  a named foreign origin permission to read it (ours: `CORSMiddleware` allowlisting the
  dev frontend origins).
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

- **Header (HTTP)** — one `name: value` line at the top of an HTTP message, describing
  the message (e.g. `content-type: application/json`).
- **Middleware** — code the web framework runs around every request/response; it can read
  or modify either (ours: `CORSMiddleware`).
- **Fragment** — the `#…` tail of a URL: a browser-only note-to-self, never sent to any
  server. The reason BattleTags must be encoded.
- **Percent-encoding** — disguising a reserved URL character as `%` + its byte in hex
  (`#` → `%23`) so it survives URL parsing; the server decodes it after.
- **Promise** — a JavaScript object standing in for a value that arrives later; it
  *resolves* with the value or *rejects* with an error. `fetch` returns one.
- **Interface (TypeScript)** — a named description of an object's fields and their types;
  checked at build time, erased from the shipped code.
- **Discriminated union** — a union type whose variants share one tag field (our
  `SearchState.status`), so the compiler knows which fields exist in each branch.
- **State (React)** — data a component owns that survives re-renders; updating it via the
  `useState` setter triggers a re-render.
- **Controlled input** — an input whose displayed value is bound to state (`value` +
  `onChange`); the state variable is the single source of truth for the box.
- **Props** — the single object of inputs a parent passes to a child component
  (`<PlayerCard profile={…} />`).
- **Conditional rendering** — returning different JSX depending on state; exactly one of
  the four result panels renders at a time.
- **StrictMode** — a development-only React wrapper that runs renders and effects twice
  to expose bugs. It does not double event handlers.
- **Cache stampede** — simultaneous cold misses for one key each doing the expensive
  fetch, because none can see the others' in-flight work.
- **Double-checked caching** — the stampede fix: check the cache, take a per-key lock,
  check again inside it, and only then fetch.

_(Grown as we meet terms — Tailwind utilities, Pydantic model, async/await, hooks beyond
`useState`, and Step 7's localStorage patterns are next.)_
