import { useState, type FormEvent } from 'react'
import { searchPlayer } from './api'
import type { PlayerProfile } from './types'

// The UI's fixed set of states — the frontend twin of the backend's failure
// taxonomy. The compiler narrows by `status`, so each panel below can only
// read the fields its state actually has.
type SearchState =
  | { status: 'idle' }
  | { status: 'loading'; battletag: string }
  | { status: 'error'; message: string }
  | { status: 'success'; profile: PlayerProfile }

function App() {
  const [query, setQuery] = useState('')
  const [search, setSearch] = useState<SearchState>({ status: 'idle' })

  async function handleSubmit(e: FormEvent<HTMLFormElement>) {
    e.preventDefault()
    const battletag = query.trim()
    if (!battletag || search.status === 'loading') return
    setSearch({ status: 'loading', battletag })
    const result = await searchPlayer(battletag)
    setSearch(
      result.ok
        ? { status: 'success', profile: result.profile }
        : { status: 'error', message: result.message },
    )
  }

  return (
    <div className="min-h-screen bg-slate-950 text-slate-100">
      <main className="mx-auto max-w-2xl px-6 py-16">
        <header>
          <h1 className="text-3xl font-semibold tracking-tight">Mirror</h1>
          <p className="mt-2 text-sm text-slate-400">
            Type a BattleTag — see their Overwatch 2 stats reflected back.
          </p>
        </header>

        <section className="mt-10" aria-label="Player search">
          <form className="flex gap-3" onSubmit={handleSubmit}>
            <input
              type="text"
              aria-label="BattleTag"
              placeholder="Enter a BattleTag, e.g. TeKrop#2217"
              value={query}
              onChange={e => setQuery(e.target.value)}
              className="h-10 min-w-0 flex-1 rounded-md border border-slate-800 bg-slate-900 px-4 text-sm placeholder:text-slate-500 focus:outline-hidden focus:ring-2 focus:ring-orange-500"
            />
            <button
              type="submit"
              disabled={search.status === 'loading'}
              className="h-10 rounded-md bg-orange-500 px-5 text-sm font-medium text-slate-950 transition-colors hover:bg-orange-400 focus:outline-hidden focus:ring-2 focus:ring-orange-500 focus:ring-offset-2 focus:ring-offset-slate-950 disabled:opacity-50"
            >
              Search
            </button>
          </form>
        </section>

        <section
          className="mt-16 rounded-lg border border-slate-800 py-16 text-center"
          aria-label="Results"
          aria-live="polite"
        >
          {search.status === 'idle' && (
            <p className="text-sm text-slate-500">Search a player to see their stats.</p>
          )}
          {search.status === 'loading' && (
            <p className="animate-pulse text-sm text-slate-500">
              Looking up {search.battletag}…
            </p>
          )}
          {search.status === 'error' && (
            <p className="text-sm text-slate-400">{search.message}</p>
          )}
          {search.status === 'success' && (
            <p className="text-sm text-slate-100">
              {search.profile.display_name} — win rate:{' '}
              {search.profile.stats.win_rate === null
                ? 'no games recorded'
                : `${search.profile.stats.win_rate}%`}
            </p>
          )}
        </section>
      </main>
    </div>
  )
}

export default App
