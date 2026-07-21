import { defineConfig } from 'vite'
import react from '@vitejs/plugin-react'
import tailwindcss from '@tailwindcss/vite'

// https://vite.dev/config/
export default defineConfig({
  plugins: [react(), tailwindcss()],
  server: {
    // The page's origin must match the backend's CORS allowlist. Fail loudly
    // if 5173 is taken instead of silently drifting to another port.
    strictPort: true,
  },
})
