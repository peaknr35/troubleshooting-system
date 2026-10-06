"""Memory operations over the SQLite brain. Plain, synchronous functions; the
agent loop calls them via asyncio.to_thread. Mirrors ../../../_shared/memory-schema.md.
"""
from __future__ import annotations

import json
import re
from datetime import datetime, timezone
from typing import Any, Optional

from .db import connect


def _now() -> str:
    return datetime.now(timezone.utc).isoformat()


def init_db() -> None:
    connect().close()


# --- conversations & turns (episodic) ---

def start_conversation(title: Optional[str] = None) -> int:
    with connect() as c:
        cur = c.execute(
            "INSERT INTO conversations (title, started_at) VALUES (?, ?)", (title, _now())
        )
        return int(cur.lastrowid)


def add_turn(conversation_id: int, role: str, content: str,
             trace: Optional[dict] = None) -> int:
    with connect() as c:
        cur = c.execute(
            "INSERT INTO turns (conversation_id, role, content, trace, created_at)"
            " VALUES (?, ?, ?, ?, ?)",
            (conversation_id, role, content,
             json.dumps(trace) if trace is not None else None, _now()),
        )
        return int(cur.lastrowid)


def recent_turns(conversation_id: int, limit: int = 10) -> list[dict[str, Any]]:
    with connect() as c:
        rows = c.execute(
            "SELECT role, content, created_at FROM turns WHERE conversation_id = ?"
            " ORDER BY id DESC LIMIT ?",
            (conversation_id, limit),
        ).fetchall()
    return [dict(r) for r in reversed(rows)]


# --- facts (semantic memory) ---

def add_fact(text: str, kind: str = "fact", source: str = "auto") -> Optional[int]:
    text = (text or "").strip()
    if not text:
        return None
    with connect() as c:
        existing = c.execute(
            "SELECT id FROM facts WHERE lower(text) = lower(?)", (text,)
        ).fetchone()
        if existing:
            return int(existing["id"])
        cur = c.execute(
            "INSERT INTO facts (text, kind, source, created_at) VALUES (?, ?, ?, ?)",
            (text, kind, source, _now()),
        )
        return int(cur.lastrowid)


def recall(query: str, limit: int = 6) -> list[dict[str, Any]]:
    """Keyword recall over facts (simple LIKE match; recency-ordered).

    Swap for FTS5 or sqlite-vec later without changing callers.
    """
    words = [w for w in re.findall(r"[A-Za-z0-9]+", query or "") if len(w) > 2]
    with connect() as c:
        if words:
            clause = " OR ".join(["text LIKE ?"] * len(words))
            params = [f"%{w}%" for w in words] + [limit]
            rows = c.execute(
                f"SELECT text, kind, source, created_at FROM facts WHERE {clause}"
                " ORDER BY created_at DESC LIMIT ?",
                params,
            ).fetchall()
            if rows:
                return [dict(r) for r in rows]
        rows = c.execute(
            "SELECT text, kind, source, created_at FROM facts"
            " ORDER BY created_at DESC LIMIT ?",
            (limit,),
        ).fetchall()
    return [dict(r) for r in rows]


def all_facts(limit: int = 100) -> list[dict[str, Any]]:
    with connect() as c:
        rows = c.execute(
            "SELECT id, text, kind, source, created_at FROM facts"
            " ORDER BY created_at DESC LIMIT ?",
            (limit,),
        ).fetchall()
    return [dict(r) for r in rows]


# --- tool run trace (for evals/debug) ---

def add_tool_run(turn_id: Optional[int], tool: str, args: Any,
                 result: str, ok: bool = True) -> int:
    with connect() as c:
        cur = c.execute(
            "INSERT INTO tool_runs (turn_id, tool, args, result, ok, created_at)"
            " VALUES (?, ?, ?, ?, ?, ?)",
            (turn_id, tool, json.dumps(args, default=str),
             (result or "")[:4000], 1 if ok else 0, _now()),
        )
        return int(cur.lastrowid)


def recent_tool_runs(limit: int = 30) -> list[dict[str, Any]]:
    with connect() as c:
        rows = c.execute(
            "SELECT turn_id, tool, args, result, ok, created_at FROM tool_runs"
            " ORDER BY id DESC LIMIT ?",
            (limit,),
        ).fetchall()
    return [dict(r) for r in rows]


# --- local calendar (events) ---

def add_event(title: str, start: str, end: Optional[str] = None,
              notes: Optional[str] = None, google_id: Optional[str] = None) -> int:
    with connect() as c:
        cur = c.execute(
            'INSERT INTO events (title, start, "end", notes, google_id, created_at)'
            " VALUES (?, ?, ?, ?, ?, ?)",
            (title, start, end, notes, google_id, _now()),
        )
        return int(cur.lastrowid)


def list_events(start: Optional[str] = None, end: Optional[str] = None,
                limit: int = 50) -> list[dict[str, Any]]:
    clauses, params = [], []
    if start:
        clauses.append("start >= ?")
        params.append(start)
    if end:
        clauses.append("start <= ?")
        params.append(end)
    where = f"WHERE {' AND '.join(clauses)}" if clauses else ""
    params.append(limit)
    with connect() as c:
        rows = c.execute(
            f'SELECT id, title, start, "end", notes, google_id FROM events {where}'
            " ORDER BY start ASC LIMIT ?",
            params,
        ).fetchall()
    return [dict(r) for r in rows]


# --- skills (procedural; M3) ---

def upsert_skill(name: str, description: str, body: str) -> None:
    with connect() as c:
        c.execute(
            "INSERT INTO skills (name, description, body, created_at) VALUES (?, ?, ?, ?)"
            " ON CONFLICT(name) DO UPDATE SET description=excluded.description,"
            " body=excluded.body",
            (name, description, body, _now()),
        )


def list_skills() -> list[dict[str, Any]]:
    with connect() as c:
        rows = c.execute(
            "SELECT name, description FROM skills ORDER BY name"
        ).fetchall()
    return [dict(r) for r in rows]


def counts() -> dict[str, int]:
    with connect() as c:
        def n(t: str) -> int:
            return int(c.execute(f"SELECT COUNT(*) AS n FROM {t}").fetchone()["n"])
        return {
            "conversations": n("conversations"), "turns": n("turns"),
            "facts": n("facts"), "events": n("events"),
            "tool_runs": n("tool_runs"), "skills": n("skills"),
        }
