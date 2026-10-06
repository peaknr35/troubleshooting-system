"""POST /research/stream -- runs the pipeline and streams SSE events."""
from __future__ import annotations

import logging

from fastapi import APIRouter
from fastapi.responses import StreamingResponse

from ..models.research import EventFactory, ResearchRequest
from ..providers.base import ProviderError, build_client
from ..services.research import run_research

logger = logging.getLogger(__name__)
router = APIRouter(tags=["research"])


@router.post("/research/stream")
async def research_stream(req: ResearchRequest) -> StreamingResponse:
    async def event_stream():
        try:
            client = build_client(req.provider, req.api_key, req.model)
        except ProviderError as exc:
            yield EventFactory().error(exc.message, code=exc.code).to_sse()
            return
        logger.info(
            "research start provider=%s model=%s subq=%s search=%s",
            req.provider.value, req.model or "(default)", req.max_subquestions, req.search,
        )
        async for event in run_research(req, client):
            yield event.to_sse()

    headers = {
        "Cache-Control": "no-cache",
        "Connection": "keep-alive",
        "X-Accel-Buffering": "no",  # disable proxy buffering so events flush live
    }
    return StreamingResponse(event_stream(), media_type="text/event-stream", headers=headers)
