"""Tool primitives shared by both agent backends.

A tool is a typed async function returning a string observation. The same
function is used by the manual (prompt-JSON) backend and by PydanticAI (which
infers its schema from the signature), so there is one definition per tool.
"""
from __future__ import annotations

import inspect
from dataclasses import dataclass
from typing import Any, Callable


@dataclass
class ToolResult:
    content: str
    ok: bool = True


@dataclass
class ToolSpec:
    name: str
    description: str
    func: Callable[..., Any]  # typed async def (...) -> str

    def signature_hint(self) -> str:
        parts = []
        for pname, p in inspect.signature(self.func).parameters.items():
            ann = p.annotation
            ann = getattr(ann, "__name__", "any") if ann is not inspect.Parameter.empty else "any"
            default = "" if p.default is inspect.Parameter.empty else f"={p.default!r}"
            parts.append(f"{pname}: {ann}{default}")
        return ", ".join(parts)

    async def run(self, args: dict[str, Any]) -> ToolResult:
        try:
            out = await self.func(**(args or {}))
            return ToolResult(str(out), ok=True)
        except TypeError as exc:
            return ToolResult(f"bad arguments for {self.name}: {exc}", ok=False)
        except Exception as exc:  # tools never crash the turn
            return ToolResult(f"{self.name} failed: {exc}", ok=False)


class ToolRegistry:
    def __init__(self) -> None:
        self._tools: dict[str, ToolSpec] = {}

    def register(self, spec: ToolSpec) -> None:
        self._tools[spec.name] = spec

    def get(self, name: str) -> ToolSpec | None:
        return self._tools.get(name)

    def all(self) -> list[ToolSpec]:
        return list(self._tools.values())

    def names(self) -> list[str]:
        return list(self._tools)

    def manual_catalog(self) -> str:
        """A compact text list of tools for the manual backend's system prompt."""
        return "\n".join(
            f"- {t.name}({t.signature_hint()}) -- {t.description}" for t in self.all()
        )
