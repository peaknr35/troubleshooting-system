# Changelog

## 2026-10-06 -- 0.2.0 (M1: local agent core)
- Evolved Deep Research Studio into a local-first personal agent; the research
  pipeline is now the `deep_research` tool.
- Agent: a visible turn loop (RECEIVE -> RECALL -> REASON/ACT/OBSERVE -> REMEMBER ->
  REPLY) with dual-track tool calling (PydanticAI default + manual prompt-JSON fallback).
- Memory: one local SQLite brain (`~/.assistant/state.db`) -- facts, turns, tool_runs,
  local calendar, skills -- with recall + a consolidation gate.
- Tools: web_search, deep_research, remember/recall, calendar (local), file read/write
  (sandboxed to a workspace dir; `APP_FILE_UNRESTRICTED=1` to widen).
- Interfaces: `POST /chat/stream` (SSE turn) + `GET /memory` + `GET /trace`; a Rich
  terminal TUI (`python -m app.cli`).
- Tests: 25 passing (existing 19 + turn loop, tools, file sandbox, PydanticAI build).
- New deps: `pydantic-ai-slim[openai,anthropic]`, `rich`. ICM contracts + per-folder
  CONTEXTs added; root rebranded.

## 2026-10-06 -- docs: complete per-folder ICM
- Added a `CONTEXT.md` to every folder, a `_templates/` starter set, and a generated
  root `FILE-MAP.md` index. No application code changed.

## 2026-10-05 -- 0.1.0 (initial build)
- ICM workspace scaffolded (root router, contracts, factory layer).
- Backend (FastAPI): `/health`, `/providers`, `POST /research/stream` (SSE).
  - Providers: OpenAI, Anthropic, Kimi K2 (bring-your-own-key, nothing stored).
  - Real workflow: plan -> DuckDuckGo web search -> synthesize -> streamed report.
  - 19 tests -- all passing.
- Frontend (Next.js 15 + TS + Tailwind): streaming chat UI, model switching, compare
  mode, browser API-key manager, state persistence, Google Docs export.
- docker-compose for local full stack; Cloud Run deploy docs + script.
