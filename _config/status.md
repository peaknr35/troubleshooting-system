# Build Status

_Status is derivable from the filesystem: a path existing = that piece is built.
This file is the human-readable summary._

## Done
- [x] ICM workspace scaffold (root router, contracts, factory layer)
- [x] Shared contracts: API/SSE schema, provider matrix, research workflow spec
- [x] Backend: config, logging, Pydantic models
- [x] Backend: provider clients (OpenAI, Anthropic, Kimi) + factory
- [x] Backend: web search tool (DuckDuckGo) + research orchestration service
- [x] Backend: routes (health, research stream) + app wiring
- [x] Backend: tests (health, auth flow, provider connections, stream)
- [x] Backend: Dockerfile + requirements + env example
- [x] Frontend: Next.js app (chat UI, streaming, progress, sources)
- [x] Frontend: model switching + compare mode
- [x] Frontend: API key manager (save / import / export / clear)
- [x] Frontend: state persistence across navigation
- [x] Frontend: export to Google Docs (copy + OAuth create)
- [x] docker-compose + env examples
- [x] docs (api, setup, changelog) + ops (Cloud Run deploy)

## Next / ideas
- [ ] Optional page-content fetch to enrich findings (currently snippet-based)
- [ ] Optional Tavily search backend when a key is provided
- [ ] Persisted research history (would require leaving "stateless" -- see project non-goals)

## Restructure log
- 2026-10-06: Completed per-folder ICM -- added a CONTEXT.md to every folder
  (identity, contents, rules, where to add things), a `_templates/` starter set,
  and a generated `FILE-MAP.md` index. Additive only; no application code changed.

## M1 -- Local agent core (2026-10-06)
- [x] SQLite memory: schema + db + store (facts/turns/tool_runs/calendar/skills) with recall
- [x] Tool registry + tools: web_search, deep_research, remember/recall, calendar (local), file (sandboxed)
- [x] Agent: dual-track engine (manual prompt-JSON + PydanticAI), visible turn loop, consolidation gate
- [x] Routes: POST /chat/stream (SSE) + GET /memory + GET /trace; wired into main
- [x] Terminal: Rich TUI (python -m app.cli)
- [x] Tests: turn loop (offline), tools, file sandbox, PydanticAI model build -- 25 passing
- [x] Shared contracts: agent-turn, memory-schema, tools; per-folder CONTEXTs; root rebrand
- [ ] M2: chat dashboard (frontend)
- [ ] M3: skills loader, LLM-as-judge evals, Google calendar sync

### Open
- Assistant name is a placeholder ("Local Agent"); rename in README + root CLAUDE.md.
- PydanticAI backend is wired + its model construction tested; full live-turn validation needs a key.
