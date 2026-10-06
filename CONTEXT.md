# Deep Research Studio -- System Context

One sentence: a user asks a question, the backend plans sub-questions, researches
each one against the live web, and streams a final cited report; the frontend
renders every stage as it arrives.

## The pipeline (full spec: `_shared/research-workflow.md`)
```
question --> 01 PLAN --> 02 RESEARCH (loop per sub-question) --> 03 REPORT
             (LLM)        (web search + LLM synthesis)            (LLM, streamed)
```
Each stage emits SSE events to the client. Stages are code-orchestrated in
`backend/app/services/research.py`; there is no mid-pipeline branching.

## How the two apps connect
```
frontend (browser)  --POST /research/stream (query, provider, model, api_key)-->  backend
       ^                                                                             |
       +---------------- text/event-stream of JSON events ----------------------------+
```
- The browser holds the user's API keys (localStorage) and sends one per request.
- The backend holds no keys and no database. It is stateless.
- Both sides agree on the event schema in `_shared/api-contract.md` -- change it in
  one place, then update both apps.

## Layer map (ICM)
| Layer | File(s) | Question it answers |
|---|---|---|
| 0 | `CLAUDE.md` | Where am I? |
| 1 | this file | Where do I go? |
| 2 | `backend/CONTEXT.md`, `frontend/CONTEXT.md`, `*/CONTEXT.md` | What do I do here? |
| 3 | `_config/`, `_shared/`, `planning/`, `docs/`, `ops/` | What rules apply? |
| 4 | `backend/app/`, `frontend/app/` + `components/` | What am I working with? |

## Status
Build status and what is done live in `_config/status.md`.
