from __future__ import annotations

import pytest

from linkedin_publisher.config import Settings
from linkedin_publisher.draft_service import create_draft, get_draft
from linkedin_publisher.errors import LinkedInApiError, ValidationError
from linkedin_publisher.linkedin_auth import store_token
from linkedin_publisher.linkedin_client import LinkedInPostResult, build_text_post_payload
from linkedin_publisher.models import DraftStatus
from linkedin_publisher.publisher_service import publish_draft
from linkedin_publisher.review_service import approve_draft, recover_failed_draft
from linkedin_publisher.schemas import DraftCreate


class FakeSuccessClient:
    def create_text_post(self, *, access_token, author_urn, text, api_version=None):
        return LinkedInPostResult(
            post_urn="urn:li:share:123",
            payload=build_text_post_payload(author_urn, text),
            status_code=201,
        )


class FakeFailureClient:
    def create_text_post(self, *, access_token, author_urn, text, api_version=None):
        raise LinkedInApiError("LinkedIn API returned 403", 403)


def db_url(tmp_path):
    return f"sqlite:///{tmp_path / 'app.db'}"


def connect_token(url):
    store_token(
        {"access_token": "access-token", "expires_in": 3600, "scope": "openid profile w_member_social"},
        settings=Settings(app_secret_key="secret", linkedin_member_urn="urn:li:person:abc"),
        database_url=url,
    )


def test_publish_requires_approval_confirmation_and_auth(tmp_path):
    url = db_url(tmp_path)
    draft = create_draft(DraftCreate(source_material="", draft_text="Post"), url)

    with pytest.raises(ValidationError):
        publish_draft(draft.id, confirmed=False, database_url=url, client=FakeSuccessClient())

    with pytest.raises(ValidationError):
        publish_draft(draft.id, confirmed=True, database_url=url, client=FakeSuccessClient())

    approve_draft(draft.id, database_url=url)
    with pytest.raises(Exception):
        publish_draft(draft.id, confirmed=True, database_url=url, client=FakeSuccessClient())


def test_publish_success_marks_published_and_exports(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    monkeypatch.setenv("APP_SECRET_KEY", "secret")
    url = db_url(tmp_path)
    draft = create_draft(DraftCreate(source_material="", draft_text="Post"), url)
    approve_draft(draft.id, database_url=url)
    connect_token(url)

    result = publish_draft(
        draft.id,
        confirmed=True,
        database_url=url,
        client=FakeSuccessClient(),
    )

    saved = get_draft(draft.id, url)
    assert result.post_urn == "urn:li:share:123"
    assert saved.status == DraftStatus.PUBLISHED
    assert saved.linkedin_post_urn == "urn:li:share:123"
    assert (tmp_path / "data" / "published_exports" / f"{draft.id}.txt").read_text() == "Post"


def test_publish_failure_marks_failed(tmp_path, monkeypatch):
    monkeypatch.setenv("APP_SECRET_KEY", "secret")
    url = db_url(tmp_path)
    draft = create_draft(DraftCreate(source_material="", draft_text="Post"), url)
    approve_draft(draft.id, database_url=url)
    connect_token(url)

    with pytest.raises(LinkedInApiError):
        publish_draft(
            draft.id,
            confirmed=True,
            database_url=url,
            client=FakeFailureClient(),
        )

    saved = get_draft(draft.id, url)
    assert saved.status == DraftStatus.FAILED
    assert "403" in saved.publish_error


def test_failed_draft_recovers_to_pending_review_and_requires_reapproval(tmp_path, monkeypatch):
    monkeypatch.setenv("APP_SECRET_KEY", "secret")
    url = db_url(tmp_path)
    draft = create_draft(DraftCreate(source_material="", draft_text="Post"), url)
    approve_draft(draft.id, database_url=url)
    connect_token(url)
    with pytest.raises(LinkedInApiError):
        publish_draft(
            draft.id,
            confirmed=True,
            database_url=url,
            client=FakeFailureClient(),
        )

    recovered = recover_failed_draft(draft.id, url)
    assert recovered.status == DraftStatus.PENDING_REVIEW
    assert recovered.approved_at is None
    assert recovered.approved_by is None

    with pytest.raises(ValidationError, match="Only approved"):
        publish_draft(
            draft.id,
            confirmed=True,
            database_url=url,
            client=FakeSuccessClient(),
        )
