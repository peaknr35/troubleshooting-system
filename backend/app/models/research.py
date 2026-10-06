"""Request and event models for the research API.

The event shape is the single source of truth mirror of
``_shared/api-contract.md``. Change both together.
"""
from __future__ import annotations

import enum
import uuid
from datetime import datetime, timezone
from typing import Any, Literal, Optional

from pydantic import BaseModel, Field, field_validator


class Provider(str, enum.Enum):
    openai = "openai"
    anthropic = "anthropic"
    kimi = "kimi"


class ResearchRequest(BaseModel):
    """Validated body for POST /research/stream."""

    query: str = Field(..., min_length=3, max_length=2000)
    provider: Provider
    model: Optional[str] = Field(default=None, max_length=100)
    api_key: str = Field(..., min_length=8, max_length=400, repr=False)
    max_subquestions: int = Field(default=4, ge=1, le=8)
    search: bool = True

    @field_validator("query")
    @classmethod
    def _strip_query(cls, v: str) -> str:
        v = v.strip()
        if len(v) < 3:
            raise ValueError("query must be at least 3 characters")
        return v

    @field_validator("api_key")
    @classmethod
    def _strip_key(cls, v: str) -> str:
        v = v.strip()
        if len(v) < 8:
            raise ValueError("api_key is too short")
        return v

    @field_validator("model")
    @classmethod
    def _strip_model(cls, v: Optional[str]) -> Optional[str]:
        if v is None:
            return None
        v = v.strip()
        return v or None


class Source(BaseModel):
    title: str = ""
    url: str = ""
    snippet: str = ""


EventType = Literal[
    "status", "plan", "sources", "finding", "token", "report", "done", "error"
]


class ResearchEvent(BaseModel):
    type: EventType
    stage: Optional[str] = None
    message: Optional[str] = None
    data: Optional[dict[str, Any]] = None
    research_id: str
    timestamp: str = Field(
        default_factory=lambda: datetime.now(timezone.utc).isoformat()
    )

    def to_sse(self) -> str:
        """Serialize to a single Server-Sent Event frame."""
        return f"data: {self.model_dump_json()}\n\n"


class EventFactory:
    """Builds ResearchEvents that all share one research_id."""

    def __init__(self, research_id: Optional[str] = None) -> None:
        self.research_id = research_id or str(uuid.uuid4())

    def _mk(
        self,
        type_: EventType,
        stage: Optional[str] = None,
        message: Optional[str] = None,
        data: Optional[dict[str, Any]] = None,
    ) -> ResearchEvent:
        return ResearchEvent(
            type=type_, stage=stage, message=message, data=data,
            research_id=self.research_id,
        )

    def status(self, stage: str, message: str, progress: Optional[float] = None) -> ResearchEvent:
        data = {"progress": round(progress, 3)} if progress is not None else None
        return self._mk("status", stage, message, data)

    def plan(self, subquestions: list[str]) -> ResearchEvent:
        return self._mk("plan", "planning", "Research plan ready", {"subquestions": subquestions})

    def sources(self, index: int, subquestion: str, sources: list[Source]) -> ResearchEvent:
        return self._mk(
            "sources", "researching", None,
            {"index": index, "subquestion": subquestion,
             "sources": [s.model_dump() for s in sources]},
        )

    def finding(self, index: int, subquestion: str, summary: str, sources: list[Source]) -> ResearchEvent:
        return self._mk(
            "finding", "researching", None,
            {"index": index, "subquestion": subquestion, "summary": summary,
             "sources": [s.model_dump() for s in sources]},
        )

    def token(self, text: str) -> ResearchEvent:
        return self._mk("token", "report", None, {"text": text})

    def report(self, report: str, sources: list[Source]) -> ResearchEvent:
        return self._mk(
            "report", "report", "Report complete",
            {"report": report, "sources": [s.model_dump() for s in sources]},
        )

    def done(self) -> ResearchEvent:
        return self._mk("done", "done", "Research complete")

    def error(self, message: str, code: str = "internal") -> ResearchEvent:
        return self._mk("error", "error", message, {"code": code})
