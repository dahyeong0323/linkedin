from __future__ import annotations

import pytest

from linkedin_publisher.config import Settings
from linkedin_publisher.errors import AuthConfigError
from linkedin_publisher.linkedin_auth import build_authorization_url, get_auth_status, store_token


def test_build_authorization_url_contains_oauth_inputs():
    settings = Settings(
        linkedin_client_id="client-id",
        linkedin_client_secret="secret",
        linkedin_redirect_uri="http://localhost:8000/auth/linkedin/callback",
        linkedin_scopes="openid profile w_member_social",
    )

    url = build_authorization_url("state-value", settings)

    assert "response_type=code" in url
    assert "client_id=client-id" in url
    assert "state=state-value" in url
    assert "scope=openid+profile+w_member_social" in url


def test_store_token_encrypts_and_reports_member_urn(tmp_path, monkeypatch):
    url = f"sqlite:///{tmp_path / 'app.db'}"
    monkeypatch.setenv("APP_SECRET_KEY", "local-secret")
    settings = Settings(app_secret_key="local-secret", linkedin_member_urn="urn:li:person:abc")

    token = store_token(
        {"access_token": "access-token", "expires_in": 3600, "scope": "openid profile w_member_social"},
        settings=settings,
        database_url=url,
    )
    status = get_auth_status(url)

    assert token.access_token == "access-token"
    assert token.member_urn == "urn:li:person:abc"
    assert status.connected
    assert not status.needs_member_urn_verification


@pytest.mark.parametrize("secret", ["", "change_me"])
def test_store_token_blocks_weak_app_secret(tmp_path, secret):
    url = f"sqlite:///{tmp_path / 'app.db'}"
    settings = Settings(app_secret_key=secret, linkedin_member_urn="urn:li:person:abc")

    with pytest.raises(AuthConfigError, match="APP_SECRET_KEY"):
        store_token(
            {"access_token": "access-token", "expires_in": 3600},
            settings=settings,
            database_url=url,
        )
