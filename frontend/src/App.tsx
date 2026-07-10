function App() {
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
          <div className="flex gap-3">
            <input
              type="text"
              aria-label="BattleTag"
              placeholder="Enter a BattleTag, e.g. TeKrop#2217"
              className="h-10 min-w-0 flex-1 rounded-md border border-slate-800 bg-slate-900 px-4 text-sm placeholder:text-slate-500 focus:outline-hidden focus:ring-2 focus:ring-orange-500"
            />
            <button
              type="button"
              className="h-10 rounded-md bg-orange-500 px-5 text-sm font-medium text-slate-950 transition-colors hover:bg-orange-400 focus:outline-hidden focus:ring-2 focus:ring-orange-500 focus:ring-offset-2 focus:ring-offset-slate-950"
            >
              Search
            </button>
          </div>
        </section>

        <section
          className="mt-16 rounded-lg border border-slate-800 py-16 text-center"
          aria-label="Results"
        >
          <p className="text-sm text-slate-500">Search a player to see their stats.</p>
        </section>
      </main>
    </div>
  )
}

export default App
