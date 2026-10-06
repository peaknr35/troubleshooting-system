"""deep_research tool -- the existing Deep Research Studio pipeline, now a tool.
Reuses services.research.run_research unchanged."""
from __future__ import annotations

from .base import ToolSpec


def make_deep_research(client) -> ToolSpec:
    async def deep_research(query: str) -> str:
        """Run a multi-step web research workflow and return a cited markdown report.
        Use when a question needs current, well-sourced information."""
        from ..models.research import Provider, ResearchRequest
        from ..services.research import run_research
        provider = client.provider if client.provider in ("openai", "anthropic", "kimi") else "openai"
        req = ResearchRequest(
            query=query, provider=Provider(provider), api_key="x" * 8,
            max_subquestions=3, search=True,
        )
        report = ""
        async for ev in run_research(req, client):
            if ev.type == "report":
                report = (ev.data or {}).get("report", "")
            elif ev.type == "error":
                return f"deep_research error: {ev.message}"
        return report or "No report produced."

    return ToolSpec(
        "deep_research", "Deep multi-step web research producing a cited report.", deep_research
    )
