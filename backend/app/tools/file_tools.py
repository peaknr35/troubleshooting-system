"""file_read / file_write -- sandboxed to a workspace dir by default.

Default root: ~/.assistant/workspace (APP_FILE_ROOT). Set APP_FILE_UNRESTRICTED=1
to allow the whole filesystem (power-user toggle). The path-escape check is always
applied relative to the root unless unrestricted.
"""
from __future__ import annotations

import asyncio
import logging
from pathlib import Path

from .base import ToolSpec

logger = logging.getLogger(__name__)


def file_root() -> Path:
    from ..config import get_settings
    s = get_settings()
    root = Path(s.file_root).expanduser() if s.file_root else Path.home() / ".assistant" / "workspace"
    root.mkdir(parents=True, exist_ok=True)
    return root.resolve()


def resolve_path(path: str) -> Path:
    from ..config import get_settings
    root = file_root()
    p = Path(path).expanduser()
    target = (p if p.is_absolute() else (root / p)).resolve()
    if get_settings().file_unrestricted:
        return target
    try:
        target.relative_to(root)
    except ValueError:
        raise PermissionError(
            f"path escapes the workspace ({root}). Set APP_FILE_UNRESTRICTED=1 to allow."
        )
    return target


def make_file_read() -> ToolSpec:
    async def file_read(path: str) -> str:
        """Read a UTF-8 text file (sandboxed to the workspace by default)."""
        def _read() -> str:
            return resolve_path(path).read_text(encoding="utf-8", errors="replace")[:20000]
        try:
            return await asyncio.to_thread(_read)
        except Exception as exc:
            return f"file_read error: {exc}"

    return ToolSpec("file_read", "Read a text file from the workspace.", file_read)


def make_file_write() -> ToolSpec:
    async def file_write(path: str, content: str) -> str:
        """Write a UTF-8 text file (sandboxed to the workspace by default)."""
        def _write() -> str:
            t = resolve_path(path)
            t.parent.mkdir(parents=True, exist_ok=True)
            t.write_text(content, encoding="utf-8")
            return str(t)
        try:
            return f"Wrote {await asyncio.to_thread(_write)}"
        except Exception as exc:
            return f"file_write error: {exc}"

    return ToolSpec("file_write", "Write a text file into the workspace.", file_write)
