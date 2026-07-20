// Field-for-field mirror of backend/models.py — the canonical shape from
// docs/architecture.md. Keep the two files in sync when the shape changes.

export interface RoleRank {
  role: string
  rank: string
}

export interface HeroUsage {
  name: string
  playtime_hours: number
}

export interface OverwatchStats {
  ranks: RoleRank[]
  win_rate: number | null
  top_heroes: HeroUsage[]
}

export interface PlayerProfile {
  username: string
  display_name: string
  avatar_url: string
  source: string
  game: string
  last_updated: string // datetime crosses the wire as ISO text; JSON has no date type
  stats: OverwatchStats
}
