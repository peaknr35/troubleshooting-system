# backend/app/services -- business logic

One job: the actual research work, kept out of the route handlers.

## What's here
- `research.py` -- `run_research(req, client)`: the async-generator pipeline
  (plan -> research loop -> streamed report) that yields `ResearchEvent`s. Holds the
  stage prompts and the sub-question JSON parser.
- `search.py` -- `web_search(query, max_results)`: DuckDuckGo via `ddgs` (no key);
  returns `Source[]`; degrades to `[]` on failure.
- `__init__.py`

## Reads / Writes
- Reads: the provider client (passed in), `../config.py` (search size), `search.py`.
- Writes: a stream of events (yielded). No persistence.

## The pipeline (full spec: _shared/research-workflow.md)
01 plan (LLM) -> 02 research loop (search + LLM synthesis, one pass per sub-question)
-> 03 report (LLM, streamed). Each boundary emits SSE events.

## Rules
- Keep the control flow linear and readable (no framework) -- ICM invariant 9.
- Catch provider/other errors at the top and emit exactly one `error` event.
- Any new event you emit must exist in `_shared/api-contract.md` + the `EventFactory`.

## Where to add / change a stage
Edit `run_research` in `research.py` (prompt + an `EventFactory` method), then update
`_shared/research-workflow.md` and `_shared/api-contract.md`. To swap the search
backend, keep `web_search()`'s signature so the pipeline is untouched.

## Links
- Workflow: `../../../_shared/research-workflow.md` . Contract:
  `../../../_shared/api-contract.md` . Parent: `../CONTEXT.md`
