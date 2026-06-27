from __future__ import annotations

from dataclasses import dataclass
from datetime import UTC, datetime, timedelta
from typing import Any
from urllib.parse import urlencode

import httpx

from linkedin_publisher.audit_log import record_event, utc_now_iso
from linkedin_publisher.config import Settings, get_settings
from linkedin_publisher.db import init_db, session
from linkedin_publisher.errors import AuthConfigError, LinkedInApiError, NotFoundError
from linkedin_publisher.token_crypto import decrypt_token, encrypt_token


AUTHORIZATION_URL = "https://www.linkedin.com/oauth/v2/authorization"
TOKEN_URL = "https://www.linkedin.com/oauth/v2/accessToken"
USERINFO_URL = "https://api.linkedin.com/v2/userinfo"
PROVIDER = "linkedin"


@dataclass(frozen=True)
class StoredLinkedInToken:
    id: int
    access_token: str
    refresh_token: str | None
    expires_at: str | None
    scopes: str | None
    member_urn: str | None


@dataclass(frozen=True)
class AuthStatus:
    connected: bool
    scopes: str | None = None
    expires_at: str | None = None
    member_urn: str | None = None
    needs_member_urn_verification: bool = False
    message: str = ""


def validate_oauth_config(settings: Settings | None = None) -> Settings:
    settings = settings or get_settings()
    missing = []
    if not settings.linkedin_client_id:
        missing.append("LINKEDIN_CLIENT_ID")
    if not settings.linkedin_client_secret:
        missing.append("LINKEDIN_CLIENT_SECRET")
    if not settings.linkedin_redirect_uri:
        missing.append("LINKEDIN_REDIRECT_URI")
    if missing:
        raise AuthConfigError(f"Missing LinkedIn OAuth config: {', '.join(missing)}")
    return settings


def validate_token_storage_secret(settings: Settings) -> None:
    if not settings.app_secret_key or settings.app_secret_key == "change_me":
        raise AuthConfigError(
            "APP_SECRET_KEY must be set to a strong non-default value before storing LinkedIn tokens"
        )


def build_authorization_url(state: str, settings: Settings | None = None) -> str:
    settings = validate_oauth_config(settings)
    query = urlencode(
        {
            "response_type": "code",
            "client_id": settings.linkedin_client_id,
            "redirect_uri": settings.linkedin_redirect_uri,
            "scope": settings.linkedin_scopes,
            "state": state,
        }
    )
    return f"{AUTHORIZATION_URL}?{query}"


def _expires_at_from_token_response(data: dict[str, Any]) -> str | None:
    expires_in = data.get("expires_in")
    if expires_in is None:
        return None
    return (
        datetime.now(UTC)
        .replace(microsecond=0)
        .__add__(timedelta(seconds=int(expires_in)))
        .isoformat()
        .replace("+00:00", "Z")
    )


def exchange_code_for_token(
    code: str,
    *,
    settings: Settings | None = None,
    client: httpx.Client | None = None,
) -> dict[str, Any]:
    settings = validate_oauth_config(settings)
    form = {
        "grant_type": "authorization_code",
        "code": code,
        "redirect_uri": settings.linkedin_redirect_uri,
        "client_id": settings.linkedin_client_id,
        "client_secret": settings.linkedin_client_secret,
    }
    owns_client = client is None
    client = client or httpx.Client(timeout=20)
    try:
        response = client.post(
            TOKEN_URL,
            data=form,
            headers={"Content-Type": "application/x-www-form-urlencoded"},
        )
    finally:
        if owns_client:
            client.close()
    if response.status_code >= 400:
        raise LinkedInApiError(
            f"LinkedIn token exchange failed with status {response.status_code}",
            response.status_code,
        )
    return response.json()


def fetch_userinfo(
    access_token: str,
    *,
    client: httpx.Client | None = None,
) -> dict[str, Any]:
    owns_client = client is None
    client = client or httpx.Client(timeout=20)
    try:
        response = client.get(USERINFO_URL, headers={"Authorization": f"Bearer {access_token}"})
    finally:
        if owns_client:
            client.close()
    if response.status_code >= 400:
        raise LinkedInApiError(
            f"LinkedIn userinfo request failed with status {response.status_code}",
            response.status_code,
        )
    return response.json()


def store_token(
    token_response: dict[str, Any],
    *,
    member_urn: str | None = None,
    settings: Settings | None = None,
    database_url: str | None = None,
) -> StoredLinkedInToken:
    settings = settings or get_settings()
    validate_token_storage_secret(settings)
    access_token = token_response.get("access_token")
    if not access_token:
        raise LinkedInApiError("LinkedIn token response did not include access_token")
    refresh_token = token_response.get("refresh_token")
    scopes = token_response.get("scope") or settings.linkedin_scopes
    now = utc_now_iso()
    effective_member_urn = member_urn or settings.linkedin_member_urn or None
    init_db(database_url)
    with session(database_url) as conn:
        conn.execute("DELETE FROM auth_tokens WHERE provider = ?", (PROVIDER,))
        conn.execute(
            """
            INSERT INTO auth_tokens (
              provider, created_at, updated_at, access_token_encrypted,
              refresh_token_encrypted, expires_at, scopes, member_urn
            )
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """,
            (
                PROVIDER,
                now,
                now,
                encrypt_token(access_token, settings.app_secret_key),
                encrypt_token(refresh_token, settings.app_secret_key)
                if refresh_token
                else None,
                _expires_at_from_token_response(token_response),
                scopes,
                effective_member_urn,
            ),
        )
        record_event(
            conn,
            "auth_connected",
            details={
                "provider": PROVIDER,
                "scopes": scopes,
                "member_urn_present": bool(effective_member_urn),
            },
        )
        row = conn.execute(
            "SELECT * FROM auth_tokens WHERE provider = ? ORDER BY id DESC LIMIT 1",
            (PROVIDER,),
        ).fetchone()
    return _row_to_stored_token(row, settings)


def _row_to_stored_token(row, settings: Settings) -> StoredLinkedInToken:
    return StoredLinkedInToken(
        id=row["id"],
        access_token=decrypt_token(row["access_token_encrypted"], settings.app_secret_key),
        refresh_token=decrypt_token(row["refresh_token_encrypted"], settings.app_secret_key)
        if row["refresh_token_encrypted"]
        else None,
        expires_at=row["expires_at"],
        scopes=row["scopes"],
        member_urn=row["member_urn"],
    )


def get_stored_token(
    *,
    settings: Settings | None = None,
    database_url: str | None = None,
) -> StoredLinkedInToken:
    settings = settings or get_settings()
    init_db(database_url)
    with session(database_url) as conn:
        row = conn.execute(
            "SELECT * FROM auth_tokens WHERE provider = ? ORDER BY id DESC LIMIT 1",
            (PROVIDER,),
        ).fetchone()
    if row is None:
        raise NotFoundError("LinkedIn auth token is not connected")
    return _row_to_stored_token(row, settings)


def get_auth_status(database_url: str | None = None) -> AuthStatus:
    try:
        token = get_stored_token(database_url=database_url)
    except NotFoundError:
        return AuthStatus(connected=False, message="LinkedIn is not connected")
    return AuthStatus(
        connected=True,
        scopes=token.scopes,
        expires_at=token.expires_at,
        member_urn=token.member_urn,
        needs_member_urn_verification=not bool(token.member_urn),
        message="LinkedIn token stored",
    )


def token_is_expired(expires_at: str | None) -> bool:
    if not expires_at:
        return False
    normalized = expires_at.replace("Z", "+00:00")
    try:
        parsed = datetime.fromisoformat(normalized)
    except ValueError:
        return True
    return parsed <= datetime.now(UTC)
