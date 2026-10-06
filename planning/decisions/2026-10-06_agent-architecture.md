# 2026-10-06 -- Agent architecture: dual-track tool calling, SQLite memory

**Decision:** Evolve Deep Research Studio into a local-first personal agent. The
research pipeline becomes the `deep_research` tool. Tool-calling is dual-track:
PydanticAI (default -- native function-calling normalized across providers) + a manual
prompt-JSON backend (fallback -- fully transparent, any model/key). Memory is one local
SQLite file. The terminal uses a Rich TUI.

**Context:** We wanted a readable, local-first assistant (Waku-style) that reuses the
DRS engine, stays provider-agnostic, shows a visible turn loop, and has built-in memory
and evals.

**Options considered:** LangGraph / openai-agents (heavier, opaque) vs pure functions;
native-only vs prompt-JSON-only vs dual-track; Postgres/vector DB vs SQLite.

**Rationale:** Pure functions keep the loop legible; dual-track gives robustness
(PydanticAI) without losing transparency or any-model support (manual). SQLite is
local-first and inspectable; keyword recall now, FTS / sqlite-vec later.

**Consequences:** Adds `pydantic-ai-slim` + `rich`. The manual backend is the tested
default path (exercised offline with a fake client); the PydanticAI backend is
validated with a live key. We own the loop; a new backend is one `*_middle` in
`agent/generate.py`.
