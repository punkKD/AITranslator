# AITranslator
Mobile-first translate UI built with Vue 3, backed by a FastAPI API.

## Project structure

```
lingo-app/
├── backend/
│   ├── main.py            # FastAPI app + /translate endpoint
│   └── requirements.txt
├── frontend/
│   ├── src/
│   │   ├── App.vue        # main UI
│   │   ├── main.js
│   │   └── style.css
│   ├── index.html
│   ├── package.json
│   └── vite.config.js
├── Dockerfile              # multi-stage: builds frontend, serves via FastAPI
├── docker-compose.yml
```

## Local development

Two terminals, backend and frontend run separately with hot reload:

```bash
# Terminal 1 — backend
cd backend
pip install -r requirements.txt
uvicorn main:app --reload --port 8000

# Terminal 2 — frontend
cd frontend
npm install
npm run dev
```

Open the Vite dev URL (usually `http://localhost:5173`). API calls to `/translate/*`
are proxied to the FastAPI server on port 8000 (see `vite.config.js`), so
CORS isn't an issue in dev.

## Plugging in a real translation engine

`backend/main.py` currently has a stub in the `translate()` function. Swap
that logic out for a real call — e.g. an external translation API, or a
locally hosted model — and keep the same request/response shape so the
frontend doesn't need to change.

## Production build (single container)

```bash
docker compose up --build
```

This builds the Vue app, then serves the static files directly from FastAPI
on port 8000 — one container, no separate frontend host needed.

## Deploying on your UGREEN NAS

1. Push this project to a git repo (or copy it directly to the NAS).
2. In UGOS Pro: **Docker > Project > Create**, and point it at this
   directory's `docker-compose.yml` (or paste its contents in).
3. Map any folder you want to persist (e.g. logs or a database file) as a
   volume in the compose file before deploying.
4. Deploy. The app will be reachable at `http://<nas-ip>:8000`.

To update after code changes: edit the Project (not the container directly),
then redeploy — UGOS rebuilds the containers with the same settings.

## Using it as a mobile app

Since the container serves a normal web app on your local network, the
simplest path is opening `http://<nas-ip>:8000` in your phone's browser and
using **"Add to Home Screen"** — it'll behave like an installed app without
extra work. If you later want a true installable PWA (offline support, home
screen icon, splash screen), add a manifest + service worker via
`vite-plugin-pwa` — happy to wire that in if you want to go that route.
