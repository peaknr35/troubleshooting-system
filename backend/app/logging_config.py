"""Logging setup and secret redaction. Never log raw API keys."""
from __future__ import annotations

import logging
import re
import sys

# Matches common provider key shapes (sk-..., sk-ant-...). Best-effort redaction.
_KEY_RE = re.compile(r"\b(sk-(?:ant-)?[A-Za-z0-9_\-]{6,})\b")


def redact(value: object) -> str:
    """Return a string form of ``value`` with anything key-shaped masked."""
    return _KEY_RE.sub("sk-***redacted***", str(value))


class _RedactingFilter(logging.Filter):
    def filter(self, record: logging.LogRecord) -> bool:  # noqa: A003
        if isinstance(record.msg, str):
            record.msg = redact(record.msg)
        if record.args:
            record.args = tuple(redact(a) if isinstance(a, str) else a for a in record.args)
        return True


def configure_logging(level: str = "INFO") -> None:
    handler = logging.StreamHandler(sys.stdout)
    handler.setFormatter(
        logging.Formatter("%(asctime)s %(levelname)-7s %(name)s : %(message)s")
    )
    handler.addFilter(_RedactingFilter())
    root = logging.getLogger()
    root.handlers = [handler]
    root.setLevel(level.upper())
    # Quiet noisy libraries.
    logging.getLogger("httpx").setLevel(logging.WARNING)
    logging.getLogger("httpcore").setLevel(logging.WARNING)
