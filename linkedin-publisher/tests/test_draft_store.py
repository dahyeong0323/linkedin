from __future__ import annotations

import sqlite3

from linkedin_publisher.db import init_db
from linkedin_publisher.draft_service import (
    create_draft,
    get_draft,
    import_draft_file,
    list_drafts,
    list_revisions,
    save_final_text,
)
from linkedin_publisher.models import DraftStatus
from linkedin_publisher.schemas import DraftCreate


def db_url(tmp_path):
    return f"sqlite:///{tmp_path / 'app.db'}"


def test_init_db_creates_required_tables(tmp_path):
    url = db_url(tmp_path)

    init_db(url)

    with sqlite3.connect(tmp_path / "app.db") as conn:
        tables = {
            row[0]
            for row in conn.execute(
                "SELECT name FROM sqlite_master WHERE type = 'table'"
            ).fetchall()
        }
    assert {"drafts", "draft_revisions", "auth_tokens", "audit_events"} <= tables


def test_create_list_get_and_edit_draft(tmp_path):
    url = db_url(tmp_path)

    draft = create_draft(
        DraftCreate(
            source_material="raw meeting notes",
            draft_text="Draft body",
            language="en",
            content_pillar="korean_startups_explained",
        ),
        url,
    )

    assert draft.id.startswith("draft_")
    assert draft.status == DraftStatus.PENDING_REVIEW
    assert draft.final_text is None

    listed = list_drafts(url)
    assert [item.id for item in listed] == [draft.id]

    saved = save_final_text(draft.id, "Edited final body", database_url=url)
    assert saved.final_text == "Edited final body"
    assert saved.status == DraftStatus.PENDING_REVIEW
    assert len(list_revisions(draft.id, url)) == 1
    assert get_draft(draft.id, url).publish_text == "Edited final body"


def test_import_draft_file(tmp_path):
    url = db_url(tmp_path)
    path = tmp_path / "draft.md"
    path.write_text("Imported draft text", encoding="utf-8")

    draft = import_draft_file(path, source_material="source", database_url=url)

    assert draft.draft_text == "Imported draft text"
    assert draft.source_material == "source"
    assert draft.status == DraftStatus.PENDING_REVIEW
