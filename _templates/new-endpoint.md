# Add a backend endpoint

1. `_shared/api-contract.md` -- define/adjust the request + response shape FIRST
   (single source of truth). Then keep everything below in sync with it.
2. `backend/app/models/research.py` -- add/extend Pydantic models (validation).
3. `backend/app/routes/<area>.py` -- add the handler on an `APIRouter`. Keep handlers
   thin; push real logic into `backend/app/services/`.
4. `backend/app/main.py` -- `app.include_router(...)` if it is a new router module.
5. `backend/tests/` -- add a test (happy path + a validation/error case).
6. `docs/api.md` -- document it (mirror of the contract).

Verify: `cd backend && pytest`.
