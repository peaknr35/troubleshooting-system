"""Offline deterministic checks -- no key, no network. These gate changes."""
from __future__ import annotations

from app.agent import generate
from app.memory import store
from app.tools.file_tools import resolve_path
from app.tools.registry import build_registry


class _FakeClient:
    provider = "openai"
    model = "fake"

    async def complete(self, *a, **k):
        return ""

    async def stream(self, *a, **k):
        if False:
            yield ""


def run_deterministic() -> dict:
    results: list[tuple[str, bool]] = []

    def check(name: str, cond: bool) -> None:
        results.append((name, bool(cond)))

    check("parse_action tool", generate.parse_action('{"tool":"x","args":{}}').get("tool") == "x")
    check("parse_action final-from-text", generate.parse_action("hello").get("final") == "hello")
    check("parse_str_list", generate.parse_str_list('["a","b"]') == ["a", "b"])
    check("parse_str_list empty", generate.parse_str_list("nope") == [])

    reg = build_registry(_FakeClient())
    for t in ["web_search", "deep_research", "remember", "recall",
              "calendar_list", "calendar_create", "file_read", "file_write"]:
        check(f"tool:{t}", reg.get(t) is not None)

    store.init_db()
    fid = store.add_fact("eval fact alpha", source="explicit")
    check("add_fact", fid is not None)
    check("add_fact dedupe", store.add_fact("eval fact alpha") == fid)
    check("recall finds", any("alpha" in r["text"] for r in store.recall("alpha")))

    try:
        resolve_path("../escape.txt")
        escaped = True
    except PermissionError:
        escaped = False
    check("file sandbox blocks escape", not escaped)
    check("file sandbox allows inside", "workspace" in str(resolve_path("ok.txt")))

    passed = sum(1 for _, ok in results if ok)
    return {"passed": passed, "total": len(results), "results": results}
