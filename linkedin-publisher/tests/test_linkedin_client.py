from __future__ import annotations

import httpx
import pytest

from linkedin_publisher.errors import LinkedInApiError, ValidationError
from linkedin_publisher.linkedin_client import build_text_post_payload, create_text_post


def test_build_text_post_payload():
    payload = build_text_post_payload("urn:li:person:abc", " Hello ")

    assert payload["author"] == "urn:li:person:abc"
    assert payload["commentary"] == "Hello"
    assert payload["visibility"] == "PUBLIC"
    assert payload["lifecycleState"] == "PUBLISHED"


def test_build_text_post_payload_requires_urn():
    with pytest.raises(ValidationError):
        build_text_post_payload("abc", "Hello")


def test_build_text_post_payload_requires_person_urn_for_v01():
    with pytest.raises(ValidationError, match="personal profile"):
        build_text_post_payload("urn:li:organization:123", "Hello")


def test_create_text_post_sends_headers_and_reads_restli_id():
    captured = {}

    def handler(request: httpx.Request) -> httpx.Response:
        captured["version"] = request.headers["Linkedin-Version"]
        captured["protocol"] = request.headers["X-Restli-Protocol-Version"]
        captured["auth"] = request.headers["Authorization"]
        return httpx.Response(201, headers={"x-restli-id": "urn:li:share:123"})

    client = httpx.Client(transport=httpx.MockTransport(handler))

    result = create_text_post(
        access_token="token",
        author_urn="urn:li:person:abc",
        text="Post text",
        api_version="202605",
        client=client,
    )

    assert result.post_urn == "urn:li:share:123"
    assert captured == {
        "version": "202605",
        "protocol": "2.0.0",
        "auth": "Bearer token",
    }


def test_create_text_post_maps_403_to_api_error():
    client = httpx.Client(transport=httpx.MockTransport(lambda request: httpx.Response(403, text="denied")))

    with pytest.raises(LinkedInApiError) as exc:
        create_text_post(
            access_token="token",
            author_urn="urn:li:person:abc",
            text="Post text",
            client=client,
        )

    assert exc.value.status_code == 403
