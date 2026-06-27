from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass(frozen=True)
class DraftCreate:
    source_material: str
    draft_text: str
    input_type: str = "manual_import"
    language: str = "en"
    content_pillar: str | None = None
    risk_notes: list[str] = field(default_factory=list)
    self_review: dict[str, Any] = field(default_factory=dict)


@dataclass(frozen=True)
class DraftUpdate:
    final_text: str
    revision_note: str | None = None


@dataclass(frozen=True)
class RevisionRequest:
    note: str
