# Architecture: System Overview

```
                         Browser (Next.js)
  +-----------------------------------------------------------+
  |  ApiKeyContext (localStorage)   ResearchContext (state)   |
  |        |                               |                  |
  |  ModelSelector / ApiKeyManager   ResearchInterface        |
  |        |                               |                  |
  |        +--------- lib/api.ts (fetch + SSE reader) --------+|
  +----------------------------|------------------------------+
                               | POST /research/stream (SSE)
                               v
                     FastAPI (stateless)
  +-----------------------------------------------------------+
  | routes/research.py  --> services/research.py (generator)  |
  |                              |            |                |
  |                   providers/ (LLM)   services/search.py    |
  |                   openai|anthropic|kimi   (DuckDuckGo)     |
  +-----------------------------------------------------------+
          |                |                 |
       OpenAI          Anthropic         Moonshot (Kimi)
```

## Data flow (one request)
1. Browser sends `{query, provider, model, api_key, ...}`.
2. Route validates (Pydantic) and builds the provider client from the key.
3. `run_research()` yields events; the route serializes each to `data: {...}\n\n`.
4. Browser's SSE reader dispatches events into `ResearchContext`, which renders.

## Statelessness
No DB, no key storage. A request's key lives only in the client object for that
request's lifetime. Horizontal scale is trivial (Cloud Run `max-instances`).

## Compare mode
The frontend fires N independent `/research/stream` requests (one per model) and
renders N columns, each with its own progress + timing. The backend is unchanged;
concurrency is a client concern.
