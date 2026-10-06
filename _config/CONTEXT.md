# _config -- factory settings (ICM Layer 3)

One job: the stable facts about the project that rarely change per run. Reference
material, not runtime config (runtime config is env vars with the `APP_` prefix).

## What's here
- `project.md` -- what this project is, who it is for, principles, non-goals.
- `tech-stack.md` -- languages, frameworks, SDKs, verified model IDs.
- `conventions.md` -- naming + code conventions for both apps.
- `status.md` -- the human-readable build tracker.

## Rules
- Facts live here once; other files link rather than copy.
- No secrets. Runtime secrets are env vars, never committed.

## Where to add things
- A durable project fact -> the matching file here.
- A per-run/runtime setting -> `backend/app/config.py` (env, `APP_` prefix), not here.

## Links
- Root router: `../CLAUDE.md` . Contracts: `../_shared/`
