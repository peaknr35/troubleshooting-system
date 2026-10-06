# Changelog

## 2026-10-06 -- docs: complete per-folder ICM
- Added a `CONTEXT.md` to every folder (identity, contents, rules, where to add
  things) so the workspace is self-describing for humans and agents.
- Added `_templates/` (copy-to-create starters: new provider/endpoint/component/
  decision record) and a generated root `FILE-MAP.md` index
  (`ops/scripts/build-file-map.sh`).
- Updated root `CLAUDE.md` routing. No application code changed.

## 2026-10-05 -- 0.1.0 (initial build)
- ICM workspace scaffolded (root router, contracts, factory layer).
- Backend (FastAPI): `/health`, `/providers`, `POST /research/stream` (SSE).
  - Providers: OpenAI, Anthropic, Kimi K2 (bring-your-own-key, nothing stored).
  - Real workflow: plan -> DuckDuckGo web search -> synthesize -> streamed report.
  - Request validation, secret-redacting logging, CORS, Dockerfile (Cloud Run ready).
  - 19 tests (health, auth flow, provider connections, streaming) -- all passing.
- Frontend (Next.js 15 + TS + Tailwind): streaming chat UI, progress stages,
  sources, model switching, compare mode, browser API-key manager with
  import/export, state persistence across navigation, Google Docs export.
  - Production build verified green.
- docker-compose for local full stack; Cloud Run deploy docs + script.
