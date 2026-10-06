# backend/evals/cases -- eval cases

One job: hold eval cases as JSONL, one case per line.

## What's here
- `basic.jsonl` -- `{id, message, expect_tool?}` cases (remember, calendar, greeting).

## Format
`{"id": "...", "message": "...", "expect_tool": "tool_name" | null}`

## Where to add a case
Add a line to `basic.jsonl` or a new `*.jsonl` here; `../run.py` loads them all.

## Links
- Parent: `../CONTEXT.md`
