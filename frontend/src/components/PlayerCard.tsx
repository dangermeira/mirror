import type { PlayerProfile } from '../types'

// Success view only. Everything here can assume a complete PlayerProfile —
// the backend's response_model and api.ts guaranteed the shape upstream.
export function PlayerCard({ profile }: { profile: PlayerProfile }) {
  const { stats } = profile
  return (
    <div className="flex flex-col gap-6">
      <header className="flex items-center gap-3">
        <img
          src={profile.avatar_url}
          alt={`${profile.display_name}'s avatar`}
          className="h-16 w-16 rounded-md border border-slate-800 bg-slate-900"
        />
        <div>
          <h2 className="text-lg font-medium">{profile.display_name}</h2>
          <p className="text-sm text-slate-400">
            {stats.win_rate === null
              ? 'No games recorded'
              : `${stats.win_rate}% win rate`}
          </p>
        </div>
      </header>

      <div>
        <h3 className="text-sm text-slate-400">Competitive ranks</h3>
        {stats.ranks.length === 0 ? (
          <p className="mt-2 text-sm text-slate-500">No PC competitive ranks</p>
        ) : (
          <ul className="mt-2 flex flex-wrap gap-3">
            {stats.ranks.map(r => (
              <li key={r.role} className="rounded-md bg-slate-900 px-4 py-2 text-sm">
                <span className="text-slate-400">{r.role}</span>{' '}
                <span className="text-slate-100">{r.rank}</span>
              </li>
            ))}
          </ul>
        )}
      </div>

      <div>
        <h3 className="text-sm text-slate-400">Top heroes by playtime</h3>
        {stats.top_heroes.length === 0 ? (
          <p className="mt-2 text-sm text-slate-500">No hero playtime recorded</p>
        ) : (
          <ul className="mt-2 flex flex-col gap-2">
            {stats.top_heroes.map(h => (
              <li key={h.name} className="flex justify-between text-sm">
                <span className="text-slate-100">{h.name}</span>
                <span className="text-slate-400">{h.playtime_hours} h</span>
              </li>
            ))}
          </ul>
        )}
      </div>
    </div>
  )
}
