"""The tool-calling engine: two backends behind one seam.

- manual_middle: prompt-JSON. The model returns {"tool":..,"args":..} or
  {"final":..}; we drive REASON -> ACT -> OBSERVE by hand. Fully transparent,
  works with any provider/key. Reuses the robust JSON-extraction idea from the
  research planner.
- pydantic_middle: PydanticAI native function-calling, normalized across providers.

Both yield TurnEvents. run_middle picks one (manual fallback if pydantic_ai is
missing). The turn loop in loop.py wraps these with RECALL / REMEMBER.
"""
from __future__ import annotations

import json
import logging
import re
from typing import Any, AsyncIterator

from ..config import get_settings
from .prompts import CONSOLIDATE_SYSTEM, base_system, manual_system
from .skills import load_skills

logger = logging.getLogger(__name__)


# --- parsing helpers ---

def parse_action(raw: str) -> dict[str, Any]:
    """Extract the first JSON object; fall back to treating text as a final answer."""
    text = (raw or "").strip()
    m = re.search(r"\{.*\}", text, re.DOTALL)
    if m:
        try:
            obj = json.loads(m.group(0))
            if isinstance(obj, dict):
                return obj
        except json.JSONDecodeError:
            pass
    return {"final": text}


def parse_str_list(raw: str) -> list[str]:
    text = (raw or "").strip()
    m = re.search(r"\[.*\]", text, re.DOTALL)
    if not m:
        return []
    try:
        data = json.loads(m.group(0))
    except json.JSONDecodeError:
        return []
    if not isinstance(data, list):
        return []
    return [str(x).strip() for x in data if str(x).strip()]


def _render_history(history: list[dict], message: str) -> str:
    lines = [f"{h['role'].capitalize()}: {h['content']}" for h in history]
    if message:
        lines.append(f"User: {message}")
    return "\n".join(lines)


async def consolidate(client, user_msg: str, assistant_msg: str) -> list[str]:
    """The consolidation gate: ask the model what (if anything) is worth remembering."""
    if not assistant_msg:
        return []
    try:
        raw = await client.complete(
            CONSOLIDATE_SYSTEM, f"User: {user_msg}\nAssistant: {assistant_msg}", max_tokens=300
        )
        return parse_str_list(raw)
    except Exception as exc:  # consolidation never breaks a turn
        logger.warning("consolidation failed: %s", exc)
        return []


# --- manual (prompt-JSON) backend ---

async def manual_middle(*, client, ev, assistant_name, memories, history, message,
                        registry, max_steps) -> AsyncIterator:
    system = manual_system(assistant_name, memories, registry.manual_catalog(), load_skills())
    convo = _render_history(history, message)
    scratch = ""
    for step in range(1, max_steps + 1):
        yield ev.phase("reason", f"Thinking (step {step})")
        prompt = convo + scratch + "\n\nRespond with the JSON object now."
        raw = await client.complete(system, prompt, max_tokens=900)
        action = parse_action(raw)
        if "tool" not in action:
            yield ev.final(str(action.get("final", raw)).strip())
            return
        name = action.get("tool")
        args = action.get("args") or {}
        yield ev.tool_call(name, args)
        spec = registry.get(name)
        if spec is None:
            obs = f"Unknown tool '{name}'. Available: {', '.join(registry.names())}"
            yield ev.tool_result(name, args, obs, ok=False)
            scratch += f"\n[{name} -> {obs}]"
            continue
        yield ev.phase("act", f"Running {name}")
        result = await spec.run(args)
        yield ev.tool_result(name, args, result.content, ok=result.ok)
        scratch += f"\n[{name}({json.dumps(args)}) -> {result.content[:1500]}]"
    # steps exhausted -> force a plain final answer
    yield ev.phase("reason", "Finalizing")
    final = await client.complete(
        base_system(assistant_name, memories, load_skills()),
        convo + scratch + "\n\nGive your final answer to the user now.",
        max_tokens=1200,
    )
    yield ev.final(final.strip())


# --- pydantic_ai backend ---

def _pai_model(provider: str, model: str | None, api_key: str):
    s = get_settings()
    if provider == "anthropic":
        from pydantic_ai.models.anthropic import AnthropicModel
        from pydantic_ai.providers.anthropic import AnthropicProvider
        return AnthropicModel(model or s.anthropic_default_model,
                              provider=AnthropicProvider(api_key=api_key))
    from pydantic_ai.models.openai import OpenAIChatModel
    from pydantic_ai.providers.openai import OpenAIProvider
    if provider == "kimi":
        return OpenAIChatModel(model or s.kimi_default_model,
                               provider=OpenAIProvider(api_key=api_key, base_url=s.kimi_base_url))
    return OpenAIChatModel(model or s.openai_default_model,
                           provider=OpenAIProvider(api_key=api_key))


async def pydantic_middle(*, provider, model, api_key, ev, assistant_name, memories,
                          history, message, registry) -> AsyncIterator:
    from pydantic_ai import Agent, Tool
    model_obj = _pai_model(provider, model, api_key)
    tools = [Tool(s.func, name=s.name, description=s.description, takes_ctx=False)
             for s in registry.all()]
    agent = Agent(model_obj, system_prompt=base_system(assistant_name, memories, load_skills()), tools=tools)
    prefix = _render_history(history, "")
    prompt = (prefix + "\nUser: " + message) if prefix.strip() else message
    yield ev.phase("reason", "Thinking")
    result = await agent.run(prompt)
    for msg in result.all_messages():
        for part in getattr(msg, "parts", []):
            kind = type(part).__name__
            if kind == "ToolCallPart":
                yield ev.tool_call(getattr(part, "tool_name", ""), getattr(part, "args", None))
            elif kind == "ToolReturnPart":
                yield ev.tool_result(getattr(part, "tool_name", ""), None,
                                     str(getattr(part, "content", "")), ok=True)
    yield ev.final(str(result.output).strip())


# --- selector ---

async def run_middle(backend: str, *, client, provider, model, api_key, ev, assistant_name,
                     memories, history, message, registry, max_steps) -> AsyncIterator:
    if backend == "pydantic_ai":
        try:
            import pydantic_ai  # noqa: F401
        except ImportError:
            logger.warning("pydantic_ai not installed; using manual backend")
        else:
            async for e in pydantic_middle(
                provider=provider, model=model, api_key=api_key, ev=ev,
                assistant_name=assistant_name, memories=memories, history=history,
                message=message, registry=registry,
            ):
                yield e
            return
    async for e in manual_middle(
        client=client, ev=ev, assistant_name=assistant_name, memories=memories,
        history=history, message=message, registry=registry, max_steps=max_steps,
    ):
        yield e
