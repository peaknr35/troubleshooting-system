# backend/app/models -- request & event models

One job: define and validate the data that crosses the API boundary. The event
model here is the server side of the SSE contract.

## What's here
- `research.py` -- `Provider` enum; `ResearchRequest` (validated body); `Source`;
  `ResearchEvent` (+ `to_sse()`); `EventFactory` (events sharing one research_id).
- `__init__.py`

## Mirrors (one home per fact)
`ResearchEvent` + the event types mirror `../../../_shared/api-contract.md`. To
change the event shape: edit the contract first, then here, then `frontend/lib/types.ts`.

## Rules
- Validation lives in Pydantic field validators (min lengths, enum, ranges).
- `api_key` is `repr=False` so it never prints in logs or tracebacks.

## Where to add things
- New request field -> add to `ResearchRequest` with a validator + default.
- New event type -> add to the `EventType` Literal + an `EventFactory` method, then
  update `_shared/api-contract.md` and `frontend/lib/types.ts`.

## Links
- Contract: `../../../_shared/api-contract.md` . Parent: `../CONTEXT.md`
