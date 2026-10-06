# backend/app/routes -- HTTP / SSE endpoints

One job: thin FastAPI handlers that validate input and delegate to services.

## What's here
- `health.py` -- `GET/HEAD /health` + `GET /providers` (the model catalog).
- `research.py` -- `POST /research/stream`: builds the client and streams the
  pipeline's events as SSE (`text/event-stream`).
- `__init__.py`

## Reads / Writes
- Reads: `../models/research.py` (request), `../providers/base.py` (`build_client`),
  `../services/research.py` (`run_research`).
- Writes: an HTTP response (JSON or an SSE stream). No persistence.

## Rules
- Handlers stay thin -- no business logic here; push it to `../services/`.
- Pydantic rejects bad input as 422 before streaming; in-stream failures become a
  single SSE `error` event, never a 500 mid-stream.
- A new router module must be registered in `../main.py` (`include_router`).

## Where to add an endpoint
See `../../../_templates/new-endpoint.md` (contract first, then model, route, main, test, docs).

## Links
- API contract: `../../../_shared/api-contract.md` . Parent: `../CONTEXT.md`
