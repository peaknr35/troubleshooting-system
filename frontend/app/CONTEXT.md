# frontend/app -- Next.js App Router

One job: routing, the root layout, and the pages. The client state providers mount
here so state survives navigation.

## What's here
- `layout.tsx` -- root layout + metadata; wraps everything in `Providers`.
- `providers.tsx` -- mounts `ApiKeyProvider` + `ResearchProvider` + `Header` above
  the pages, so research/key state persists across route changes.
- `page.tsx` -- the main research view (renders `ResearchInterface`).
- `compare/` -- the `/compare` route (its own CONTEXT).
- `globals.css` -- theme tokens (light/dark) + component classes (`card`, `btn`,
  `input`, `chip`) + markdown styles. The one place colors are defined.

## Rules
- Pages are thin: they render a component from `../components/`. Logic lives there.
- State that must survive navigation lives in a context in `providers.tsx`, not a page.
- New styles/colors go in `globals.css` tokens, not inline hex.

## Where to add a page
Create `app/<route>/page.tsx` that renders a component from `../components/`.

## Links
- Parent: `../CONTEXT.md` . Components: `../components/CONTEXT.md`
