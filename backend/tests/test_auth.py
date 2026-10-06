"""Auth flow + request validation. The server never stores keys; a bad key
surfaces as an SSE error event, and malformed requests are rejected by Pydantic.
"""
import json

import app.routes.research as research_route
from app.providers.base import ProviderError


def _collect_events(resp):
    events = []
    for line in resp.iter_lines():
        if not line:
            continue
        if isinstance(line, bytes):
            line = line.decode()
        if line.startswith("data: "):
            events.append(json.loads(line[len("data: "):]))
    return events


def test_missing_api_key_is_422(client):
    r = client.post("/research/stream", json={"query": "hello world", "provider": "openai"})
    assert r.status_code == 422


def test_short_api_key_is_422(client):
    r = client.post(
        "/research/stream",
        json={"query": "hello world", "provider": "openai", "api_key": "short"},
    )
    assert r.status_code == 422


def test_short_query_is_422(client):
    r = client.post(
        "/research/stream",
        json={"query": "hi", "provider": "openai", "api_key": "sk-abcdefgh"},
    )
    assert r.status_code == 422


def test_unknown_provider_is_422(client):
    r = client.post(
        "/research/stream",
        json={"query": "hello world", "provider": "nope", "api_key": "sk-abcdefgh"},
    )
    assert r.status_code == 422


def test_invalid_key_streams_auth_error(client, monkeypatch):
    class AuthFailClient:
        provider = "openai"
        model = "gpt-5.1"

        async def complete(self, *a, **k):
            raise ProviderError("Invalid or unauthorized API key.", code="auth", status=401)

        async def stream(self, *a, **k):
            if False:
                yield ""  # make this an async generator; never reached

    monkeypatch.setattr(research_route, "build_client", lambda *a, **k: AuthFailClient())

    with client.stream(
        "POST", "/research/stream",
        json={"query": "a genuine question", "provider": "openai", "api_key": "sk-abcdefgh"},
    ) as resp:
        assert resp.status_code == 200
        events = _collect_events(resp)

    errors = [e for e in events if e["type"] == "error"]
    assert errors, f"expected an error event, got {[e['type'] for e in events]}"
    assert errors[0]["data"]["code"] == "auth"
