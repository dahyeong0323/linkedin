from __future__ import annotations

from datetime import UTC, datetime
import json
from pathlib import Path
import sqlite3
from typing import Any

from linkedin_publisher.audit_log import record_event, utc_now_iso
from linkedin_publisher.db import connect, init_db, session
from linkedin_publisher.errors import NotFoundError, ValidationError
from linkedin_publisher.models import Draft, DraftRevision, DraftStatus
from linkedin_publisher.schemas import DraftCreate


def _row_to_draft(row: sqlite3.Row) -> Draft:
    return Draft(
        id=row["id"],
        created_at=row["created_at"],
        updated_at=row["updated_at"],
        input_type=row["input_type"],
        source_material=row["source_material"],
        draft_text=row["draft_text"],
        final_text=row["final_text"],
        language=row["language"],
        content_pillar=row["content_pillar"],
        status=DraftStatus(row["status"]),
        risk_notes=json.loads(row["risk_notes_json"] or "[]"),
        self_review=json.loads(row["self_review_json"] or "{}"),
        approved_at=row["approved_at"],
        approved_by=row["approved_by"],
        published_at=row["published_at"],
        linkedin_post_urn=row["linkedin_post_urn"],
        linkedin_url=row["linkedin_url"],
        publish_error=row["publish_error"],
    )


def _row_to_revision(row: sqlite3.Row) -> DraftRevision:
    return DraftRevision(
        id=row["id"],
        draft_id=row["draft_id"],
        created_at=row["created_at"],
        previous_text=row["previous_text"],
        new_text=row["new_text"],
        revision_note=row["revision_note"],
    )


def _next_draft_id(conn: sqlite3.Connection) -> str:
    today = datetime.now(UTC).strftime("%Y%m%d")
    prefix = f"draft_{today}_"
    row = conn.execute(
        "SELECT id FROM drafts WHERE id LIKE ? ORDER BY id DESC LIMIT 1",
        (f"{prefix}%",),
    ).fetchone()
    if row is None:
        next_number = 1
    else:
        next_number = int(row["id"].rsplit("_", 1)[-1]) + 1
    return f"{prefix}{next_number:04d}"


def create_draft(payload: DraftCreate, database_url: str | None = None) -> Draft:
    if not payload.draft_text.strip():
        raise ValidationError("draft_text must not be empty")
    init_db(database_url)
    now = utc_now_iso()
    with session(database_url) as conn:
        draft_id = _next_draft_id(conn)
        conn.execute(
            """
            INSERT INTO drafts (
              id, created_at, updated_at, input_type, source_material, draft_text,
              final_text, language, content_pillar, status, risk_notes_json,
              self_review_json
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                draft_id,
                now,
                now,
                payload.input_type,
                payload.source_material,
                payload.draft_text.strip(),
                None,
                payload.language,
                payload.content_pillar,
                DraftStatus.PENDING_REVIEW.value,
                json.dumps(payload.risk_notes, ensure_ascii=True),
                json.dumps(payload.self_review, ensure_ascii=True, sort_keys=True),
            ),
        )
        record_event(
            conn,
            "draft_created",
            draft_id,
            {"input_type": payload.input_type, "language": payload.language},
        )
        return get_draft(draft_id, database_url, conn=conn)


def import_draft_file(
    path: str | Path,
    *,
    source_material: str = "",
    language: str = "en",
    content_pillar: str | None = None,
    database_url: str | None = None,
) -> Draft:
    draft_path = Path(path)
    if not draft_path.exists():
        raise ValidationError(f"Draft file does not exist: {draft_path}")
    draft_text = draft_path.read_text(encoding="utf-8").strip()
    return create_draft(
        DraftCreate(
            source_material=source_material,
            draft_text=draft_text,
            input_type=f"file:{draft_path.suffix.lower() or 'text'}",
            language=language,
            content_pillar=content_pillar,
        ),
        database_url,
    )


def list_drafts(
    database_url: str | None = None,
    *,
    status: DraftStatus | str | None = None,
    language: str | None = None,
) -> list[Draft]:
    init_db(database_url)
    clauses: list[str] = []
    params: list[Any] = []
    if status:
        clauses.append("status = ?")
        params.append(str(status))
    if language:
        clauses.append("language = ?")
        params.append(language)
    where = f"WHERE {' AND '.join(clauses)}" if clauses else ""
    with session(database_url) as conn:
        rows = conn.execute(
            f"SELECT * FROM drafts {where} ORDER BY created_at DESC, id DESC",
            params,
        ).fetchall()
    return [_row_to_draft(row) for row in rows]


def get_draft(
    draft_id: str,
    database_url: str | None = None,
    *,
    conn: sqlite3.Connection | None = None,
) -> Draft:
    should_close = conn is None
    if conn is None:
        init_db(database_url)
        conn = connect(database_url)
    try:
        row = conn.execute("SELECT * FROM drafts WHERE id = ?", (draft_id,)).fetchone()
        if row is None:
            raise NotFoundError(f"Draft not found: {draft_id}")
        return _row_to_draft(row)
    finally:
        if should_close:
            conn.close()


def list_revisions(draft_id: str, database_url: str | None = None) -> list[DraftRevision]:
    init_db(database_url)
    with session(database_url) as conn:
        rows = conn.execute(
            "SELECT * FROM draft_revisions WHERE draft_id = ? ORDER BY created_at DESC, id DESC",
            (draft_id,),
        ).fetchall()
    return [_row_to_revision(row) for row in rows]


def save_final_text(
    draft_id: str,
    final_text: str,
    *,
    revision_note: str | None = None,
    database_url: str | None = None,
) -> Draft:
    if not final_text.strip():
        raise ValidationError("final_text must not be empty")
    init_db(database_url)
    now = utc_now_iso()
    with session(database_url) as conn:
        draft = get_draft(draft_id, database_url, conn=conn)
        if draft.status == DraftStatus.PUBLISHED:
            raise ValidationError("Published drafts cannot be edited")
        previous = draft.final_text or draft.draft_text
        next_status = draft.status
        if draft.status in {DraftStatus.APPROVED, DraftStatus.REVISION_REQUESTED}:
            next_status = DraftStatus.PENDING_REVIEW
        approved_at = None if draft.status == DraftStatus.APPROVED else draft.approved_at
        approved_by = None if draft.status == DraftStatus.APPROVED else draft.approved_by
        conn.execute(
            """
            UPDATE drafts
            SET final_text = ?, updated_at = ?, status = ?, approved_at = ?, approved_by = ?
            WHERE id = ?
            """,
            (final_text.strip(), now, next_status.value, approved_at, approved_by, draft_id),
        )
        conn.execute(
            """
            INSERT INTO draft_revisions (
              draft_id, created_at, previous_text, new_text, revision_note
            )
            VALUES (?, ?, ?, ?, ?)
            """,
            (draft_id, now, previous, final_text.strip(), revision_note),
        )
        record_event(
            conn,
            "draft_updated",
            draft_id,
            {"revision_note": revision_note or "", "status": next_status.value},
        )
        return get_draft(draft_id, database_url, conn=conn)
