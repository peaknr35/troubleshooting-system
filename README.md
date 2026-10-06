# Deep Research Studio

A bring-your-own-key **deep research app**. Ask a question; a FastAPI backend runs
a real research workflow — **plan → search the live web → synthesize → write a
cited report** — and streams every step to a polished Next.js UI as it happens.
Supports **OpenAI, Anthropic, and Kimi K2**. No API keys are ever stored on the
server; keys live in your browser and are sent per request.

This repository is organized as an **ICM workspace** (Interpretable Context
Methodology): the folder structure itself documents the system for both humans
and AI agents. Start at [`CLAUDE.md`](CLAUDE.md) (routing) and
[`CONTEXT.md`](CONTEXT.md) (how it fits together).

## Features
- **Live streaming** of planning, per-sub-question research + sources, and a
  token-streamed final report (Server-Sent Events).
- **Three providers, your key:** OpenAI, Anthropic (Claude), Kimi K2 (Moonshot).
- **Model switching** and a **compare mode** (same question across up to 4 models,
  results + timing side by side).
- **API key manager** in the browser: save, import/export JSON, clear.
- **State persists** across navigation (Home ↔ Compare) and reloads.
- **Export to Google Docs**: copy-for-Docs, or one-click OAuth doc creation.
- **Container-ready:** `docker compose up` locally; backend deploys to Cloud Run.

## Quick start (Docker — recommended)
```bash
docker compose up --build
```
- Frontend: http://localhost:3000
- Backend:  http://localhost:8080  (health at `/health`, docs at `/docs`)

Then open the app, click **Keys**, paste an API key for a provider, ask a
question, and watch it research.

## Run locally without Docker
Backend:
```bash
cd backend
python -m venv .venv && . .venv/Scripts/activate   # Windows; use .venv/bin/activate on macOS/Linux
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8080
```
Frontend:
```bash
cd frontend
npm install
npm run dev     # http://localhost:3000 (uses Turbopack)
```

> **Windows / E: drive note:** this project lives on a drive whose filesystem
> returns `EISDIR` from `readlink` on normal files, which breaks the webpack
> `next build` locally (compile succeeds; Node's prerender step fails). It does
> **not** affect Docker (Linux) or Cloud Run, and `npm run dev` uses Turbopack
> which is unaffected. To run a local production build, build via Docker or from
> a folder on your C: drive. The backend and its tests run fine on E:.

## Providers & keys
| Provider | Default model | Get a key |
|---|---|---|
| OpenAI | `gpt-5.1` | https://platform.openai.com/api-keys |
| Anthropic | `claude-opus-5-5` | https://console.anthropic.com/settings/keys |
| Kimi K2 | `kimi-k2-0905-preview` | https://platform.moonshot.ai |

All model IDs are overridable in the UI. See [`_shared/providers.md`](_shared/providers.md).

## Project layout
```
CLAUDE.md / CONTEXT.md   ICM entry + task router
_config/                 project facts, tech stack, conventions, status
_shared/                 API/SSE contract, provider matrix, workflow spec
planning/                specs, architecture, decision records
backend/                 FastAPI app + tests + Dockerfile
frontend/                Next.js app + Dockerfile
docs/                    API reference, setup, changelog
ops/                     Cloud Run deploy + local run recipes
docker-compose.yml       local full stack
```

## Tests
```bash
cd backend
pip install -r requirements-dev.txt
pytest        # 19 tests: health, auth flow, provider connections, streaming
```

## Deploy
Backend → Google Cloud Run: see [`ops/deploy/cloud-run-backend.md`](ops/deploy/cloud-run-backend.md).
Frontend → any Node host / Vercel / Cloud Run; set `NEXT_PUBLIC_BACKEND_URL`.

## License / references
Built as an ICM per the method of Van Clief & McDermott (arXiv:2603.16021).
Structure and workflow informed by ShenSeanChen's launch-DeepResearch
[backend](https://github.com/ShenSeanChen/launch-DeepResearch-Backend) and
[frontend](https://github.com/ShenSeanChen/launch-DeepResearch-Frontend).
