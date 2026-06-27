from __future__ import annotations

import pytest

from linkedin_publisher.draft_service import create_draft, save_final_text
from linkedin_publisher.errors import InvalidTransitionError
from linkedin_publisher.models import DraftStatus
from linkedin_publisher.review_service import approve_draft, can_publish, reject_draft, request_revision
from linkedin_publisher.schemas import DraftCreate


def db_url(tmp_path):
    return f"sqlite:///{tmp_path / 'app.db'}"


def make_draft(tmp_path):
    return create_draft(DraftCreate(source_material="", draft_text="Ready text"), db_url(tmp_path))


def test_approve_reject_and_revision_guards(tmp_path):
    url = db_url(tmp_path)
    draft = create_draft(DraftCreate(source_material="", draft_text="Ready text"), url)

    revision = request_revision(draft.id, "Make it sharper", url)
    assert revision.status == DraftStatus.REVISION_REQUESTED

    with pytest.raises(InvalidTransitionError):
        approve_draft(draft.id, database_url=url)

    ready = save_final_text(draft.id, "Sharper text", database_url=url)
    assert ready.status == DraftStatus.PENDING_REVIEW

    approved = approve_draft(draft.id, database_url=url)
    assert approved.status == DraftStatus.APPROVED
    assert can_publish(approved)

    with pytest.raises(InvalidTransitionError):
        reject_draft(draft.id, url)


def test_only_pending_review_can_be_approved(tmp_path):
    url = db_url(tmp_path)
    draft = create_draft(DraftCreate(source_material="", draft_text="Ready text"), url)
    rejected = reject_draft(draft.id, url)
    assert rejected.status == DraftStatus.REJECTED

    with pytest.raises(InvalidTransitionError):
        approve_draft(draft.id, database_url=url)
