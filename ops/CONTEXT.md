# Operations

Deploy scripts and runbooks.

## Infrastructure
- Local: `docker-compose.yml` runs backend (8080) + frontend (3000).
- Backend prod: Google Cloud Run (container listens on `$PORT`).
- Frontend prod: any Node host / Vercel / Cloud Run (set `NEXT_PUBLIC_BACKEND_URL`).

## Contents
- `deploy/cloud-run-backend.md` -- step-by-step Cloud Run deploy
- `deploy/deploy-backend.sh` -- scripted build + deploy (idempotent)
- `scripts/run-local.md` -- local run recipes (Docker and bare-metal)

## Rules
- Deploy scripts must be safe to run twice (idempotent).
- Cloud Run: generous timeout + concurrency for long research runs.
