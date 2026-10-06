"""M3 tests: skills loading, Google calendar disabled-by-default, deterministic evals."""
from app.agent.skills import load_skills
from app.config import get_settings
from app.tools import google_calendar
from evals.deterministic import run_deterministic


def test_skills_load():
    names = {s["name"] for s in load_skills()}
    assert "daily-standup" in names
    assert "summarize-url" in names


def test_google_calendar_disabled_by_default(monkeypatch):
    monkeypatch.delenv("APP_GOOGLE_CALENDAR", raising=False)
    assert google_calendar.is_enabled() is False
    # disabled -> no Google import, returns None (not synced)
    assert google_calendar.create_event("Lunch", "2026-10-10T12:00") is None


def test_deterministic_evals_pass(tmp_path, monkeypatch):
    monkeypatch.setenv("APP_DB_PATH", str(tmp_path / "state.db"))
    monkeypatch.setenv("APP_FILE_ROOT", str(tmp_path / "workspace"))
    get_settings.cache_clear()
    try:
        r = run_deterministic()
        assert r["passed"] == r["total"], r["results"]
    finally:
        get_settings.cache_clear()
