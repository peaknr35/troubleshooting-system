# backend/app/tools -- the tool registry (agent "nodes")

One job: the practical things the agent can do. Each tool is a typed async function
returning a string observation; the SAME function feeds the manual backend (prompt
describes it) and PydanticAI (infers its schema). Mirrors ../../../_shared/tools.md.

## What's here
- `base.py` -- `ToolSpec` (name, description, typed func), `ToolResult`, `ToolRegistry`
  (+ `manual_catalog()` for the prompt).
- `registry.py` -- `build_registry(client)` assembles the set for one turn.
- `web_search.py` -- wraps `services/search.web_search`.
- `deep_research.py` -- wraps `services/research.run_research` (the DRS pipeline).
- `calendar.py` -- `calendar_create` / `calendar_list` over the local events table.
- `file_tools.py` -- `file_read` / `file_write`, sandboxed to `APP_FILE_ROOT`
  (toggle `APP_FILE_UNRESTRICTED=1` to widen; path-escape check always on).
- `memory_tools.py` -- `remember` / `recall` (explicit long-term memory).

## Rules
- A tool returns a short string the model can read; it never raises to the loop
  (`ToolSpec.run` traps errors into an observation).
- Tools that need the LLM (deep_research) receive the client via `build_registry`.
- Keep args simple + typed so both backends can call them; document them in the docstring.

## Where to add a tool
See `../../../_templates/new-tool.md`: write `make_<name>()` in a file here, register
it in `registry.py`, and (if it needs a new capability) add a `_shared/tools.md` note.

## Links
- Tool contract: `../../../_shared/tools.md` . Parent: `../CONTEXT.md`
