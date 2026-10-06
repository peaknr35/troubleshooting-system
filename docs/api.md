# API Reference

Base URL (local): `http://localhost:8080`. This mirrors the canonical contract in
[`../_shared/api-contract.md`](../_shared/api-contract.md).

## GET /health  (also HEAD)
```json
{ "status": "ok", "service": "Deep Research Studio API", "version": "0.1.0" }
```

## GET /providers
Returns the provider/model catalog for populating UI dropdowns (no key required).

## POST /research/stream
Runs the research pipeline and streams Server-Sent Events.

Request body:
```json
{
  "query": "What are the tradeoffs of serverless vs containers?",
  "provider": "openai",            // openai | anthropic | kimi
  "model": "gpt-5.1",              // optional; provider default if omitted
  "api_key": "sk-...",             // your key; never stored
  "max_subquestions": 4,            // optional, 1..8
  "search": true                    // optional, live web search
}
```

Response: `Content-Type: text/event-stream`. Each frame is `data: <json>\n\n`.
Event JSON:
```json
{ "type": "...", "stage": "...", "message": "...", "data": {...},
  "research_id": "uuid", "timestamp": "ISO-8601" }
```
Event order: `status(planning)` → `plan` → per sub-question
`status(researching)` → `sources` → `finding` → `status(report)` →
many `token` → `report` → `done`. On failure: one `error` event.

### curl example
```bash
curl -N -X POST http://localhost:8080/research/stream \
  -H 'Content-Type: application/json' \
  -d '{"query":"best practices for FastAPI logging","provider":"openai","api_key":"sk-...","max_subquestions":3}'
```

### Errors
- `422` — request failed validation (bad/short query, missing/short `api_key`,
  unknown `provider`).
- In-stream `error` event with `data.code`: `auth` (provider rejected the key),
  `provider` (upstream error), `search`, `internal`.
