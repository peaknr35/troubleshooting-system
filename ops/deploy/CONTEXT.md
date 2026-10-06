# ops/deploy -- deployment

One job: how the backend ships to production (Cloud Run).

## What's here
- `cloud-run-backend.md` -- step-by-step Cloud Run deploy + verify.
- `deploy-backend.sh` -- idempotent scripted deploy (`PROJECT_ID`/`FRONTEND_ORIGIN` env).

## Rules
- Scripts must be safe to run twice (idempotent).
- No provider keys here -- they come from each client request.
- In production set `APP_CORS_ORIGINS` to the real frontend origin (not `*`).

## Where to add things
- A new target/runbook -> a `kebab-case.md` (or a script) here.

## Links
- Parent: `../CONTEXT.md`
