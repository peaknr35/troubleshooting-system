# _shared -- cross-cutting contracts (ICM Layer 3, the single source of truth)

One job: the facts BOTH apps must agree on. This is the authoritative home; the
backend and frontend mirror these.

## What's here
- `api-contract.md` -- endpoints + the SSE event schema. Mirrored by
  `backend/app/models/research.py` and `frontend/lib/types.ts`.
- `providers.md` -- the provider/model matrix. Mirrored by `backend/app/config.py`
  + `routes/health.py` and `frontend/lib/models.ts`.
- `research-workflow.md` -- the plan->research->report pipeline spec, implemented in
  `backend/app/services/research.py`.

## Rules
- Change a contract HERE FIRST, then update both apps' mirrors in the same change.
- One home per fact: if it is defined here, other files link, never re-state it.

## Where to add things
- A new cross-app agreement -> a file here, then wire both apps to it.

## Links
- Backend: `../backend/CONTEXT.md` . Frontend: `../frontend/CONTEXT.md` . Root: `../CLAUDE.md`
