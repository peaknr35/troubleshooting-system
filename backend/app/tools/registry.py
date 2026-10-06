"""build_registry(client) -- assemble the tool set for one turn.

Each tool is built here so deep_research can close over the turn's model client.
The same registry feeds both agent backends (manual + PydanticAI).
"""
from __future__ import annotations

from .base import ToolRegistry
from .calendar import make_calendar_create, make_calendar_list
from .deep_research import make_deep_research
from .file_tools import make_file_read, make_file_write
from .memory_tools import make_recall, make_remember
from .web_search import make_web_search


def build_registry(client) -> ToolRegistry:
    reg = ToolRegistry()
    for spec in (
        make_web_search(),
        make_deep_research(client),
        make_remember(),
        make_recall(),
        make_calendar_list(),
        make_calendar_create(),
        make_file_read(),
        make_file_write(),
    ):
        reg.register(spec)
    return reg
