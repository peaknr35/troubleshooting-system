# Setup

## Prerequisites
- Docker (for the one-command path), or Python 3.12+ and Node 18.18+ for local dev.
- An API key for at least one provider (OpenAI, Anthropic, or Kimi/Moonshot).

## Docker (recommended)
```bash
docker compose up --build
# frontend http://localhost:3000, backend http://localhost:8080
```
Optional: to enable the OAuth "Create Google Doc" export, create a `.env` at the
repo root with `NEXT_PUBLIC_GOOGLE_CLIENT_ID=<your-web-oauth-client-id>` before
building (it is baked into the frontend bundle at build time).

## Backend only
```bash
cd backend
python -m venv .venv
. .venv/Scripts/activate          # Windows (bash). macOS/Linux: . .venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8080
```
Config is via env vars with the `APP_` prefix — see `backend/.env.example`.

## Frontend only
```bash
cd frontend
npm install
# point the UI at your backend:
echo "NEXT_PUBLIC_BACKEND_URL=http://localhost:8080" > .env.local
npm run dev
```

## Using the app
1. Click **Keys**, paste a key for your provider. Keys are saved in your browser
   (localStorage) only. You can export/import them as JSON, or clear them.
2. Type a question, pick a provider + model, and click **Research**.
3. Watch planning, per-sub-question findings with sources, then the streamed
   report. Export it to Google Docs.
4. Use **Compare** to run the same question on several models at once.

## Google Docs export (optional)
- **Copy for Google Docs** always works (clipboard, no setup).
- **Create Google Doc** needs a Google OAuth Web Client ID in
  `NEXT_PUBLIC_GOOGLE_CLIENT_ID`, with the Docs API enabled and your origin added
  to the client's authorized JavaScript origins.
