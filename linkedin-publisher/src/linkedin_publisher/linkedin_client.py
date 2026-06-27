from __future__ import annotations

from dataclasses import dataclass
from typing import Any

import httpx

from linkedin_publisher.config import get_settings
from linkedin_publisher.errors import LinkedInApiError, ValidationError


POSTS_URL = "https://api.linkedin.com/rest/posts"


@dataclass(frozen=True)
class LinkedInPostResult:
    post_urn: str
    payload: dict[str, Any]
    status_code: int


def build_text_post_payload(author_urn: str, text: str) -> dict[str, Any]:
    if not author_urn.startswith("urn:li:person:"):
        raise ValidationError("LinkedIn v0.1 author must be a personal profile URN")
    if not text.strip():
        raise ValidationError("LinkedIn post text must not be empty")
    return {
        "author": author_urn,
        "commentary": text.strip(),
        "visibility": "PUBLIC",
        "distribution": {
            "feedDistribution": "MAIN_FEED",
            "targetEntities": [],
            "thirdPartyDistributionChannels": [],
        },
        "lifecycleState": "PUBLISHED",
        "isReshareDisabledByAuthor": False,
    }


def _safe_error_message(response: httpx.Response) -> str:
    text = response.text[:1000] if response.text else ""
    if response.status_code == 401:
        return "LinkedIn API returned 401. Re-authentication or token refresh is required."
    if response.status_code == 403:
        return "LinkedIn API returned 403. Check products, scopes, and member permissions."
    if response.status_code == 429:
        return "LinkedIn API returned 429. Rate limit hit; retry later."
    if 400 <= response.status_code < 500:
        return f"LinkedIn API returned {response.status_code}. Payload/config issue. {text}"
    if response.status_code >= 500:
        return f"LinkedIn API returned {response.status_code}. Temporary LinkedIn/server error. {text}"
    return f"LinkedIn API returned unexpected status {response.status_code}. {text}"


def create_text_post(
    *,
    access_token: str,
    author_urn: str,
    text: str,
    api_version: str | None = None,
    client: httpx.Client | None = None,
) -> LinkedInPostResult:
    settings = get_settings()
    payload = build_text_post_payload(author_urn, text)
    version = api_version or settings.linkedin_api_version
    owns_client = client is None
    client = client or httpx.Client(timeout=30)
    try:
        response = client.post(
            POSTS_URL,
            json=payload,
            headers={
                "Authorization": f"Bearer {access_token}",
                "Content-Type": "application/json",
                "Linkedin-Version": version,
                "X-Restli-Protocol-Version": "2.0.0",
            },
        )
    finally:
        if owns_client:
            client.close()
    if response.status_code >= 400:
        raise LinkedInApiError(_safe_error_message(response), response.status_code)

    post_urn = response.headers.get("x-restli-id") or response.headers.get("X-RestLi-Id")
    if not post_urn:
        try:
            body = response.json()
        except ValueError:
            body = {}
        post_urn = body.get("id") or body.get("urn")
    if not post_urn:
        post_urn = "[NEEDS_VERIFICATION: missing LinkedIn post URN in response]"
    return LinkedInPostResult(post_urn=post_urn, payload=payload, status_code=response.status_code)
