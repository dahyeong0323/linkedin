from __future__ import annotations

from linkedin_publisher.audit_log import record_event, utc_now_iso
from linkedin_publisher.db import init_db, session
from linkedin_publisher.draft_service import get_draft
from linkedin_publisher.errors import InvalidTransitionError, ValidationError
from linkedin_publisher.models import Draft, DraftStatus


def request_revision(
    draft_id: str,
    note: str,
    database_url: str | None = None,
) -> Draft:
    if not note.strip():
        raise ValidationError("Revision request note must not be empty")
    init_db(database_url)
    now = utc_now_iso()
    with session(database_url) as conn:
        draft = get_draft(draft_id, database_url, conn=conn)
        if draft.status != DraftStatus.PENDING_REVIEW:
            raise InvalidTransitionError(
                f"Cannot request revision from status {draft.status.value}"
            )
        conn.execute(
            "UPDATE drafts SET status = ?, updated_at = ? WHERE id = ?",
            (DraftStatus.REVISION_REQUESTED.value, now, draft_id),
        )
        record_event(conn, "draft_revision_requested", draft_id, {"note": note.strip()})
        return get_draft(draft_id, database_url, conn=conn)


def mark_ready_for_review(draft_id: str, database_url: str | None = None) -> Draft:
    init_db(database_url)
    now = utc_now_iso()
    with session(database_url) as conn:
        draft = get_draft(draft_id, database_url, conn=conn)
        if draft.status != DraftStatus.REVISION_REQUESTED:
            raise InvalidTransitionError(
                f"Cannot mark ready for review from status {draft.status.value}"
            )
        conn.execute(
            "UPDATE drafts SET status = ?, updated_at = ? WHERE id = ?",
            (DraftStatus.PENDING_REVIEW.value, now, draft_id),
        )
        record_event(conn, "draft_ready_for_review", draft_id)
        return get_draft(draft_id, database_url, conn=conn)


def approve_draft(
    draft_id: str,
    *,
    approved_by: str = "local_user",
    database_url: str | None = None,
) -> Draft:
    init_db(database_url)
    now = utc_now_iso()
    with session(database_url) as conn:
        draft = get_draft(draft_id, database_url, conn=conn)
        if draft.status != DraftStatus.PENDING_REVIEW:
            raise InvalidTransitionError(f"Cannot approve from status {draft.status.value}")
        final_text = draft.final_text or draft.draft_text
        if not final_text.strip():
            raise ValidationError("Cannot approve an empty draft")
        conn.execute(
            """
            UPDATE drafts
            SET status = ?, final_text = ?, updated_at = ?, approved_at = ?, approved_by = ?
            WHERE id = ?
            """,
            (
                DraftStatus.APPROVED.value,
                final_text.strip(),
                now,
                now,
                approved_by,
                draft_id,
            ),
        )
        record_event(conn, "draft_approved", draft_id, {"approved_by": approved_by})
        return get_draft(draft_id, database_url, conn=conn)


def reject_draft(draft_id: str, database_url: str | None = None) -> Draft:
    init_db(database_url)
    now = utc_now_iso()
    with session(database_url) as conn:
        draft = get_draft(draft_id, database_url, conn=conn)
        if draft.status not in {
            DraftStatus.PENDING_REVIEW,
            DraftStatus.REVISION_REQUESTED,
        }:
            raise InvalidTransitionError(f"Cannot reject from status {draft.status.value}")
        conn.execute(
            "UPDATE drafts SET status = ?, updated_at = ? WHERE id = ?",
            (DraftStatus.REJECTED.value, now, draft_id),
        )
        record_event(conn, "draft_rejected", draft_id)
        return get_draft(draft_id, database_url, conn=conn)


def recover_failed_draft(draft_id: str, database_url: str | None = None) -> Draft:
    init_db(database_url)
    now = utc_now_iso()
    with session(database_url) as conn:
        draft = get_draft(draft_id, database_url, conn=conn)
        if draft.status != DraftStatus.FAILED:
            raise InvalidTransitionError(f"Cannot recover from status {draft.status.value}")
        conn.execute(
            """
            UPDATE drafts
            SET status = ?, updated_at = ?, approved_at = NULL, approved_by = NULL
            WHERE id = ?
            """,
            (DraftStatus.PENDING_REVIEW.value, now, draft_id),
        )
        record_event(conn, "draft_recovered_from_failed", draft_id)
        return get_draft(draft_id, database_url, conn=conn)


def can_publish(draft: Draft) -> bool:
    return draft.status == DraftStatus.APPROVED and bool(draft.publish_text)
