"""Load user-editable skills (procedures) from the repo-root skills/ folder.

A skill is a markdown file whose first heading is its name and whose body is the
procedure. Skills are surfaced to the model in the system prompt (M3). Returns []
if the folder is absent, so this is safe to call anytime.
"""
from __future__ import annotations

from pathlib import Path


def skills_dir() -> Path:
    # backend/app/agent/skills.py -> parents[3] is the repo root.
    return Path(__file__).resolve().parents[3] / "skills"


def load_skills() -> list[dict]:
    d = skills_dir()
    if not d.exists():
        return []
    out: list[dict] = []
    for f in sorted(d.glob("*.md")):
        if f.name.upper() == "CONTEXT.MD":
            continue
        text = f.read_text(encoding="utf-8", errors="replace")
        first = text.splitlines()[0].lstrip("# ").strip() if text.strip() else f.stem
        out.append({"name": f.stem, "description": first, "body": text})
    return out
