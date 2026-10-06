# Deep Research Studio

A bring-your-own-key deep research app: a FastAPI backend that runs a real
plan -> research -> report workflow and streams progress live, and a Next.js
frontend that renders the research as it happens. Supports OpenAI, Anthropic,
and Kimi K2. No API keys are ever stored on the server.

## Where things live
| Path | What it holds |
|---|---|
| `FILE-MAP.md` | Generated index of every file (refresh: `ops/scripts/build-file-map.sh`) |
| `_config/` | Factory settings: what this project is, tech stack, conventions, build status |
| `_shared/` | Cross-cutting contracts both apps obey: API/SSE schema, provider matrix, workflow spec |
| `_templates/` | Copy-to-create starters: new provider, endpoint, component, decision record |
| `planning/` | Feature specs, architecture, decision records |
| `backend/` | FastAPI app (code, tests, Dockerfile) |
| `frontend/` | Next.js app (code, Dockerfile) |
| `docs/` | API docs, setup guide, changelog |
| `ops/` | Deploy scripts and runbooks (Docker, Cloud Run) |

## Route by intent
| Task | Go to | Read first |
|---|---|---|
| Get oriented / find any file | `FILE-MAP.md` | this file -> FILE-MAP.md |
| Understand the whole system | `CONTEXT.md` | this file -> CONTEXT.md |
| Work inside any folder | that folder's `CONTEXT.md` | it states purpose, contents, rules, where to add things |
| Change the SSE event shape | `_shared/api-contract.md` | then update BOTH backend + frontend |
| Add a provider / endpoint / UI piece | `_templates/` | the matching checklist, then the folder CONTEXT |
| Change the research steps | `_shared/research-workflow.md` -> `backend/app/services/research.py` | - |
| Work on the API | `backend/CONTEXT.md` | - |
| Work on the UI | `frontend/CONTEXT.md` | - |
| Deploy or run locally | `ops/CONTEXT.md` | - |
| Record a decision | `planning/decisions/` (copy the template) | - |
| Check what is done | `_config/status.md` | - |

## Tech stack (summary; full detail in `_config/tech-stack.md`)
- Backend: Python 3.12, FastAPI, Uvicorn, Pydantic v2, SSE streaming
- LLM SDKs: `openai` (OpenAI + Kimi via base_url), `anthropic` (Claude)
- Frontend: Next.js 15 (App Router), TypeScript, Tailwind CSS
- Containers: Docker + docker-compose; backend deploys to Google Cloud Run

## Commands
| Action | Command |
|---|---|
| Run both apps locally | `docker compose up --build` |
| Backend dev server | `cd backend && uvicorn app.main:app --reload --port 8080` |
| Backend tests | `cd backend && pytest` |
| Frontend dev server | `cd frontend && npm run dev` |
| Refresh the file index | `bash ops/scripts/build-file-map.sh` |

## The one rule
Secrets stay client-side. The server never persists an API key -- keys arrive per
request and live only for that request. Never add server-side key storage.

## Conventions
- **Every folder has a `CONTEXT.md`** -- its identity, contents, rules, and where to
  add things. Open it first when you enter a folder. The root keeps the only
  `CLAUDE.md` (this file); folders never get their own entry file.
- Folders `kebab-case/`; contracts `CONTEXT.md`; config/docs `kebab-case.md`;
  decisions `YYYY-MM-DD_title.md`; Python `snake_case.py`; React `PascalCase.tsx`.
