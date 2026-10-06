"""End-to-end streaming test with a mocked LLM and mocked web search."""
import json

import app.routes.research as research_route
import app.services.research as research_svc
from app.models.research import Source


class FakeLLMClient:
    provider = "fake"
    model = "fake-model"

    def __init__(self):
        self.calls = 0

    async def complete(self, system, user, *, max_tokens=2000):
        self.calls += 1
        if self.calls == 1:
            return '["What is X?", "What is Y?"]'  # the plan
        return f"Grounded answer #{self.calls}. (https://example.com)"

    async def stream(self, system, user, *, max_tokens=4000):
        for t in ["# Report\n\n", "Executive summary. ", "Details. ", "Conclusion."]:
            yield t


async def _fake_search(query, max_results=5):
    return [Source(title="Example", url="https://example.com", snippet="A snippet.")]


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


def test_full_pipeline_stream(client, monkeypatch):
    monkeypatch.setattr(research_route, "build_client", lambda *a, **k: FakeLLMClient())
    monkeypatch.setattr(research_svc, "web_search", _fake_search)

    body = {
        "query": "What is deep research?",
        "provider": "openai",
        "api_key": "sk-abcdefgh",
        "max_subquestions": 2,
        "search": True,
    }
    with client.stream("POST", "/research/stream", json=body) as resp:
        assert resp.status_code == 200
        assert resp.headers["content-type"].startswith("text/event-stream")
        events = _collect_events(resp)

    types = [e["type"] for e in events]
    # Ordering guarantee from _shared/api-contract.md
    assert types[0] == "status"
    assert "plan" in types
    assert "sources" in types
    assert "finding" in types
    assert "token" in types
    assert types[-2] == "report"
    assert types[-1] == "done"

    plan = next(e for e in events if e["type"] == "plan")
    assert len(plan["data"]["subquestions"]) == 2

    report = next(e for e in events if e["type"] == "report")
    assert report["data"]["report"].startswith("# Report")
    assert len(report["data"]["sources"]) == 1

    # Every event shares one research_id
    assert len({e["research_id"] for e in events}) == 1


def test_search_disabled_skips_sources(client, monkeypatch):
    monkeypatch.setattr(research_route, "build_client", lambda *a, **k: FakeLLMClient())
    monkeypatch.setattr(research_svc, "web_search", _fake_search)

    body = {
        "query": "What is deep research?",
        "provider": "anthropic",
        "api_key": "sk-ant-abcdefgh",
        "max_subquestions": 1,
        "search": False,
    }
    with client.stream("POST", "/research/stream", json=body) as resp:
        events = _collect_events(resp)

    types = [e["type"] for e in events]
    assert "sources" not in types
    assert "finding" in types
    assert types[-1] == "done"
