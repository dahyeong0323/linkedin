from __future__ import annotations

import secrets
from urllib.parse import quote

from fastapi import APIRouter, Request
from fastapi.responses import RedirectResponse
from starlette import status

from linkedin_publisher.errors import AuthStateError, PublisherError
from linkedin_publisher.linkedin_auth import (
    build_authorization_url,
    exchange_code_for_token,
    fetch_userinfo,
    get_auth_status,
    store_token,
)


router = APIRouter(prefix="/auth")
STATE_COOKIE = "linkedin_oauth_state"


def _templates(request: Request):
    return request.app.state.templates


def _status_response(request: Request, error: str | None = None):
    return _templates(request).TemplateResponse(
        request,
        "auth_status.html",
        {"status": get_auth_status(), "error": error},
    )


@router.get("/status")
def auth_status(request: Request, error: str | None = None):
    return _status_response(request, error)


@router.get("/linkedin")
def start_linkedin_auth():
    try:
        state = secrets.token_urlsafe(32)
        url = build_authorization_url(state)
    except PublisherError as exc:
        return RedirectResponse(
            f"/auth/status?error={quote(str(exc))}",
            status_code=status.HTTP_303_SEE_OTHER,
        )
    response = RedirectResponse(url, status_code=status.HTTP_303_SEE_OTHER)
    response.set_cookie(
        STATE_COOKIE,
        state,
        httponly=True,
        secure=False,
        samesite="lax",
        max_age=600,
    )
    return response


@router.get("/linkedin/callback")
def linkedin_callback(
    request: Request,
    code: str | None = None,
    state: str | None = None,
    error: str | None = None,
    error_description: str | None = None,
):
    if error:
        return _status_response(request, f"LinkedIn OAuth error: {error_description or error}")
    try:
        expected_state = request.cookies.get(STATE_COOKIE)
        if not expected_state or not state or state != expected_state:
            raise AuthStateError("LinkedIn OAuth state did not match")
        if not code:
            raise AuthStateError("LinkedIn OAuth callback did not include code")
        token_response = exchange_code_for_token(code)
        userinfo = fetch_userinfo(token_response["access_token"])
        # Do not infer Posts API author URN from OIDC sub automatically.
        token = store_token(token_response)
        member_note = (
            "LINKEDIN_MEMBER_URN is set"
            if token.member_urn
            else "member URN still needs verification before publishing"
        )
        response = _status_response(
            request,
            f"Connected. OIDC sub received: {bool(userinfo.get('sub'))}; {member_note}.",
        )
        response.delete_cookie(STATE_COOKIE)
        return response
    except PublisherError as exc:
        return _status_response(request, str(exc))
