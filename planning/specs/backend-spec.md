# Spec: Backend (FastAPI)

**Problem:** Users want to run a transparent, multi-provider deep-research
workflow with their own API key, and watch it happen live.

**Proposal:** A stateless FastAPI service exposing a health check, a provider
catalog, and an SSE streaming research endpoint.

**Scope (in):**
- `GET/HEAD /health`, `GET /providers`, `POST /research/stream`
- Providers: OpenAI, Anthropic, Kimi K2 (BYO key per request)
- Real research loop: plan -> web search -> synthesize -> streamed report
- Request validation (Pydantic), structured logging (no secrets), CORS
- Tests for provider connections + auth flow (mocked, no real keys)
- Dockerfile; Cloud Run ready (listens on `$PORT`)

**Scope (out):** accounts, persistence, billing, rate limiting beyond provider's.

**Dependencies:** `_shared/api-contract.md`, `_shared/providers.md`,
`_shared/research-workflow.md`.

**Open questions (resolved):**
- Search backend? -> DuckDuckGo (no key) default; Tavily optional later.
- Orchestration? -> plain async generator, no LangGraph (see decision record).
