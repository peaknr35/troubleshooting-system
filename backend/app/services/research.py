"""The deep-research pipeline: plan -> research (loop) -> streamed report.

Implemented as a single async generator yielding ResearchEvents. See
../../_shared/research-workflow.md for the spec. No framework; the control flow
is readable top-to-bottom on purpose (ICM invariant 9).
"""
from __future__ import annotations

import json
import logging
import re
from typing import AsyncIterator

from ..config import get_settings
from ..models.research import EventFactory, ResearchEvent, ResearchRequest, Source
from ..providers.base import LLMClient, ProviderError
from .search import web_search

logger = logging.getLogger(__name__)

PLAN_SYSTEM = (
    "You are a meticulous research planner. Given a user's question, break it into "
    "a small set of focused, independently-researchable sub-questions that together "
    "fully answer it. Prefer specific, non-overlapping angles. "
    'Respond with ONLY a JSON array of strings, e.g. ["...", "..."]. No prose.'
)

SYNTH_SYSTEM = (
    "You are a careful research analyst. Using the provided web search results, "
    "write a concise, factual answer to the sub-question. Ground claims in the "
    "sources and cite them inline using their URL in parentheses. If the sources "
    "are thin or missing, say so and answer cautiously from general knowledge. "
    "Keep it to a few tight paragraphs."
)

REPORT_SYSTEM = (
    "You are an expert report writer. Synthesize the research findings into a "
    "clear, well-structured markdown report that answers the original question. "
    "Use: a short executive summary, themed sections with ## headings, and a brief "
    "conclusion. Preserve inline source citations where relevant. Be objective and "
    "do not invent facts beyond the findings."
)


def _plan_user(query: str, n: int) -> str:
    return f"Question: {query}\n\nProduce at most {n} sub-questions as a JSON array of strings."


def _sources_block(sources: list[Source]) -> str:
    if not sources:
        return "(no web search results were available)"
    lines = []
    for i, s in enumerate(sources, 1):
        lines.append(f"[{i}] {s.title}\nURL: {s.url}\n{s.snippet}")
    return "\n\n".join(lines)


def _synth_user(subquestion: str, sources: list[Source]) -> str:
    return (
        f"Sub-question: {subquestion}\n\n"
        f"Web search results:\n{_sources_block(sources)}\n\n"
        "Write the grounded answer now."
    )


def _report_user(query: str, findings: list[dict]) -> str:
    parts = [f"Original question: {query}\n", "Research findings:\n"]
    for i, f in enumerate(findings, 1):
        parts.append(f"### Finding {i}: {f['subquestion']}\n{f['summary']}\n")
    parts.append("\nWrite the final markdown report now.")
    return "\n".join(parts)


def _parse_subquestions(raw: str, fallback_query: str, n: int) -> list[str]:
    """Extract a JSON array of strings from the model output, robustly."""
    text = (raw or "").strip()
    match = re.search(r"\[.*\]", text, re.DOTALL)
    candidate = match.group(0) if match else text
    try:
        data = json.loads(candidate)
        if isinstance(data, list):
            subs = [str(x).strip() for x in data if str(x).strip()]
            if subs:
                return subs[:n]
    except (json.JSONDecodeError, TypeError):
        pass
    # Fallback: split numbered/bulleted lines, else use the question itself.
    lines = [
        re.sub(r"^\s*(?:[-*\d.)]+)\s*", "", ln).strip()
        for ln in text.splitlines()
        if ln.strip()
    ]
    lines = [ln for ln in lines if len(ln) > 8]
    return (lines[:n] if lines else [fallback_query])


async def run_research(req: ResearchRequest, client: LLMClient) -> AsyncIterator[ResearchEvent]:
    ev = EventFactory()
    settings = get_settings()
    try:
        # --- 01 PLAN ---
        yield ev.status("planning", "Planning the research...", 0.0)
        raw_plan = await client.complete(
            PLAN_SYSTEM, _plan_user(req.query, req.max_subquestions), max_tokens=700
        )
        subquestions = _parse_subquestions(raw_plan, req.query, req.max_subquestions)
        yield ev.plan(subquestions)

        # --- 02 RESEARCH (loop) ---
        findings: list[dict] = []
        all_sources: list[Source] = []
        seen_urls: set[str] = set()
        total = len(subquestions)
        for i, subq in enumerate(subquestions):
            yield ev.status("researching", f"Researching: {subq}", i / max(total, 1))
            sources: list[Source] = []
            if req.search:
                sources = await web_search(subq, settings.search_max_results)
                yield ev.sources(i, subq, sources)
            summary = await client.complete(
                SYNTH_SYSTEM, _synth_user(subq, sources), max_tokens=900
            )
            findings.append({"subquestion": subq, "summary": summary, "sources": sources})
            for s in sources:
                if s.url and s.url not in seen_urls:
                    seen_urls.add(s.url)
                    all_sources.append(s)
            yield ev.finding(i, subq, summary, sources)

        # --- 03 REPORT (streamed) ---
        yield ev.status("report", "Writing the final report...", 1.0)
        chunks: list[str] = []
        async for chunk in client.stream(
            REPORT_SYSTEM, _report_user(req.query, findings), max_tokens=8000
        ):
            chunks.append(chunk)
            yield ev.token(chunk)
        report_text = "".join(chunks).strip()
        yield ev.report(report_text, all_sources)
        yield ev.done()

    except ProviderError as exc:
        logger.warning("provider error during research: %s", exc.message)
        yield ev.error(exc.message, code=exc.code)
    except Exception as exc:  # pragma: no cover - defensive
        logger.exception("research pipeline failed")
        yield ev.error(f"Internal error: {exc}", code="internal")
