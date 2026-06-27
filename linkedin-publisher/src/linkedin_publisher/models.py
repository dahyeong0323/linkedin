from __future__ import annotations

from dataclasses import dataclass
from enum import StrEnum
from typing import Any


class DraftStatus(StrEnum):
    DRAFT = "draft"
    PENDING_REVIEW = "pending_review"
    REVISION_REQUESTED = "revision_requested"
    APPROVED = "approved"
    PUBLISHING = "publishing"
    PUBLISHED = "published"
    FAILED = "failed"
    REJECTED = "rejected"


@dataclass(frozen=True)
class Draft:
    id: str
    created_at: str
    updated_at: str
    input_type: str
    source_material: str
    draft_text: str
    final_text: str | None
    language: str
    content_pillar: str | None
    status: DraftStatus
    risk_notes: list[str]
    self_review: dict[str, Any]
    approved_at: str | None
    approved_by: str | None
    published_at: str | None
    linkedin_post_urn: str | None
    linkedin_url: str | None
    publish_error: str | None

    @property
    def publish_text(self) -> str:
        return (self.final_text or self.draft_text).strip()


@dataclass(frozen=True)
class DraftRevision:
    id: int
    draft_id: str
    created_at: str
    previous_text: str
    new_text: str
    revision_note: str | None


@dataclass(frozen=True)
class AuthToken:
    id: int
    provider: str
    created_at: str
    updated_at: str
    access_token_encrypted: str
    refresh_token_encrypted: str | None
    expires_at: str | None
    scopes: str | None
    member_urn: str | None


@dataclass(frozen=True)
class AuditEvent:
    id: int
    created_at: str
    event_type: str
    draft_id: str | None
    details: dict[str, Any]
