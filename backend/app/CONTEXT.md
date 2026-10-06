# backend/app -- the FastAPI application package

One job: the importable app. `main.py` assembles it; everything else is grouped by
role so each kind of thing has exactly one home.

## What's here
- `main.py` -- FastAPI app: loads config, configures logging + CORS, includes routers, `/` root.
- `config.py` -- `Settings` (env prefix `APP_`) + provider default models.
- `logging_config.py` -- logging setup + `redact()` (never log keys).
- `models/` -- Pydantic request + event models (+ `EventFactory`).
- `providers/` -- LLM clients behind the `LLMClient` protocol + `build_client()`.
- `services/` -- business logic: the research pipeline + web search.
- `routes/` -- HTTP/SSE endpoints (thin handlers).
- `__init__.py` -- marks the package.

## Layering (one-directional)
routes -> services -> providers / models; config + logging are leaf utilities.
Handlers stay thin; real work lives in `services/`.

## Rules
- Never log key-shaped text: pass it through `logging_config.redact()`.
- Settings come from env (prefix `APP_`); no secrets in code or config files.

## Where to add things
- New endpoint -> `routes/` (`../../_templates/new-endpoint.md`).
- New provider -> `providers/` (`../../_templates/new-provider.md`).
- New pipeline step -> `services/research.py` (see `services/CONTEXT.md`).

## Links
- Parent: `../CONTEXT.md` . Contracts: `../../_shared/`
