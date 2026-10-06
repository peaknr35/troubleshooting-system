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
