# Research Workflow

The deep-research pipeline, implemented in `backend/app/services/research.py` as a
single async generator that yields SSE events. Three stages, code-orchestrated.

## 01 PLAN  (stage: planning)
- Input: the user's `query`.
- The LLM is asked to decompose the question into `max_subquestions` focused,
  independently-researchable sub-questions, returned as strict JSON.
- Robust parse: extract the first JSON object/array; on failure fall back to
  splitting the question into one sub-question (the question itself).
- Emits: `status(planning)`, then `plan` with the sub-question list.

## 02 RESEARCH  (stage: researching)  -- loop, one pass per sub-question
For each sub-question `i`:
1. `status(researching)` with progress = i / N.
2. Web search (`app/services/search.py`): DuckDuckGo, top `search_max_results`.
   Returns `Source[]` (title, url, snippet). Emits `sources`.
   - If `search=false` or search fails, proceed with no sources (the model
     answers from its own knowledge and the finding says so).
3. LLM synthesis: given the sub-question + the search snippets, write a concise,
   grounded answer that cites the source URLs inline. Emits `finding`.

## 03 REPORT  (stage: report)
- `status(report)`.
- The LLM is given the original question + every finding and writes a structured
  markdown report (executive summary, themed sections, conclusion). It is
  **streamed** token-by-token as `token` events.
- After streaming completes, emit `report` with the full text + the de-duplicated
  union of all sources, then `done`.

## Errors
Any exception is caught at the top of the generator and emitted as a single
`error` event (code chosen by exception type: auth/provider/search/internal)
before the stream closes. The process never crashes the request.

## Why no LangGraph
The reference backend uses LangGraph; we keep it to a plain async generator. The
sequencing is linear and human-legible, which matches ICM invariant 9 (the control
flow is visible in one file). Add a framework only if branching/concurrency is
needed later.
