"""OpenAI-compatible client. Serves BOTH OpenAI and Kimi K2 (Moonshot).

Kimi differs only in base_url. Per-provider request quirks:
  - openai: newer models require max_completion_tokens and reject a custom
    temperature, so we send max_completion_tokens and no temperature.
  - kimi:   Moonshot implements the classic Chat Completions spec, so max_tokens
    and temperature are fine.
"""
from __future__ import annotations

import logging
from typing import AsyncIterator, Optional

import openai
from openai import AsyncOpenAI

from ..config import get_settings
from .base import ProviderError

logger = logging.getLogger(__name__)


class OpenAICompatibleClient:
    def __init__(self, api_key: str, model: str, *, provider: str = "openai",
                 base_url: Optional[str] = None) -> None:
        self.provider = provider
        self.model = model
        self._client = AsyncOpenAI(
            api_key=api_key, base_url=base_url,
            timeout=get_settings().request_timeout, max_retries=1,
        )

    def _params(self, system: str, user: str, max_tokens: int, stream: bool) -> dict:
        params: dict = {
            "model": self.model,
            "messages": [
                {"role": "system", "content": system},
                {"role": "user", "content": user},
            ],
            "stream": stream,
        }
        if self.provider == "openai":
            params["max_completion_tokens"] = max_tokens
        else:
            params["max_tokens"] = max_tokens
            params["temperature"] = 0.4
        return params

    def _translate(self, exc: Exception) -> ProviderError:
        if isinstance(exc, openai.AuthenticationError):
            return ProviderError("Invalid or unauthorized API key.", code="auth", status=401)
        if isinstance(exc, openai.PermissionDeniedError):
            return ProviderError("API key lacks permission for this model.", code="auth", status=403)
        if isinstance(exc, openai.RateLimitError):
            return ProviderError("Rate limited by the provider. Try again shortly.", code="provider", status=429)
        if isinstance(exc, openai.APIStatusError):
            return ProviderError(f"Provider error ({exc.status_code}).", code="provider", status=exc.status_code)
        if isinstance(exc, openai.APIConnectionError):
            return ProviderError("Could not reach the provider.", code="provider")
        return ProviderError(f"Unexpected provider error: {exc}", code="provider")

    async def complete(self, system: str, user: str, *, max_tokens: int = 2000) -> str:
        try:
            resp = await self._client.chat.completions.create(
                **self._params(system, user, max_tokens, stream=False)
            )
            return (resp.choices[0].message.content or "").strip()
        except Exception as exc:
            raise self._translate(exc) from exc

    async def stream(self, system: str, user: str, *, max_tokens: int = 4000) -> AsyncIterator[str]:
        try:
            stream = await self._client.chat.completions.create(
                **self._params(system, user, max_tokens, stream=True)
            )
            async for chunk in stream:
                if not chunk.choices:
                    continue
                delta = chunk.choices[0].delta
                if delta and delta.content:
                    yield delta.content
        except Exception as exc:
            raise self._translate(exc) from exc
