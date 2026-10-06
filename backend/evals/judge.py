"""LLM-as-judge: run a case through the real turn loop and score it. Needs a key."""
from __future__ import annotations

import json
import re

from app.agent.loop import run_turn
from app.providers.base import build_client

JUDGE_SYSTEM = (
    "You are a strict evaluator. Given a user message, the tools the assistant used, "
    "and its final answer, judge the answer. Respond with ONLY JSON: "
    '{"helpful": true/false, "hallucinated": true/false, "notes": "<short>"}.'
)


async def _run_case(case: dict, provider: str, model, api_key: str) -> dict:
    tools_used: list[str] = []
    final = ""
    async for ev in run_turn(message=case["message"], provider=provider, api_key=api_key, model=model):
        if ev.type == "tool_call":
            tools_used.append(ev.name or "")
        elif ev.type == "final":
            final = ev.message or ""
        elif ev.type == "error":
            final = f"[error] {ev.message}"

    expect = case.get("expect_tool")
    tool_ok = expect is None or expect in tools_used

    verdict: dict = {}
    try:
        client = build_client(provider, api_key, model)
        raw = await client.complete(
            JUDGE_SYSTEM,
            f"User: {case['message']}\nTools used: {tools_used}\nAnswer: {final}",
            max_tokens=200,
        )
        m = re.search(r"\{.*\}", raw, re.DOTALL)
        if m:
            verdict = json.loads(m.group(0))
    except Exception as exc:  # judging never crashes the run
        verdict = {"notes": f"judge error: {exc}"}

    return {
        "id": case["id"], "tool_ok": tool_ok, "tools_used": tools_used,
        "helpful": verdict.get("helpful"), "hallucinated": verdict.get("hallucinated"),
        "final": final[:200],
    }


async def run_judge(cases: list[dict], provider: str, model, api_key: str) -> list[dict]:
    return [await _run_case(c, provider, model, api_key) for c in cases]
