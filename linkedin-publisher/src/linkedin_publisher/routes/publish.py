from __future__ import annotations

from fastapi import APIRouter, Form, Request
from fastapi.responses import RedirectResponse
from starlette import status
from urllib.parse import quote

from linkedin_publisher.draft_service import get_draft
from linkedin_publisher.errors import PublisherError, ValidationError
from linkedin_publisher.publisher_service import publish_draft


router = APIRouter()


def _templates(request: Request):
    return request.app.state.templates


def _redirect(path: str) -> RedirectResponse:
    return RedirectResponse(path, status_code=status.HTTP_303_SEE_OTHER)


@router.get("/drafts/{draft_id}/publish-confirm")
def publish_confirm(request: Request, draft_id: str, error: str | None = None):
    draft = get_draft(draft_id)
    return _templates(request).TemplateResponse(
        request,
        "publish_confirm.html",
        {"draft": draft, "error": error},
    )


@router.post("/drafts/{draft_id}/publish")
def publish_confirmed(draft_id: str, typed_confirmation: str = Form("")):
    try:
        if typed_confirmation.strip() != "PUBLISH":
            raise ValidationError("Type PUBLISH to confirm live publishing")
        publish_draft(draft_id, confirmed=True)
    except PublisherError as exc:
        return _redirect(f"/drafts/{draft_id}/publish-confirm?error={quote(str(exc))}")
    return _redirect(f"/drafts/{draft_id}")
