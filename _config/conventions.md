# Conventions

## Python
- `snake_case` for files, functions, variables; `PascalCase` for classes.
- Routes in `app/routes/`, business logic in `app/services/`, provider clients in
  `app/providers/`, Pydantic models in `app/models/`.
- Every provider client raises `ProviderError` (never a raw SDK error) so the
  route can translate it to a clean SSE `error` event.
- Never log an API key. Use `app.logging_config.redact()` on anything that might
  contain one.
- Type-hint public functions. Keep handlers thin; push logic into services.

## TypeScript / React
- Components `PascalCase.tsx`, hooks/libs `camelCase.ts`.
- Client components declare `"use client"`.
- API keys live only in the browser (`localStorage`), never sent to our own
  logging or analytics -- only to the chosen model provider via our backend.

## The SSE contract
- Defined once in `_shared/api-contract.md`. Backend emits it; frontend parses it.
- Change the shape there first, then update `backend/app/models/research.py` and
  `frontend/lib/types.ts` together.

## Commits (if versioned)
Conventional commits: `feat:`, `fix:`, `docs:`, `chore:`, `test:`.

## Decision records
`planning/decisions/YYYY-MM-DD_title.md` when a non-obvious technical choice is made.
