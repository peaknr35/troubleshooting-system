"""Web search tool. DuckDuckGo via the `ddgs` package -- no API key required.

Degrades gracefully: if no search backend is installed or a query fails, returns
an empty list and logs a warning. The research service then proceeds without
sources for that sub-question.
"""
from __future__ import annotations

import asyncio
import logging

from ..models.research import Source

logger = logging.getLogger(__name__)


def _ddgs_class():
    try:
        from ddgs import DDGS  # current package name
        return DDGS
    except ImportError:
        try:
            from duckduckgo_search import DDGS  # older package name
            return DDGS
        except ImportError:
            return None


async def web_search(query: str, max_results: int = 5) -> list[Source]:
    ddgs_cls = _ddgs_class()
    if ddgs_cls is None:
        logger.warning("no search backend installed (pip install ddgs); skipping search")
        return []

    def _run() -> list[Source]:
        out: list[Source] = []
        with ddgs_cls() as ddgs:
            for r in ddgs.text(query, max_results=max_results):
                out.append(
                    Source(
                        title=(r.get("title") or "").strip(),
                        url=(r.get("href") or r.get("url") or "").strip(),
                        snippet=(r.get("body") or r.get("snippet") or "").strip(),
                    )
                )
        return out

    try:
        return await asyncio.to_thread(_run)
    except Exception as exc:  # network/rate-limit/parsing -- never fatal
        logger.warning("web_search failed for query %r: %s", query, exc)
        return []
