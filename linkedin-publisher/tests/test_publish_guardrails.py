from __future__ import annotations

import httpx
import pytest

from linkedin_publisher.config import Settings
from linkedin_publisher.db import session
from linkedin_publisher.draft_service import create_draft, get_draft
from linkedin_publisher.errors import LinkedInApiError, NotFoundError, ValidationError
from linkedin_publisher.linkedin_auth import store_token
from linkedin_publisher.linkedin_client import create_text_post
from linkedin_publisher.models import DraftStatus
from linkedin_publisher import publisher_service
from linkedin_publisher.publisher_service import publish_draft
from linkedin_publisher.review_service import approve_draft, reject_draft
from linkedin_publisher.schemas import DraftCreate


class ShouldNotCallLinkedInClient:
    def create_text_post(self, *, access_token, author_urn, text, api_version=None):
        raise AssertionError("LinkedIn API should not be called when guardrails fail")


class SuccessClient:
    def create_text_post(self, *, access_token, author_urn, text, api_version=None):
        from linkedin_publisher.linkedin_client import LinkedInPostResult, build_text_post_payload

        return LinkedInPostResult(
            post_urn="urn:li:share:guardrail",
            payload=build_text_post_payload(author_urn, text),
            status_code=201,
        )


def db_url(tmp_path):
    return f"sqlite:///{tmp_path / 'app.db'}"


def connect_token(url, *, member_urn: str | None = "urn:li:person:abc", expires_in: int = 3600):
    store_token(
        {
            "access_token": "access-token",
            "expires_in": expires_in,
            "scope": "openid profile w_member_social",
        },
        settings=Settings(app_secret_key="secret", linkedin_member_urn=member_urn or ""),
        database_url=url,
    )


def make_draft(url):
    return create_draft(DraftCreate(source_material="", draft_text="Post text"), url)


def test_pending_review_draft_cannot_publish_even_with_token(tmp_path, monkeypatch):
    monkeypatch.setenv("APP_SECRET_KEY", "secret")
    url = db_url(tmp_path)
    draft = make_draft(url)
    connect_token(url)

    with pytest.raises(ValidationError, match="Only approved"):
        publish_draft(
            draft.id,
            confirmed=True,
            database_url=url,
            client=ShouldNotCallLinkedInClient(),
        )


def test_rejected_draft_cannot_publish(tmp_path, monkeypatch):
    monkeypatch.setenv("APP_SECRET_KEY", "secret")
    url = db_url(tmp_path)
    draft = make_draft(url)
    reject_draft(draft.id, url)
    connect_token(url)

    with pytest.raises(ValidationError, match="Only approved"):
        publish_draft(
            draft.id,
            confirmed=True,
            database_url=url,
            client=ShouldNotCallLinkedInClient(),
        )


def test_published_draft_cannot_publish_again(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    monkeypatch.setenv("APP_SECRET_KEY", "secret")
    url = db_url(tmp_path)
    draft = make_draft(url)
    approve_draft(draft.id, database_url=url)
    connect_token(url)
    publish_draft(draft.id, confirmed=True, database_url=url, client=SuccessClient())

    with pytest.raises(ValidationError, match="Only approved"):
        publish_draft(
            draft.id,
            confirmed=True,
            database_url=url,
            client=ShouldNotCallLinkedInClient(),
        )


def test_publishing_status_claimed_by_another_worker_blocks_api_call(tmp_path, monkeypatch):
    monkeypatch.setenv("APP_SECRET_KEY", "secret")
    url = db_url(tmp_path)
    draft = make_draft(url)
    approve_draft(draft.id, database_url=url)
    connect_token(url)
    with session(url) as conn:
        conn.execute(
            "UPDATE drafts SET status = ? WHERE id = ?",
            (DraftStatus.PUBLISHING.value, draft.id),
        )

    with pytest.raises(ValidationError, match="Only approved"):
        publish_draft(
            draft.id,
            confirmed=True,
            database_url=url,
            client=ShouldNotCallLinkedInClient(),
        )


def test_atomic_claim_blocks_stale_approved_precondition(tmp_path, monkeypatch):
    monkeypatch.setenv("APP_SECRET_KEY", "secret")
    url = db_url(tmp_path)
    draft = make_draft(url)
    stale_approved = approve_draft(draft.id, database_url=url)
    connect_token(url)
    token = publisher_service.get_stored_token(database_url=url)
    with session(url) as conn:
        conn.execute(
            "UPDATE drafts SET status = ? WHERE id = ?",
            (DraftStatus.PUBLISHING.value, draft.id),
        )

    monkeypatch.setattr(
        publisher_service,
        "validate_publish_preconditions",
        lambda *args, **kwargs: (stale_approved, token),
    )

    with pytest.raises(ValidationError, match="no longer approved"):
        publisher_service.publish_draft(
            draft.id,
            confirmed=True,
            database_url=url,
            client=ShouldNotCallLinkedInClient(),
        )


def test_missing_token_blocks_publish(tmp_path):
    url = db_url(tmp_path)
    draft = make_draft(url)
    approve_draft(draft.id, database_url=url)

    with pytest.raises(NotFoundError, match="not connected"):
        publish_draft(
            draft.id,
            confirmed=True,
            database_url=url,
            client=ShouldNotCallLinkedInClient(),
        )


def test_missing_member_urn_blocks_publish(tmp_path, monkeypatch):
    monkeypatch.setenv("APP_SECRET_KEY", "secret")
    url = db_url(tmp_path)
    draft = make_draft(url)
    approve_draft(draft.id, database_url=url)
    connect_token(url, member_urn=None)

    with pytest.raises(ValidationError, match="member URN"):
        publish_draft(
            draft.id,
            confirmed=True,
            database_url=url,
            client=ShouldNotCallLinkedInClient(),
        )


def test_organization_member_urn_blocks_publish(tmp_path, monkeypatch):
    monkeypatch.setenv("APP_SECRET_KEY", "secret")
    url = db_url(tmp_path)
    draft = make_draft(url)
    approve_draft(draft.id, database_url=url)
    connect_token(url, member_urn="urn:li:organization:123")

    with pytest.raises(ValidationError, match="personal profile"):
        publish_draft(
            draft.id,
            confirmed=True,
            database_url=url,
            client=ShouldNotCallLinkedInClient(),
        )


def test_missing_w_member_social_scope_blocks_publish(tmp_path, monkeypatch):
    monkeypatch.setenv("APP_SECRET_KEY", "secret")
    url = db_url(tmp_path)
    draft = make_draft(url)
    approve_draft(draft.id, database_url=url)
    store_token(
        {
            "access_token": "access-token",
            "expires_in": 3600,
            "scope": "openid profile",
        },
        settings=Settings(app_secret_key="secret", linkedin_member_urn="urn:li:person:abc"),
        database_url=url,
    )

    with pytest.raises(ValidationError, match="w_member_social"):
        publish_draft(
            draft.id,
            confirmed=True,
            database_url=url,
            client=ShouldNotCallLinkedInClient(),
        )


def test_expired_token_blocks_publish(tmp_path, monkeypatch):
    monkeypatch.setenv("APP_SECRET_KEY", "secret")
    url = db_url(tmp_path)
    draft = make_draft(url)
    approve_draft(draft.id, database_url=url)
    connect_token(url, expires_in=-1)

    with pytest.raises(ValidationError, match="expired"):
        publish_draft(
            draft.id,
            confirmed=True,
            database_url=url,
            client=ShouldNotCallLinkedInClient(),
        )


def test_empty_text_blocks_publish_before_api_call(tmp_path, monkeypatch):
    monkeypatch.setenv("APP_SECRET_KEY", "secret")
    url = db_url(tmp_path)
    draft = make_draft(url)
    approve_draft(draft.id, database_url=url)
    connect_token(url)
    with session(url) as conn:
        conn.execute(
            "UPDATE drafts SET draft_text = '', final_text = '' WHERE id = ?",
            (draft.id,),
        )

    with pytest.raises(ValidationError, match="empty"):
        publish_draft(
            draft.id,
            confirmed=True,
            database_url=url,
            client=ShouldNotCallLinkedInClient(),
        )


def test_dry_run_returns_payload_without_changing_status(tmp_path, monkeypatch):
    monkeypatch.setenv("APP_SECRET_KEY", "secret")
    url = db_url(tmp_path)
    draft = make_draft(url)
    approve_draft(draft.id, database_url=url)
    connect_token(url)

    result = publish_draft(
        draft.id,
        confirmed=True,
        database_url=url,
        dry_run=True,
        client=ShouldNotCallLinkedInClient(),
    )

    saved = get_draft(draft.id, url)
    assert result.dry_run
    assert result.payload["commentary"] == "Post text"
    assert saved.status == DraftStatus.APPROVED
    assert saved.published_at is None


@pytest.mark.parametrize("status_code", [401, 403, 429, 500])
def test_linkedin_api_error_statuses_are_mapped(status_code):
    client = httpx.Client(
        transport=httpx.MockTransport(
            lambda request: httpx.Response(status_code, text="mock failure")
        )
    )

    with pytest.raises(LinkedInApiError) as exc:
        create_text_post(
            access_token="token",
            author_urn="urn:li:person:abc",
            text="Post text",
            client=client,
        )

    assert exc.value.status_code == status_code
