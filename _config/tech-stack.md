# Tech Stack

## Backend (`backend/`)
- Python 3.12
- FastAPI + Uvicorn (ASGI)
- Pydantic v2 + pydantic-settings (request validation + config)
- SSE streaming via `StreamingResponse` (media type `text/event-stream`)
- LLM SDKs:
  - `openai` -- used for OpenAI AND Kimi K2 (Kimi is OpenAI-compatible; only the
    `base_url` differs: `https://api.moonshot.ai/v1`)
  - `anthropic` -- used for Claude
- Web search: `ddgs` (DuckDuckGo, no API key). Optional Tavily if a key is given.
- Tests: `pytest` + `pytest-asyncio` + FastAPI `TestClient` (providers mocked)

## Frontend (`frontend/`)
- Next.js 15 (App Router) + React 18 + TypeScript
- Tailwind CSS
- lucide-react icons
- State: React Context mounted in the root layout (survives route changes),
  mirrored to `localStorage`/`sessionStorage` for reload resilience
- Streaming: `fetch()` + `ReadableStream` reader parsing SSE (POST body, so
  EventSource is not usable)

## Containers / deploy
- Docker for each app; `docker-compose.yml` runs both locally
- Backend deploys to Google Cloud Run (listens on `$PORT`, default 8080)

## Model IDs verified (2026-10-05) -- all overridable per request
- OpenAI default: `gpt-5.1`
- Anthropic default: `claude-opus-5-5`
- Kimi default: `kimi-k2-0905-preview`
See `_shared/providers.md` for the full matrix.
