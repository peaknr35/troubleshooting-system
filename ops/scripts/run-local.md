# Run locally

## Full stack (Docker)
```bash
docker compose up --build        # frontend :3000, backend :8080
docker compose down              # stop
```

## Backend only
```bash
cd backend
uvicorn app.main:app --reload --port 8080
# health:
curl http://localhost:8080/health
# smoke a stream (replace sk-...):
curl -N -X POST http://localhost:8080/research/stream \
  -H 'Content-Type: application/json' \
  -d '{"query":"how does HTTP SSE work","provider":"openai","api_key":"sk-...","max_subquestions":2}'
```

## Frontend only
```bash
cd frontend
npm install
npm run dev                       # Turbopack, http://localhost:3000
```

## Tests
```bash
cd backend && pytest
cd frontend && npm run typecheck
```

## Troubleshooting
- **CORS error in the browser:** set `APP_CORS_ORIGINS=http://localhost:3000` for
  the backend (docker-compose already does this).
- **Frontend `next build` fails with EISDIR on Windows E: drive:** build via
  Docker or from a C: path; `npm run dev` (Turbopack) is unaffected. See README.
- **No sources appear:** DuckDuckGo may be rate-limiting; the report still runs
  from the model's knowledge, or toggle off "Live web search".
