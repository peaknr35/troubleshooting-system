"""Provider/model connection tests. Providers are mocked -- no real keys/network."""
from unittest.mock import AsyncMock, MagicMock

import httpx
import openai
import pytest

from app.models.research import Provider
from app.providers.anthropic_client import AnthropicClient
from app.providers.base import ProviderError, build_client
from app.providers.openai_client import OpenAICompatibleClient


def test_factory_builds_openai():
    c = build_client(Provider.openai, "sk-test12345678", None)
    assert isinstance(c, OpenAICompatibleClient)
    assert c.provider == "openai"


def test_factory_builds_kimi_with_moonshot_base_url():
    c = build_client("kimi", "sk-test12345678", None)
    assert isinstance(c, OpenAICompatibleClient)
    assert c.provider == "kimi"
    assert "moonshot" in str(c._client.base_url)


def test_factory_builds_anthropic():
    c = build_client(Provider.anthropic, "sk-ant-test12345", None)
    assert isinstance(c, AnthropicClient)
    assert c.provider == "anthropic"


def test_factory_respects_model_override():
    c = build_client("openai", "sk-test12345678", "gpt-5.1-mini")
    assert c.model == "gpt-5.1-mini"


def test_openai_and_kimi_params_differ():
    oc = build_client("openai", "sk-test12345678", None)
    kc = build_client("kimi", "sk-test12345678", None)
    p_openai = oc._params("sys", "user", 100, False)
    p_kimi = kc._params("sys", "user", 100, False)
    # OpenAI: reasoning-model-safe (no max_tokens, no temperature)
    assert "max_completion_tokens" in p_openai
    assert "temperature" not in p_openai
    # Kimi: classic chat-completions params
    assert p_kimi["max_tokens"] == 100
    assert p_kimi["temperature"] == 0.4


async def test_openai_complete_returns_text():
    c = build_client(Provider.openai, "sk-test12345678", None)
    message = MagicMock()
    message.content = "hello from the model"
    choice = MagicMock()
    choice.message = message
    resp = MagicMock()
    resp.choices = [choice]
    c._client.chat.completions.create = AsyncMock(return_value=resp)

    out = await c.complete("system", "user")
    assert out == "hello from the model"


async def test_openai_auth_error_maps_to_provider_error():
    c = build_client(Provider.openai, "sk-bad", None)
    request = httpx.Request("POST", "https://api.openai.com/v1/chat/completions")
    response = httpx.Response(401, request=request)
    err = openai.AuthenticationError("invalid key", response=response, body=None)
    c._client.chat.completions.create = AsyncMock(side_effect=err)

    with pytest.raises(ProviderError) as excinfo:
        await c.complete("system", "user")
    assert excinfo.value.code == "auth"
    assert excinfo.value.status == 401


async def test_openai_stream_yields_chunks():
    c = build_client(Provider.openai, "sk-test12345678", None)

    def _mk_chunk(text):
        delta = MagicMock()
        delta.content = text
        choice = MagicMock()
        choice.delta = delta
        chunk = MagicMock()
        chunk.choices = [choice]
        return chunk

    class _FakeStream:
        def __aiter__(self):
            async def gen():
                for t in ["Hello", " ", "world"]:
                    yield _mk_chunk(t)
            return gen()

    c._client.chat.completions.create = AsyncMock(return_value=_FakeStream())
    out = [chunk async for chunk in c.stream("system", "user")]
    assert "".join(out) == "Hello world"
