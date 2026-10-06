# frontend/lib -- framework-free helpers

One job: types, the API client, the reducer, storage, the model catalog, and the
export logic. No React here.

## What's here
- `types.ts` -- SSE event + state types. Mirrors `../../_shared/api-contract.md`.
- `models.ts` -- provider/model catalog. Mirrors `../../_shared/providers.md`.
- `api.ts` -- `streamResearch()`: POST + ReadableStream SSE parser; `BACKEND_URL`.
- `research.ts` -- `applyEvent()` reducer + `initialResearchState/newRunState`.
- `storage.ts` -- localStorage keys + sessionStorage state helpers (all try/catch).
- `googleDocs.ts` -- copy-for-Docs + OAuth create-doc.

## Mirrors (one home per fact)
`types.ts` and `models.ts` are the client copies of the `_shared/` contracts. When a
contract changes, change the contract first, then these.

## Rules
- No DOM assumptions beyond guarded `window` access (stays SSR-safe).
- All browser-storage reads/writes are wrapped in try/catch.

## Where to add things
- New event/state field -> `types.ts` + handle it in `research.ts` `applyEvent`.
- New provider/model -> `models.ts` (+ the backend side; see `../../_templates/new-provider.md`).

## Links
- Contracts: `../../_shared/api-contract.md`, `../../_shared/providers.md` . Parent: `../CONTEXT.md`
