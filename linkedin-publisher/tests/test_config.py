from __future__ import annotations

from linkedin_publisher.config import get_settings


def test_get_settings_loads_dotenv_from_current_directory(tmp_path, monkeypatch):
    monkeypatch.chdir(tmp_path)
    monkeypatch.delenv("APP_SECRET_KEY", raising=False)
    monkeypatch.delenv("LINKEDIN_CLIENT_ID", raising=False)
    (tmp_path / ".env").write_text(
        "APP_SECRET_KEY=local-test-secret\nLINKEDIN_CLIENT_ID=dotenv-client\n",
        encoding="utf-8",
    )

    settings = get_settings()

    assert settings.app_secret_key == "local-test-secret"
    assert settings.linkedin_client_id == "dotenv-client"
