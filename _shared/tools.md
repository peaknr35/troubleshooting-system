# Tools (single source of truth)

A tool is a typed async function returning a string observation, wrapped in a
`ToolSpec` (`backend/app/tools/base.py`) and assembled by `build_registry`
(`backend/app/tools/registry.py`). The SAME function feeds both agent backends
(manual prompt-JSON + PydanticAI).

## Built-in tools
| tool | args | does |
|---|---|---|
| `web_search` | `query, max_results=5` | live web search (DuckDuckGo) |
| `deep_research` | `query` | the Deep Research Studio pipeline -> cited report |
| `remember` | `text` | save a fact to memory (explicit) |
| `recall` | `query` | search memory |
| `calendar_list` | `start="", end=""` | list local calendar events |
| `calendar_create` | `title, start, end="", notes=""` | create a local event (ISO datetimes) |
| `file_read` | `path` | read a workspace text file (sandboxed) |
| `file_write` | `path, content` | write a workspace text file (sandboxed) |

## File safety
`file_read` / `file_write` resolve paths under `APP_FILE_ROOT`
(default `~/.assistant/workspace`). `APP_FILE_UNRESTRICTED=1` widens to the whole
filesystem; the path-escape check is always applied relative to the root otherwise.

## Adding a tool
See `../_templates/new-tool.md`.

## Google calendar (optional)
Set `APP_GOOGLE_CALENDAR=1` + `APP_GOOGLE_TOKEN_FILE` to mirror `calendar_create` to
Google Calendar (needs `pip install google-api-python-client google-auth`). The local
SQLite calendar stays the source of truth; sync is best-effort and failures are non-fatal.
