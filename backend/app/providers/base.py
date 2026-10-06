"""Provider abstraction: one small protocol, one error type, one factory."""
from __future__ import annotations

from typing import AsyncIterator, Optional, Protocol, runtime_checkable

from ..config import get_settings
from ..models.research import Provider


class ProviderError(Exception):
    """Raised by every provider client instead of leaking raw SDK errors.

    code is one of: auth | provider | validation | internal and is surfaced to
    the client in the SSE error event.
    """

    def __init__(self, message: str, *, code: str = "provider", status: Optional[int] = None) -> None:
        super().__init__(message)
        self.message = message
        self.code = code
        self.status = status


@runtime_checkable
class LLMClient(Protocol):
    provider: str
    model: str

    async def complete(self, system: str, user: str, *, max_tokens: int = 2000) -> str:
        """Return a full completion as a string."""
        ...

    def stream(self, system: str, user: str, *, max_tokens: int = 4000) -> AsyncIterator[str]:
        """Yield text chunks as they are generated."""
        ...


def build_client(provider: "Provider | str", api_key: str, model: Optional[str] = None) -> LLMClient:
    """Construct the right client for a provider + user key. Never stores the key."""
    from .anthropic_client import AnthropicClient
    from .openai_client import OpenAICompatibleClient

    settings = get_settings()
    provider = provider if isinstance(provider, Provider) else Provider(provider)

    if provider is Provider.openai:
        return OpenAICompatibleClient(
            api_key=api_key, model=model or settings.openai_default_model, provider="openai"
        )
    if provider is Provider.kimi:
        return OpenAICompatibleClient(
            api_key=api_key, model=model or settings.kimi_default_model,
            provider="kimi", base_url=settings.kimi_base_url,
        )
    if provider is Provider.anthropic:
        return AnthropicClient(api_key=api_key, model=model or settings.anthropic_default_model)
    raise ProviderError(f"unknown provider: {provider}", code="validation")
