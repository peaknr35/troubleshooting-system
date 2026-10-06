# ops/scripts -- operational scripts & runbooks

One job: local run recipes and maintenance scripts.

## What's here
- `run-local.md` -- run the stack locally (Docker + bare-metal) + troubleshooting.
- `build-file-map.sh` -- regenerate the root `FILE-MAP.md` index (run from repo root).

## Rules
- Generated indexes are rebuilt by script, never hand-edited (ICM invariant 9).

## Where to add things
- A new recipe -> a `kebab-case.md`; a new maintenance script -> a `*.sh` here.

## Links
- Parent: `../CONTEXT.md` . Index it builds: `../../FILE-MAP.md`
