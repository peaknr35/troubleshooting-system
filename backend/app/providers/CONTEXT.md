# backend/app/providers -- LLM clients

One job: turn `(provider, api_key, model)` into an object with `complete()` and
`stream()`, hiding each SDK behind one tiny protocol. The key is used only to build
a client for one request and is never stored.

## What's here
- `base.py` -- the `LLMClient` protocol, `ProviderError`, and `build_client()` factory.
- `openai_client.py` -- `OpenAICompatibleClient`: serves BOTH OpenAI and Kimi (Kimi
  only differs by `base_url`). OpenAI path uses `max_completion_tokens` + no
  temperature; Kimi path uses `max_tokens` + temperature.
- `anthropic_client.py` -- `AnthropicClient`: omits thinking/effort/temperature so one
  code path is valid across every Claude model a user might select.
- `__init__.py`

## Reads / Writes
- Reads: `../config.py` (default models, base_url, timeout).
- Writes: nothing persistent (stateless; no key storage).

## Rules
- Every client raises `ProviderError(code=...)` -- never a raw SDK error -- so the
  route can emit a clean SSE `error`. Codes: auth | provider | validation | internal.
- Do not send a param a user-selected model may reject (see each client header note).

## Where to add a provider
Follow `../../../_templates/new-provider.md`. Chain: enum (`../models/research.py`)
-> client here -> register in `base.py build_client()` -> defaults in `../config.py`
-> `/providers` in `../routes/health.py` -> `_shared/providers.md` ->
`frontend/lib/models.ts`; add a factory test in `../../tests/test_providers.py`.

## Links
- Provider matrix: `../../../_shared/providers.md` . Parent: `../CONTEXT.md`
