# frontend/components -- React components

One job: all the UI pieces. Pages compose these; components read/write shared state
through contexts.

## What's here
- `Header.tsx` -- top nav + opens the Keys modal.
- `ResearchInterface.tsx` -- the main view: input, options, live results.
- `CompareView.tsx` -- multi-model compare grid.
- `ApiKeyManager.tsx` -- the keys modal (save/import/export/clear).
- `ModelSelector.tsx` -- provider + model dropdowns with a key-status chip.
- `ProgressStages.tsx` -- planning/researching/report stepper + progress bar.
- `FindingCard.tsx` -- one expandable sub-question finding + its sources.
- `SourceList.tsx` -- a list of sources (title, link, snippet).
- `ReportView.tsx` -- the final report + export menu + sources.
- `ExportMenu.tsx` -- copy-for-Docs + create Google Doc.
- `Markdown.tsx` -- react-markdown wrapper used for findings + report.

## Rules
- PascalCase filenames; add `"use client"` if it uses state/effects/handlers.
- Read/write shared state via `../contexts/` -- do not hold persistable research
  state locally.
- Style with Tailwind + the tokens/classes in `../app/globals.css`. No new palettes.

## Where to add a component
See `../../_templates/new-component.md`.

## Links
- Contexts: `../contexts/CONTEXT.md` . Lib: `../lib/CONTEXT.md` . Parent: `../CONTEXT.md`
