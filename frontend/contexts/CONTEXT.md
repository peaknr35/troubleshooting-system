# frontend/contexts -- React shared state

One job: hold the app's shared, persistent state. Mounted in `app/providers.tsx`
(above the pages) so it survives navigation.

## What's here
- `ApiKeyContext.tsx` -- the user's API keys: load/save to localStorage,
  set/remove/clear, import/export. Hook: `useApiKeys()`.
- `ResearchContext.tsx` -- the main run + compare runs; `runMain/stopMain`,
  `runCompare/stopCompare`; streams via `lib/api`, folds events with
  `lib/research.applyEvent`, mirrors to sessionStorage. Hook: `useResearch()`.

## Reads / Writes
- Reads: `../lib/api.ts` (streaming), `../lib/research.ts` (reducer), `../lib/storage.ts`.
- Writes: `localStorage` (keys) + `sessionStorage` (research state), per-viewer only.

## Rules
- Keys never leave the browser except as the per-request body to our backend.
- On hydrate, coerce any persisted `running` flag to false (the stream is gone).

## Where to add state
Add a field + action to the matching context; if it must persist, mirror it to
storage via `../lib/storage.ts`. A new kind of state can get a new context mounted in
`../app/providers.tsx`.

## Links
- Lib: `../lib/CONTEXT.md` . Parent: `../CONTEXT.md`
