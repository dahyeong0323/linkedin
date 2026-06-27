from __future__ import annotations

from fastapi import APIRouter, Form, Request
from fastapi.responses import RedirectResponse
from starlette import status
from urllib.parse import quote

from linkedin_publisher.draft_service import (
    create_draft,
    get_draft,
    list_drafts,
    list_revisions,
    save_final_text,
)
from linkedin_publisher.errors import PublisherError
from linkedin_publisher.review_service import (
    approve_draft,
    recover_failed_draft,
    reject_draft,
    request_revision,
)
from linkedin_publisher.schemas import DraftCreate


router = APIRouter()


def _templates(request: Request):
    return request.app.state.templates


def _redirect(path: str) -> RedirectResponse:
    return RedirectResponse(path, status_code=status.HTTP_303_SEE_OTHER)


@router.get("/")
def home() -> RedirectResponse:
    return _redirect("/drafts")


@router.get("/drafts")
def drafts_list(request: Request, status_filter: str | None = None, language: str | None = None):
    drafts = list_drafts(status=status_filter, language=language)
    return _templates(request).TemplateResponse(
        request,
        "drafts_list.html",
        {
            "drafts": drafts,
            "status_filter": status_filter or "",
            "language": language or "",
        },
    )


@router.post("/drafts")
def create_draft_from_form(
    source_material: str = Form(""),
    draft_text: str = Form(...),
    language: str = Form("en"),
    content_pillar: str = Form(""),
):
    draft = create_draft(
        DraftCreate(
            source_material=source_material,
            draft_text=draft_text,
            language=language or "en",
            content_pillar=content_pillar or None,
        )
    )
    return _redirect(f"/drafts/{draft.id}")


@router.get("/drafts/{draft_id}")
def draft_detail(request: Request, draft_id: str, error: str | None = None):
    draft = get_draft(draft_id)
    revisions = list_revisions(draft_id)
    return _templates(request).TemplateResponse(
        request,
        "draft_detail.html",
        {
            "draft": draft,
            "revisions": revisions,
            "error": error,
        },
    )


@router.post("/drafts/{draft_id}/save")
def save_draft_edits(
    draft_id: str,
    final_text: str = Form(...),
    revision_note: str = Form(""),
):
    try:
        save_final_text(draft_id, final_text, revision_note=revision_note or None)
    except PublisherError as exc:
        return _redirect(f"/drafts/{draft_id}?error={quote(str(exc))}")
    return _redirect(f"/drafts/{draft_id}")


@router.post("/drafts/{draft_id}/request-revision")
def request_draft_revision(draft_id: str, note: str = Form(...)):
    try:
        request_revision(draft_id, note)
    except PublisherError as exc:
        return _redirect(f"/drafts/{draft_id}?error={quote(str(exc))}")
    return _redirect(f"/drafts/{draft_id}")


@router.post("/drafts/{draft_id}/approve")
def approve_draft_route(draft_id: str):
    try:
        approve_draft(draft_id)
    except PublisherError as exc:
        return _redirect(f"/drafts/{draft_id}?error={quote(str(exc))}")
    return _redirect(f"/drafts/{draft_id}")


@router.post("/drafts/{draft_id}/reject")
def reject_draft_route(draft_id: str):
    try:
        reject_draft(draft_id)
    except PublisherError as exc:
        return _redirect(f"/drafts/{draft_id}?error={quote(str(exc))}")
    return _redirect(f"/drafts/{draft_id}")


@router.post("/drafts/{draft_id}/recover-failed")
def recover_failed_draft_route(draft_id: str):
    try:
        recover_failed_draft(draft_id)
    except PublisherError as exc:
        return _redirect(f"/drafts/{draft_id}?error={quote(str(exc))}")
    return _redirect(f"/drafts/{draft_id}")
