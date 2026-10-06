# Deep Research Studio

A bring-your-own-key deep research app: a FastAPI backend that runs a real
plan -> research -> report workflow and streams progress live, and a Next.js
frontend that renders the research as it happens. Supports OpenAI, Anthropic,
and Kimi K2. No API keys are ever stored on the server.

## Where things live
| Folder | What it holds |
|---|---|
| `_config/` | Factory settings: what this project is, tech stack, conventions, build status |
| `_shared/` | Cross-cutting contracts both apps obey: API/SSE schema, provider matrix, workflow spec |
| `planning/` | Feature specs, architecture, decision records |
| `backend/` | FastAPI app (code, tests, Dockerfile) |
| `frontend/` | Next.js app (code, Dockerfile) |
| `docs/` | API docs, setup guide, changelog |
| `ops/` | Deploy scripts and runbooks (Docker, Cloud Run) |

## Route by intent
| Task | Go to | Read first |
|---|---|---|
| Understand the whole system | `CONTEXT.md` | this file -> CONTEXT.md |
| Change the SSE event shape | `_shared/api-contract.md` | then update BOTH backend + frontend |
| Add/adjust a model or provider | `_shared/providers.md` + `backend/app/providers/` + `frontend/lib/models.ts` | - |
| Change the research steps | `_shared/research-workflow.md` -> `backend/app/services/research.py` | - |
| Work on the API | `backend/CONTEXT.md` | - |
| Work on the UI | `frontend/CONTEXT.md` | - |
| Deploy or run locally | `ops/CONTEXT.md` | - |
| Record a decision | `planning/decisions/YYYY-MM-DD_title.md` | - |
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

## The one rule
Secrets stay client-side. The server never persists an API key -- keys arrive per
request and live only for that request. Never add server-side key storage.

## Naming
Stage/working folders `kebab-case/`; contracts `CONTEXT.md`; config/docs
`kebab-case.md`; decisions `YYYY-MM-DD_title.md`; Python `snake_case.py`;
React components `PascalCase.tsx`.
