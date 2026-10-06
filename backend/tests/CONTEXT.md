# backend/tests -- pytest suite

One job: prove the API, auth flow, and provider wiring work -- with no real keys or
network (providers + search are mocked).

## What's here
- `conftest.py` -- the `client` fixture (FastAPI `TestClient`).
- `test_health.py` -- `/health`, `/`, `/providers`.
- `test_auth.py` -- request validation (422s) + invalid key -> SSE `error` (auth).
- `test_providers.py` -- factory builds the right client; OpenAI happy path +
  auth-error mapping + stream chunking (all mocked).
- `test_research_stream.py` -- full pipeline event order with a fake LLM + fake search.
- `__init__.py`

## Run
`cd backend && pip install -r requirements-dev.txt && pytest`
(`asyncio_mode=auto` and `testpaths` are set in `../pyproject.toml`).

## Rules
- Never use a real key or hit the network. Patch `build_client` in
  `app.routes.research` and `web_search` in `app.services.research` (patch at the
  import site the code uses, not the definition site).
- Add a test with every new endpoint, provider, or event type.

## Links
- Parent: `../CONTEXT.md` . App: `../app/CONTEXT.md`
