import type { PlayerProfile } from "./types"

// Every outcome of a search — success, a {state, message} failure from the
// backend, an unreadable body, or no backend at all — is converted into this
// one type, so the UI never parses errors itself.
export type SearchResult =
  | { ok: true; profile: PlayerProfile }
  | { ok: false; message: string }

// Substituted by Vite at build time; the fallback covers a missing .env.
const API_BASE_URL: string = import.meta.env.VITE_API_BASE_URL ?? "http://localhost:8000"

const FALLBACK_MESSAGE = "Something went wrong fetching those stats."
const UNREACHABLE_MESSAGE = "Can't reach Mirror's backend — is it running?"

export async function searchPlayer(battletag: string): Promise<SearchResult> {
  // "#" would start a URL fragment and never be sent — encode it to %23.
  const playerId = encodeURIComponent(battletag.trim())

  let response: Response
  try {
    response = await fetch(`${API_BASE_URL}/player/${playerId}`)
  } catch {
    // fetch rejects only when there is no response at all (backend not
    // running). No body exists, so the message must be our own.
    return { ok: false, message: UNREACHABLE_MESSAGE }
  }

  if (!response.ok) {
    // The backend's exception handler sends {state, message} — pass the
    // message through. Guard the shape: a non-JSON or unexpected body
    // falls back to a generic line.
    try {
      const body = await response.json()
      const message = typeof body.message === "string" ? body.message : FALLBACK_MESSAGE
      return { ok: false, message }
    } catch {
      return { ok: false, message: FALLBACK_MESSAGE }
    }
  }

  // 200: response_model already validated this shape on the server — we type
  // it and read it with no runtime checks of our own.
  const profile: PlayerProfile = await response.json()
  return { ok: true, profile }
}
