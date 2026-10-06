"""Agent M1 tests: turn loop (manual backend, offline), tools, file sandbox, and
PydanticAI model construction. No real keys or network."""
import pytest

import app.agent.loop as loop_mod
from app.agent import generate
from app.config import get_settings
from app.tools.file_tools import resolve_path
from app.tools.registry import build_registry


class FakeClient:
    provider = "openai"
    model = "fake-model"

    def __init__(self):
        self.step = 0

    async def complete(self, system, user, *, max_tokens=2000):
        if "worth remembering" in system:  # the consolidation gate
            return '["User likes tea"]'
        self.step += 1
        if self.step == 1:
            return '{"tool": "remember", "args": {"text": "User likes tea"}}'
        return '{"final": "Done - I remembered you like tea."}'

    async def stream(self, system, user, *, max_tokens=4000):
        yield "x"


@pytest.fixture
def local_env(tmp_path, monkeypatch):
    monkeypatch.setenv("APP_DB_PATH", str(tmp_path / "state.db"))
    monkeypatch.setenv("APP_FILE_ROOT", str(tmp_path / "workspace"))
    monkeypatch.setenv("APP_AGENT_BACKEND", "manual")
    get_settings.cache_clear()
    yield
    get_settings.cache_clear()


def test_parse_action():
    assert generate.parse_action('{"tool":"x","args":{"a":1}}')["tool"] == "x"
    assert generate.parse_action('here {"final":"hi"} there')["final"] == "hi"
    assert generate.parse_action("just text")["final"] == "just text"


def test_parse_str_list():
    assert generate.parse_str_list('["a","b"]') == ["a", "b"]
    assert generate.parse_str_list("nope") == []


def test_registry_has_core_tools():
    reg = build_registry(FakeClient())
    for name in ["web_search", "deep_research", "remember", "recall",
                 "calendar_list", "calendar_create", "file_read", "file_write"]:
        assert reg.get(name) is not None


async def test_turn_loop_manual(local_env, monkeypatch):
    monkeypatch.setattr(loop_mod, "build_client", lambda *a, **k: FakeClient())
    events = [e async for e in loop_mod.run_turn(
        message="I like tea", provider="openai", api_key="x" * 8
    )]
    types = [e.type for e in events]
    assert types[0] == "phase"
    assert any(e.type == "tool_call" and e.name == "remember" for e in events)
    assert any(e.type == "final" for e in events)
    assert types[-1] == "done"
    from app.memory import store
    facts = [f["text"].lower() for f in store.all_facts()]
    assert any("tea" in f for f in facts)


async def test_file_sandbox(local_env):
    inside = resolve_path("notes/a.txt")
    assert "workspace" in str(inside)
    with pytest.raises(PermissionError):
        resolve_path("../escape.txt")


def test_pydantic_models_build(local_env):
    for provider in ("openai", "anthropic", "kimi"):
        model = generate._pai_model(provider, None, "sk-test12345678")
        assert model is not None
