from __future__ import annotations

from fastapi.testclient import TestClient

from linkedin_publisher.draft_service import list_drafts
from linkedin_publisher.main import app
from linkedin_publisher.models import DraftStatus


def test_web_import_detail_edit_and_approve(tmp_path, monkeypatch):
    monkeypatch.setenv("DATABASE_URL", f"sqlite:///{tmp_path / 'app.db'}")

    with TestClient(app) as client:
        response = client.post(
            "/drafts",
            data={
                "source_material": "notes",
                "draft_text": "Web draft",
                "language": "en",
                "content_pillar": "",
            },
        )
        assert response.status_code == 200
        assert "Web draft" in response.text

        draft = list_drafts()[0]

        response = client.post(
            f"/drafts/{draft.id}/save",
            data={"final_text": "Web final", "revision_note": "manual edit"},
        )
        assert response.status_code == 200
        assert "Web final" in response.text

        response = client.post(f"/drafts/{draft.id}/approve")
        assert response.status_code == 200

        approved = list_drafts()[0]
        assert approved.status == DraftStatus.APPROVED
        assert "approved" in response.text


def test_web_publish_requires_typed_confirmation(tmp_path, monkeypatch):
    monkeypatch.setenv("DATABASE_URL", f"sqlite:///{tmp_path / 'app.db'}")

    with TestClient(app) as client:
        client.post(
            "/drafts",
            data={
                "source_material": "notes",
                "draft_text": "Web draft",
                "language": "en",
                "content_pillar": "",
            },
        )
        draft = list_drafts()[0]
        client.post(f"/drafts/{draft.id}/approve")

        response = client.post(f"/drafts/{draft.id}/publish", data={})
        assert response.status_code == 200
        assert "Type PUBLISH" in response.text

        response = client.post(
            f"/drafts/{draft.id}/publish",
            data={"typed_confirmation": "publish"},
        )
        assert response.status_code == 200
        assert "Type PUBLISH" in response.text

        saved = list_drafts()[0]
        assert saved.status == DraftStatus.APPROVED
