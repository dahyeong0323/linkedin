from __future__ import annotations

from contextlib import contextmanager
from pathlib import Path
import sqlite3
from typing import Iterator

from linkedin_publisher.config import get_settings


SCHEMA_STATEMENTS = [
    """
    CREATE TABLE IF NOT EXISTS drafts (
      id TEXT PRIMARY KEY,
      created_at TEXT NOT NULL,
      updated_at TEXT NOT NULL,
      input_type TEXT NOT NULL,
      source_material TEXT NOT NULL,
      draft_text TEXT NOT NULL,
      final_text TEXT,
      language TEXT NOT NULL,
      content_pillar TEXT,
      status TEXT NOT NULL,
      risk_notes_json TEXT NOT NULL DEFAULT '[]',
      self_review_json TEXT NOT NULL DEFAULT '{}',
      approved_at TEXT,
      approved_by TEXT,
      published_at TEXT,
      linkedin_post_urn TEXT,
      linkedin_url TEXT,
      publish_error TEXT
    )
    """,
    """
    CREATE TABLE IF NOT EXISTS draft_revisions (
      id INTEGER PRIMARY KEY AUTOINCREMENT,
      draft_id TEXT NOT NULL,
      created_at TEXT NOT NULL,
      previous_text TEXT NOT NULL,
      new_text TEXT NOT NULL,
      revision_note TEXT,
      FOREIGN KEY (draft_id) REFERENCES drafts(id)
    )
    """,
    """
    CREATE TABLE IF NOT EXISTS auth_tokens (
      id INTEGER PRIMARY KEY AUTOINCREMENT,
      provider TEXT NOT NULL,
      created_at TEXT NOT NULL,
      updated_at TEXT NOT NULL,
      access_token_encrypted TEXT NOT NULL,
      refresh_token_encrypted TEXT,
      expires_at TEXT,
      scopes TEXT,
      member_urn TEXT
    )
    """,
    """
    CREATE TABLE IF NOT EXISTS audit_events (
      id INTEGER PRIMARY KEY AUTOINCREMENT,
      created_at TEXT NOT NULL,
      event_type TEXT NOT NULL,
      draft_id TEXT,
      details_json TEXT NOT NULL DEFAULT '{}'
    )
    """,
]


def sqlite_path_from_url(database_url: str | None = None) -> Path:
    url = database_url or get_settings().database_url
    if url == "sqlite:///:memory:":
        return Path(":memory:")
    if not url.startswith("sqlite:///"):
        raise ValueError(f"Only sqlite:/// URLs are supported for MVP, got: {url}")
    raw_path = url.removeprefix("sqlite:///")
    return Path(raw_path)


def connect(database_url: str | None = None) -> sqlite3.Connection:
    db_path = sqlite_path_from_url(database_url)
    if str(db_path) != ":memory:":
        db_path.parent.mkdir(parents=True, exist_ok=True)
    conn = sqlite3.connect(str(db_path))
    conn.row_factory = sqlite3.Row
    conn.execute("PRAGMA foreign_keys = ON")
    return conn


def init_db(database_url: str | None = None) -> None:
    with connect(database_url) as conn:
        for statement in SCHEMA_STATEMENTS:
            conn.execute(statement)
        conn.commit()


@contextmanager
def session(database_url: str | None = None) -> Iterator[sqlite3.Connection]:
    conn = connect(database_url)
    try:
        yield conn
        conn.commit()
    except Exception:
        conn.rollback()
        raise
    finally:
        conn.close()
