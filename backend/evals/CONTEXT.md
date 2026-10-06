# backend/evals -- test whether changes make the agent better

One job: two-tier evals -- deterministic checks (offline, no key) + LLM-as-judge
(needs a key) over the agent's turn trace.

## What's here
- `cases/*.jsonl` -- eval cases: `{id, message, expect_tool?}`.
- `deterministic.py` -- offline checks: parsing, tool registry, memory CRUD/recall, file sandbox.
- `judge.py` -- run a case through `run_turn` and score it (tool choice + LLM judge).
- `run.py` -- entrypoint.

## Run
- `cd backend && python -m evals.run`                 (deterministic always; judge if `APP_API_KEY`)
- `cd backend && python -m evals.run --deterministic` (offline only)
- `APP_API_KEY=... python -m evals.run --judge`       (LLM-as-judge)

## Rules
- Deterministic evals must pass offline (no key, no network); they gate changes.
- Runs use a temp DB + workspace; they never touch `~/.assistant`.

## Where to add a case
Add a line to `cases/basic.jsonl` (or a new `*.jsonl`): `{id, message, expect_tool?}`.

## Links
- Turn loop: `../app/agent/CONTEXT.md` . Parent: `../CONTEXT.md`
