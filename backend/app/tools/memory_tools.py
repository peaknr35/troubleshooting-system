"""remember / recall tools -- explicit user control over long-term memory."""
from __future__ import annotations

import asyncio

from .base import ToolSpec


def make_remember() -> ToolSpec:
    async def remember(text: str) -> str:
        """Save an important fact or preference to long-term memory."""
        from ..memory import store
        await asyncio.to_thread(store.add_fact, text, "fact", "explicit")
        return f"Remembered: {text}"

    return ToolSpec(
        "remember", "Save an important fact or preference to long-term memory.", remember
    )


def make_recall() -> ToolSpec:
    async def recall(query: str) -> str:
        """Search long-term memory for facts relevant to the query."""
        from ..memory import store
        rows = await asyncio.to_thread(store.recall, query, 6)
        if not rows:
            return "No relevant memories."
        return "\n".join(f"- {r['text']}" for r in rows)

    return ToolSpec("recall", "Search long-term memory for relevant facts.", recall)
