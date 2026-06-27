from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Any, Protocol

from linkedin_publisher.audit_log import record_event, utc_now_iso
from linkedin_publisher.config import get_settings
from linkedin_publisher.db import init_db, session
from linkedin_publisher.draft_service import get_draft
from linkedin_publisher.errors import LinkedInApiError, ValidationError
from linkedin_publisher.linkedin_auth import get_stored_token, token_is_expired
from linkedin_publisher.linkedin_client import LinkedInPostResult, build_text_post_payload, create_text_post
from linkedin_publisher.models import Draft, DraftStatus


class LinkedInPostClient(Protocol):
    def create_text_post(
        self,
        *,
        access_token: str,
        author_urn: str,
        text: str,
        api_version: str | None = None,
    ) -> LinkedInPostResult:
        ...


@dataclass(frozen=True)
class PublishResult:
    draft: Draft
    payload: dict[str, Any]
    post_urn: str | None = None
    dry_run: bool = False


def _published_export_path(draft_id: str) -> Path:
    return Path("data") / "published_exports" / f"{draft_id}.txt"


def _derive_linkedin_url(post_urn: str | None) -> str | None:
    if not post_urn or post_urn.startswith("[NEEDS_VERIFICATION"):
        return None
    # LinkedIn public URLs are not reliably derivable from every Posts API URN.
    return None


def validate_publish_preconditions(
    draft_id: str,
    *,
    confirmed: bool,
    database_url: str | None = None,
) -> tuple[Draft, Any]:
    if not confirmed:
        raise ValidationError("Publish requires explicit confirmation")
    draft = get_draft(draft_id, database_url)
    if draft.status != DraftStatus.APPROVED:
        raise ValidationError("Only approved drafts can be published")
    if not draft.publish_text:
        raise ValidationError("Cannot publish empty text")
    token = get_stored_token(database_url=database_url)
    if token_is_expired(token.expires_at):
        raise ValidationError("LinkedIn access token is expired. Reconnect LinkedIn.")
    if not token.member_urn:
        raise ValidationError(
            "LinkedIn member URN is not verified. Set LINKEDIN_MEMBER_URN and reconnect."
        )
    if not token.member_urn.startswith("urn:li:person:"):
        raise ValidationError("LinkedIn v0.1 only supports personal profile member URNs")
    scopes = set((token.scopes or "").replace(",", " ").split())
    if "w_member_social" not in scopes:
        raise ValidationError("LinkedIn token is missing required scope w_member_social")
    return draft, token


def dry_run_publish_payload(draft_id: str, database_url: str | None = None) -> dict[str, Any]:
    draft = get_draft(draft_id, database_url)
    token = get_stored_token(database_url=database_url)
    if not token.member_urn:
        raise ValidationError("LinkedIn member URN is required for payload generation")
    return build_text_post_payload(token.member_urn, draft.publish_text)


def publish_draft(
    draft_id: str,
    *,
    confirmed: bool,
    database_url: str | None = None,
    dry_run: bool = False,
    client: LinkedInPostClient | None = None,
) -> PublishResult:
    init_db(database_url)
    settings = get_settings()
    draft, token = validate_publish_preconditions(
        draft_id,
        confirmed=confirmed,
        database_url=database_url,
    )
    payload = build_text_post_payload(token.member_urn, draft.publish_text)
    if dry_run:
        return PublishResult(draft=draft, payload=payload, dry_run=True)

    now = utc_now_iso()
    with session(database_url) as conn:
        result = conn.execute(
            """
            UPDATE drafts
            SET status = ?, updated_at = ?, publish_error = NULL
            WHERE id = ? AND status = ?
            """,
            (
                DraftStatus.PUBLISHING.value,
                now,
                draft_id,
                DraftStatus.APPROVED.value,
            ),
        )
        if result.rowcount != 1:
            raise ValidationError("Draft is no longer approved for publishing")
        claimed_draft = get_draft(draft_id, database_url, conn=conn)
        if not claimed_draft.publish_text:
            raise ValidationError("Cannot publish empty text")
        record_event(conn, "publish_attempted", draft_id)
    draft = claimed_draft

    try:
        if client is None:
            result = create_text_post(
                access_token=token.access_token,
                author_urn=token.member_urn,
                text=draft.publish_text,
                api_version=settings.linkedin_api_version,
            )
        else:
            result = client.create_text_post(
                access_token=token.access_token,
                author_urn=token.member_urn,
                text=draft.publish_text,
                api_version=settings.linkedin_api_version,
            )
    except LinkedInApiError as exc:
        now = utc_now_iso()
        with session(database_url) as conn:
            conn.execute(
                "UPDATE drafts SET status = ?, updated_at = ?, publish_error = ? WHERE id = ?",
                (DraftStatus.FAILED.value, now, str(exc), draft_id),
            )
            record_event(
                conn,
                "publish_failed",
                draft_id,
                {"status_code": exc.status_code, "error": str(exc)},
            )
        raise

    now = utc_now_iso()
    linkedin_url = _derive_linkedin_url(result.post_urn)
    with session(database_url) as conn:
        conn.execute(
            """
            UPDATE drafts
            SET status = ?, updated_at = ?, published_at = ?, linkedin_post_urn = ?,
                linkedin_url = ?, publish_error = NULL
            WHERE id = ?
            """,
            (
                DraftStatus.PUBLISHED.value,
                now,
                now,
                result.post_urn,
                linkedin_url,
                draft_id,
            ),
        )
        record_event(
            conn,
            "publish_succeeded",
            draft_id,
            {"linkedin_post_urn": result.post_urn, "linkedin_url": linkedin_url},
        )
    export_path = _published_export_path(draft_id)
    export_path.parent.mkdir(parents=True, exist_ok=True)
    export_path.write_text(draft.publish_text, encoding="utf-8")
    return PublishResult(
        draft=get_draft(draft_id, database_url),
        payload=result.payload,
        post_urn=result.post_urn,
        dry_run=False,
    )
