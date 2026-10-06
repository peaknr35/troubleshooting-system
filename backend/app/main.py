"""FastAPI application entrypoint."""
from __future__ import annotations

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .config import get_settings
from .logging_config import configure_logging
from .routes import health, research

settings = get_settings()
configure_logging(settings.log_level)

app = FastAPI(
    title=settings.app_name,
    version=settings.version,
    description="Streaming deep-research API (OpenAI, Anthropic, Kimi K2). Bring your own key.",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.origins_list,
    allow_methods=["*"],
    allow_headers=["*"],
    allow_credentials=False,
)

app.include_router(health.router)
app.include_router(research.router)


@app.get("/", tags=["meta"])
async def root() -> dict:
    return {
        "service": settings.app_name,
        "version": settings.version,
        "docs": "/docs",
        "health": "/health",
        "providers": "/providers",
        "research": "POST /research/stream",
    }
