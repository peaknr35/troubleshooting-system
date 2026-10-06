"""Anthropic (Claude) client.

Multi-model safety: the user may select ANY Anthropic model, so we do NOT send
thinking, output_config.effort, or temperature. Thinking-on models (Opus 5.x,
Sonnet 5.x) reject a custom temperature, and Haiku rejects the effort/adaptive
settings others need -- omitting all three keeps one code path valid everywhere.
We stream and read text_stream.
"""
from __future__ import annotations

import logging
from typing import AsyncIterator

import anthropic
from anthropic import AsyncAnthropic

from ..config import get_settings
from .base import ProviderError

logger = logging.getLogger(__name__)


class AnthropicClient:
    def __init__(self, api_key: str, model: str) -> None:
        self.provider = "anthropic"
        self.model = model
        self._client = AsyncAnthropic(
            api_key=api_key, timeout=get_settings().request_timeout, max_retries=1
        )

    def _translate(self, exc: Exception) -> ProviderError:
        if isinstance(exc, anthropic.AuthenticationError):
            return ProviderError("Invalid or unauthorized API key.", code="auth", status=401)
        if isinstance(exc, anthropic.PermissionDeniedError):
            return ProviderError("API key lacks permission for this model.", code="auth", status=403)
        if isinstance(exc, anthropic.RateLimitError):
            return ProviderError("Rate limited by the provider. Try again shortly.", code="provider", status=429)
        if isinstance(exc, anthropic.APIStatusError):
            return ProviderError(f"Provider error ({exc.status_code}).", code="provider", status=exc.status_code)
        if isinstance(exc, anthropic.APIConnectionError):
            return ProviderError("Could not reach the provider.", code="provider")
        return ProviderError(f"Unexpected provider error: {exc}", code="provider")

    async def complete(self, system: str, user: str, *, max_tokens: int = 2000) -> str:
        try:
            async with self._client.messages.stream(
                model=self.model, max_tokens=max_tokens, system=system,
                messages=[{"role": "user", "content": user}],
            ) as stream:
                message = await stream.get_final_message()
            return "".join(
                b.text for b in message.content if getattr(b, "type", None) == "text"
            ).strip()
        except Exception as exc:
            raise self._translate(exc) from exc

    async def stream(self, system: str, user: str, *, max_tokens: int = 4000) -> AsyncIterator[str]:
        try:
            async with self._client.messages.stream(
                model=self.model, max_tokens=max_tokens, system=system,
                messages=[{"role": "user", "content": user}],
            ) as stream:
                async for text in stream.text_stream:
                    yield text
        except Exception as exc:
            raise self._translate(exc) from exc
