# skills -- user-editable procedures the agent can follow

One job: reusable "how to do X" procedures, in plain markdown, surfaced to the agent
in its system prompt. Edit or add files here; no code change needed.

## What's here
- `daily-standup.md` -- produce a short daily standup from memory + calendar.
- `summarize-url.md` -- summarize a page/topic using web_search / deep_research.
- (add your own `*.md`)

## Format
A skill is one markdown file: the first heading is its name; the body is the
procedure (reference tools by name). Loaded by `backend/app/agent/skills.py`
(`load_skills()`); `CONTEXT.md` is skipped.

## Rules
- Keep a skill to a few concrete steps; name the tools it should use.
- Skills are guidance, not code -- the agent still decides when to apply them.

## Where to add a skill
Copy `../_templates/new-skill.md` to `<name>.md` here.

## Links
- Loader: `../backend/app/agent/skills.py` . Root: `../CLAUDE.md`
