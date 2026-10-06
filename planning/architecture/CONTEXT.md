# planning/architecture -- how the pieces fit

One job: durable architecture docs (component map, data flow) referenced when building.

## What's here
- `system-overview.md` -- component map, request data flow, statelessness, compare mode.

## Rules
- Describe the system as it IS; when architecture changes, update the doc in the same change.

## Where to add things
- A new architecture doc -> a `kebab-case.md` here. For a point-in-time choice, write a
  record in `../decisions/` instead.

## Links
- Parent: `../CONTEXT.md` . Decisions: `../decisions/CONTEXT.md`
