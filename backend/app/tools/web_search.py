"""web_search tool -- wraps the existing DuckDuckGo search service."""
from __future__ import annotations

from .base import ToolSpec


def make_web_search() -> ToolSpec:
    async def web_search(query: str, max_results: int = 5) -> str:
        """Search the live web. Returns titles, URLs, and snippets for the top results."""
        from ..config import get_settings
        from ..services.search import web_search as _search
        results = await _search(query, max_results or get_settings().search_max_results)
        if not results:
            return "No web results found."
        return "\n\n".join(
            f"[{i}] {s.title}\n{s.url}\n{s.snippet}" for i, s in enumerate(results, 1)
        )

    return ToolSpec(
        "web_search", "Search the live web for up-to-date information.", web_search
    )
