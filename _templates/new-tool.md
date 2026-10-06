# Add a tool (agent capability)

Tools are typed async functions returning a string. One definition serves both the
manual and PydanticAI backends.

1. `backend/app/tools/<name>.py` -- write a factory:
   ```python
   from .base import ToolSpec
   def make_<name>() -> ToolSpec:
       async def <name>(arg1: str, arg2: int = 3) -> str:
           """One-line description the model sees."""
           ...                      # do the work; return a short string observation
           return "result"
       return ToolSpec("<name>", "One-line description.", <name>)
   ```
   - Keep args simple + typed (PydanticAI builds the schema from the signature).
   - Never raise to the loop for expected errors -- return an explanatory string.
   - If it needs the LLM, take the client via `build_registry` (see `deep_research.py`).
   - If it touches files, resolve paths through `file_tools.resolve_path` (sandbox).
2. `backend/app/tools/registry.py` -- register it in `build_registry()`.
3. `_shared/tools.md` -- add the row.
4. `backend/tests/test_agent.py` -- add it to the registry test (+ a behavior test).

Verify: `cd backend && pytest`.
