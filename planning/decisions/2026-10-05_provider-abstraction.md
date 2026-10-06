# 2026-10-05 -- Provider abstraction & no LangGraph

**Decision:** Use one `OpenAICompatibleClient` (OpenAI + Kimi) and a separate
`AnthropicClient`, behind a tiny `LLMClient` protocol with `complete()` and
`stream()`. Orchestrate research as a plain async generator, not LangGraph.

**Context:** The reference backend uses LangGraph + `open_deep_research`. We want
something a human can read top-to-bottom in one file and that ICM can route to.

**Options considered:**
1. LangGraph (reference approach) -- powerful, but heavy and opaque for a linear flow.
2. Plain async generator -- linear, legible, matches ICM invariant 9.

**Rationale:** The workflow is strictly sequential with human-visible stages. A
generator keeps control flow in one place and makes streaming natural.

**Consequences:** If we later need branching or parallel sub-question research
inside one request, revisit (could add `asyncio.gather` per sub-question, or a
framework). Compare-mode concurrency stays a frontend concern.

**Decision:** Anthropic client omits `thinking`/`effort` so one code path works
for every user-selected Anthropic model (Haiku rejects what Opus requires).
