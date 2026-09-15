import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'

export default defineConfig({
  plugins: [vue()],
  server: {
    // Lets the Vite dev server forward /translate calls to FastAPI on :8000,
    // so you don't need CORS configured during local development.
    proxy: {
      '/translate': 'http://localhost:8000',
    },
  },
})
