# Add a frontend component / feature

1. `frontend/components/<Name>.tsx` -- PascalCase; add `"use client"` if it uses
   state, effects, or event handlers.
2. State: read/write through `frontend/contexts/` (ApiKey / Research). Don't keep
   research state local if it must persist across navigation.
3. Types from `frontend/lib/types.ts`; backend calls through `frontend/lib/api.ts`.
4. Styling: Tailwind + the tokens/classes in `frontend/app/globals.css`
   (`card`, `btn`, `input`, `chip`, `--accent`, ...). Don't invent a new color system.
5. Use it from a page in `frontend/app/` (or from another component).

Verify: `cd frontend && npm run typecheck` (and `npm run dev` to see it).
