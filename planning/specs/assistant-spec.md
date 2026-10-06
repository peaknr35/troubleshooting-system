# Spec: Local Agent

**Problem:** A local-first personal assistant on the laptop, readable end to end, that
talks in a terminal AND a dashboard off one brain, remembers useful things, and does
practical work with tools.

**Proposal:** A stateful, visible turn loop over a provider-agnostic model, a single
SQLite brain, a tool registry, a Rich terminal TUI, a chat dashboard, and built-in evals.

**Scope**
- M1: turn loop (visible phases), SQLite memory (recall + consolidation gates), tools
  (web_search, deep_research, remember/recall, calendar-local, file sandboxed), Rich TUI,
  `/chat/stream` + `/memory` + `/trace`, tests.
- M2: chat dashboard (live turn timeline + memory panel); research moves to `/research`.
- M3: skills loader, LLM-as-judge evals, optional Google calendar sync.

**Out:** accounts, server-side key storage, multi-user serving.

**Dependencies:** `_shared/agent-turn-contract.md`, `_shared/memory-schema.md`,
`_shared/tools.md`, `_shared/providers.md`.
