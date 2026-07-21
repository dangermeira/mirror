import type { PlayerProfile } from "./types"

// The backend's failure states, plus the one only the frontend can see.
export type FailureState =
  | "NOT_FOUND"
  | "PRIVATE"
  | "RATE_LIMITED"
  | "SOURCE_DOWN"
  | "UNKNOWN"
  | "UNREACHABLE"

// Every outcome of a search — success, a {state, message} failure from the
// backend, an unreadable body, or no readable response at all — is converted
// into this one type, so the UI never parses errors itself.
export type SearchResult =
  | { ok: true; profile: PlayerProfile }
  | { ok: false; state: FailureState; message: string }

// Substituted by Vite at build time. `||` (not `??`) so an empty value in
// .env also falls back; the trailing-slash trim keeps the path well-formed.
const API_BASE_URL: string = (
  import.meta.env.VITE_API_BASE_URL || "http://localhost:8000"
).replace(/\/+$/, "")

const REQUEST_TIMEOUT_MS = 10_000 // mirrors the backend's own upstream timeout

const UNREADABLE_MESSAGE = "The backend sent a response we couldn't read."
const UNREACHABLE_MESSAGE = "Can't reach Mirror's backend — is it running?"

export async function searchPlayer(battletag: string): Promise<SearchResult> {
  // "#" would start a URL fragment and never be sent — encode it to %23.
  // (App.tsx owns input normalization; the value arrives trimmed.)
  const playerId = encodeURIComponent(battletag)

  let response: Response
  try {
    response = await fetch(`${API_BASE_URL}/player/${playerId}`, {
      signal: AbortSignal.timeout(REQUEST_TIMEOUT_MS),
    })
  } catch {
    // No readable response. Usually the backend isn't running — but a CORS
    // block or a timeout rejects identically; the browser tells code nothing
    // about why (the real reason appears only in the devtools console).
    return { ok: false, state: "UNREACHABLE", message: UNREACHABLE_MESSAGE }
  }

  if (!response.ok) {
    // The backend's exception handler sends {state, message} — pass both
    // through. Guard the shape: a non-JSON or differently-shaped body (e.g.
    // FastAPI's own {detail} responses) becomes UNKNOWN with our own text.
    try {
      const body = await response.json()
      if (typeof body.state === "string" && typeof body.message === "string") {
        return { ok: false, state: body.state as FailureState, message: body.message }
      }
      return { ok: false, state: "UNKNOWN", message: UNREADABLE_MESSAGE }
    } catch {
      return { ok: false, state: "UNKNOWN", message: UNREADABLE_MESSAGE }
    }
  }

  try {
    // response_model validated this shape on the server; the annotation holds
    // our code to it. The parse itself can still fail (truncated body, a
    // non-backend server answering 200) — that must not escape this seam.
    const profile: PlayerProfile = await response.json()
    return { ok: true, profile }
  } catch {
    return { ok: false, state: "UNKNOWN", message: UNREADABLE_MESSAGE }
  }
}
