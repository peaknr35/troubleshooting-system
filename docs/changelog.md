# Changelog

## 2026-10-06 -- 0.2.0 (M2: chat dashboard)
- Frontend chat home: message the assistant and watch the turn loop live -- phase
  badges, tool-call cards, recalled/saved memory -- streamed over SSE.
- Read-only memory panel (facts + counts + recent tool runs) via GET /memory + /trace.
- `lib/api.ts` generalized to one SSE reader with `streamResearch` + `streamChat` +
  `fetchMemory`/`fetchTrace`; new `ChatContext` persists chat across navigation.
- The original research UI moved to `/research`; nav rebranded (Assistant / Research /
  Compare). Typecheck + production build green.

## 2026-10-06 -- 0.2.0 (M1: local agent core)
- Evolved Deep Research Studio into a local-first personal agent; the research
  pipeline is now the `deep_research` tool.
- Agent: a visible turn loop with dual-track tool calling (PydanticAI + manual prompt-JSON).
- Memory: one local SQLite brain (`~/.assistant/state.db`) with recall + consolidation gate.
- Tools: web_search, deep_research, remember/recall, calendar (local), file read/write
  (sandboxed). Interfaces: `POST /chat/stream` + `GET /memory` + `GET /trace`; Rich TUI.
- Tests: 25 passing. New deps: pydantic-ai-slim, rich.

## 2026-10-06 -- docs: complete per-folder ICM
- A `CONTEXT.md` in every folder, a `_templates/` starter set, and a generated
  `FILE-MAP.md` index. No application code changed.

## 2026-10-05 -- 0.1.0 (initial build)
- Deep Research Studio: FastAPI SSE research backend (OpenAI/Anthropic/Kimi, BYO key)
  + Next.js streaming UI (compare mode, key manager, Google Docs export). 19 tests.
