"""Optional Google Calendar sync. OFF unless APP_GOOGLE_CALENDAR=1 and a token file
(APP_GOOGLE_TOKEN_FILE) is configured. When off, imports nothing from Google, so the
google client libraries are an optional extra:
    pip install google-api-python-client google-auth
The local SQLite calendar stays the source of truth; this mirrors an event into
Google when enabled, and never raises (callers treat None as "not synced").
"""
from __future__ import annotations

import logging
import os
from typing import Optional

logger = logging.getLogger(__name__)


def is_enabled() -> bool:
    return os.getenv("APP_GOOGLE_CALENDAR", "") == "1"


def _service():
    from google.oauth2.credentials import Credentials
    from googleapiclient.discovery import build

    token_file = os.getenv("APP_GOOGLE_TOKEN_FILE", "")
    if not token_file:
        raise RuntimeError("APP_GOOGLE_TOKEN_FILE is not set")
    creds = Credentials.from_authorized_user_file(
        token_file, ["https://www.googleapis.com/auth/calendar.events"]
    )
    return build("calendar", "v3", credentials=creds, cache_discovery=False)


def create_event(title: str, start: str, end: Optional[str] = None,
                 notes: Optional[str] = None) -> Optional[str]:
    """Create a Google Calendar event; return its Google id, or None if disabled/failed."""
    if not is_enabled():
        return None
    try:
        service = _service()
        body = {
            "summary": title,
            "description": notes or "",
            "start": {"dateTime": start},
            "end": {"dateTime": end or start},
        }
        ev = service.events().insert(calendarId="primary", body=body).execute()
        return ev.get("id")
    except Exception as exc:  # optional + best-effort; never breaks the local path
        logger.warning("google calendar sync failed: %s", exc)
        return None
