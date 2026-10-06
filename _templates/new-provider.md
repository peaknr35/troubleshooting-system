# Add an LLM provider (end to end)

Goal: add a provider so it works in the API *and* the UI, with nothing half-wired.

## Backend
1. `backend/app/models/research.py` -- add the id to the `Provider` enum.
2. `backend/app/providers/<name>_client.py` -- implement a client exposing
   `provider`, `model`, `async complete(system, user, *, max_tokens)`,
   `async stream(...)`; translate SDK errors to `ProviderError`
   (codes: auth | provider | validation | internal).
   - If the provider is OpenAI-compatible, reuse `OpenAICompatibleClient` with a
     `base_url` instead of writing a new client (that is how Kimi works).
3. `backend/app/providers/base.py` -- register it in `build_client()`.
4. `backend/app/config.py` -- add `<name>_default_model` (+ `<name>_base_url` if needed).
5. `backend/app/routes/health.py` -- add it to the `/providers` catalog.
6. `backend/tests/test_providers.py` -- add a factory test (+ error-mapping test if new client).

## Shared contract
7. `_shared/providers.md` -- add the row (SDK, base_url, default + offered models).

## Frontend
8. `frontend/lib/types.ts` -- add the id to the `Provider` union.
9. `frontend/lib/models.ts` -- add a `ProviderInfo` entry (label, keyHint, models, getKeyUrl).

## Verify
- `cd backend && pytest`
- `cd frontend && npm run typecheck`
- Run a research stream with the new provider + a real key.
