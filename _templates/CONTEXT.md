# _templates -- copy-to-create starters

One job: hold blank starters so a new unit of work begins as a copy, not a blank
page (ICM invariant 10). Nothing here runs or ships; these are stamps.

## What's here
- `folder-CONTEXT.template.md` -- the per-folder contract starter (stamp a new folder's CONTEXT.md)
- `new-provider.md` -- end-to-end checklist to add an LLM provider to the backend + UI
- `new-endpoint.md` -- add a backend HTTP/SSE endpoint and keep the contract in sync
- `new-component.md` -- add a frontend React component/feature
- `decision-record.template.md` -- starter for `planning/decisions/YYYY-MM-DD_title.md`

## How to use
Copy a file to its destination and fill the <angle-bracket> placeholders, e.g.:
`cp _templates/folder-CONTEXT.template.md backend/app/newthing/CONTEXT.md`

## Rules
- Templates stay generic -- never reference run-specific data.
- When a real pattern changes (e.g. how a provider is wired), update the matching
  template here so the next copy is correct.

## Links
- Root router: `../CLAUDE.md` · Contracts these point at: `../_shared/`
