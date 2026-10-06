# Agent Turn Contract (single source of truth)

`POST /chat/stream` runs one turn and streams SSE TurnEvents. Mirrored by
`backend/app/models/chat.py` and `frontend/lib/chatTypes.ts` -- change here first.

## Request body
```json
{ "message": "str 1..8000 (required)",
  "provider": "openai | anthropic | kimi (required)",
  "model": "str, optional (provider default if omitted)",
  "api_key": "str >= 8 (required) -- never stored",
  "conversation_id": "int, optional (continue a thread)",
  "backend": "pydantic_ai | manual, optional (override default)" }
```

## Response: text/event-stream (`data: <json>\n\n`)
Every event:
```json
{ "type": "...", "phase": "...", "name": "...", "message": "...", "data": {...},
  "turn_id": "uuid", "timestamp": "ISO-8601" }
```

| type | phase | meaning | data |
|---|---|---|---|
| `phase` | receive/recall/reason/act/observe/remember/reply/done/error | stage marker | - |
| `memory` | recall / remember | memories read or saved | `{items: [str]}` (name = recall/save) |
| `tool_call` | act | a tool is being called | `{args}` (name = tool) |
| `tool_result` | observe | a tool returned | `{args, result, ok}` (name = tool) |
| `token` | reply | streamed reply chunk (optional) | `{text}` |
| `final` | reply | the final answer | `message` = answer |
| `error` | error | failure; stream ends | `{code}` (message = text) |
| `done` | done | turn complete | `{conversation_id, turn_id}` |

## Order
`receive -> recall -> (reason -> act -> observe)* -> remember -> final -> done`.
On failure: a single `error` event, then the stream closes.

## Read-only endpoints (dashboard)
`GET /memory -> {facts, counts}` . `GET /trace -> {tool_runs}`.
