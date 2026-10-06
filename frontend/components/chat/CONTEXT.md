# frontend/components/chat -- the assistant chat UI

One job: render the conversation and the live turn loop. Reads chat state from
ChatContext; streams come from `lib/api.streamChat`.

## What's here
- `ChatWindow.tsx` -- the main view: message list, input, model selector, memory panel.
- `TurnTimeline.tsx` -- the live phases + memory + tool cards for one assistant turn.
- `PhaseBadge.tsx` -- a colored badge per phase.
- `ToolCallCard.tsx` -- one tool call (args + result, collapsible).
- `MemoryPanel.tsx` -- read-only facts + counts + recent tool runs (GET /memory, /trace).

## Rules
- Read/write turn state via `../../contexts/ChatContext` (`useChat`); don't hold it locally.
- Event shapes come from `../../lib/chatTypes` (mirror of the turn contract).
- Style with Tailwind + the tokens in `../../app/globals.css`.

## Where to add things
- A new turn-event rendering -> fold it into `ChatContext` activity + a component here.

## Links
- Turn contract: `../../../_shared/agent-turn-contract.md` . Parent: `../CONTEXT.md`
