# Backend (FastAPI) -- contract

One job: expose a health check, a provider catalog, and a streaming research
endpoint that runs plan -> research -> report and emits the SSE events defined in
`../_shared/api-contract.md`. Stateless; no key storage.

## Inputs
- Reference (every change): `../_shared/api-contract.md`, `../_shared/providers.md`,
  `../_shared/research-workflow.md`, `../_config/conventions.md`.
- Working: the request body (validated by `app/models/research.py`).
Do NOT load: the frontend. The only coupling is the SSE contract above.

## Structure
```
app/
  main.py            FastAPI app, CORS, routers
  config.py          Settings (env, APP_ prefix) + provider default models
  logging_config.py  logging setup + redact() (never log keys)
  models/research.py Pydantic request + event models + EventFactory
  providers/         LLM clients behind an LLMClient protocol
    base.py          protocol, ProviderError, build_client() factory
    openai_client.py OpenAICompatibleClient (serves OpenAI AND Kimi)
    anthropic_client.py AnthropicClient
  services/
    search.py        web_search() -- DuckDuckGo, no key, returns Source[]
    research.py      run_research() -- the async generator pipeline
  routes/
    health.py        GET/HEAD /health, GET /providers
    research.py      POST /research/stream -> StreamingResponse
tests/               pytest: health, auth flow, provider connections, stream
```

## Process (how a request flows)
1. `routes/research.py` receives a `ResearchRequest` (Pydantic validates -> 422 on bad input).
2. `build_client(provider, api_key, model)` constructs the provider client.
3. `run_research(req, client)` yields `ResearchEvent`s; each is serialized to SSE.
4. Any `ProviderError`/exception becomes one `error` event; the server never 500s mid-stream.

## Run / test
- Dev: `uvicorn app.main:app --reload --port 8080`
- Tests: `pip install -r requirements.txt -r requirements-dev.txt && pytest`

## Human check
Hit `GET /health` -> `{"status":"ok"}`. `pytest` green. A real key in the UI
streams plan/sources/finding/report events in order.

## Avoid
- Logging anything that could contain a key (use `redact()`).
- Sending Anthropic `thinking`/`temperature` (400s on thinking-on models).
- Sending OpenAI `max_tokens`/`temperature` to reasoning models (use `max_completion_tokens`, no temp).
