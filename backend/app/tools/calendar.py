"""Local calendar tools -- events live in the SQLite events table (local-first).
If Google sync is enabled (APP_GOOGLE_CALENDAR=1 + a token), new events are also
mirrored to Google; the local store stays the source of truth."""
from __future__ import annotations

import asyncio

from . import google_calendar
from .base import ToolSpec


def make_calendar_create() -> ToolSpec:
    async def calendar_create(title: str, start: str, end: str = "", notes: str = "") -> str:
        """Create a calendar event. start/end are ISO-8601 datetimes, e.g. 2026-10-10T09:00."""
        from ..memory import store
        gid = google_calendar.create_event(title, start, end or None, notes or None)
        eid = await asyncio.to_thread(
            store.add_event, title, start, end or None, notes or None, gid
        )
        suffix = " (synced to Google)" if gid else ""
        return f"Created event #{eid}: {title} at {start}{suffix}"

    return ToolSpec("calendar_create", "Create a local calendar event.", calendar_create)


def make_calendar_list() -> ToolSpec:
    async def calendar_list(start: str = "", end: str = "") -> str:
        """List calendar events, optionally within an ISO-8601 date range."""
        from ..memory import store
        rows = await asyncio.to_thread(store.list_events, start or None, end or None, 50)
        if not rows:
            return "No events."
        return "\n".join(
            f"#{e['id']} {e['start']} -- {e['title']}" + (f" (ends {e['end']})" if e["end"] else "")
            for e in rows
        )

    return ToolSpec("calendar_list", "List upcoming local calendar events.", calendar_list)
