from dataclasses import dataclass
import os
from pathlib import Path

from dotenv import load_dotenv


@dataclass(frozen=True)
class Settings:
    app_env: str = "local"
    app_secret_key: str = "change_me"
    database_url: str = "sqlite:///./data/app.db"
    linkedin_client_id: str = ""
    linkedin_client_secret: str = ""
    linkedin_redirect_uri: str = "http://localhost:8000/auth/linkedin/callback"
    linkedin_scopes: str = "openid profile w_member_social"
    linkedin_member_urn: str = ""
    linkedin_api_version: str = "202605"
    writing_skill_path: str = "../linkedin-style-writer-skill"


def get_settings() -> Settings:
    load_dotenv(Path.cwd() / ".env")
    load_dotenv(Path(__file__).resolve().parents[2] / ".env")
    return Settings(
        app_env=os.getenv("APP_ENV", Settings.app_env),
        app_secret_key=os.getenv("APP_SECRET_KEY", Settings.app_secret_key),
        database_url=os.getenv("DATABASE_URL", Settings.database_url),
        linkedin_client_id=os.getenv("LINKEDIN_CLIENT_ID", ""),
        linkedin_client_secret=os.getenv("LINKEDIN_CLIENT_SECRET", ""),
        linkedin_redirect_uri=os.getenv(
            "LINKEDIN_REDIRECT_URI",
            Settings.linkedin_redirect_uri,
        ),
        linkedin_scopes=os.getenv("LINKEDIN_SCOPES", Settings.linkedin_scopes),
        linkedin_member_urn=os.getenv("LINKEDIN_MEMBER_URN", ""),
        linkedin_api_version=os.getenv("LINKEDIN_API_VERSION", Settings.linkedin_api_version),
        writing_skill_path=os.getenv("WRITING_SKILL_PATH", Settings.writing_skill_path),
    )
