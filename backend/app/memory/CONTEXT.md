# backend/app/memory -- the single local brain (SQLite)

One job: persist and recall what is worth keeping, in one local SQLite file. No
server, no external DB. Mirrors ../../../_shared/memory-schema.md.

## What's here
- `schema.sql` -- the tables: conversations, turns, facts, skills, tool_runs, events.
- `db.py` -- `connect()` (opens + inits the DB at ~/.assistant/state.db / `APP_DB_PATH`).
- `store.py` -- all operations: conversations/turns (episodic), facts + `recall()`
  (semantic), `add_tool_run`/`recent_tool_runs` (trace), calendar events, skills,
  `counts()`.

## Rules
- Connections are opened per call; the agent loop wraps store calls in
  `asyncio.to_thread` so SQLite never blocks the event loop.
- `recall()` is simple keyword LIKE matching today; swap to FTS5/sqlite-vec later
  without changing callers.
- Facts are de-duplicated by text. `source` is `auto` (consolidation gate) or
  `explicit` (the user said "remember that...").

## Where to add things
- A new table -> `schema.sql` (+ mirror in `_shared/memory-schema.md`) + functions here.
- A new memory query -> a function in `store.py` (keep SQL in this folder only).

## Links
- Schema contract: `../../../_shared/memory-schema.md` . Parent: `../CONTEXT.md`
