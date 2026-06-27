from __future__ import annotations

from datetime import UTC, datetime
import json
import sqlite3
from typing import Any


def utc_now_iso() -> str:
    return datetime.now(UTC).replace(microsecond=0).isoformat().replace("+00:00", "Z")


def record_event(
    conn: sqlite3.Connection,
    event_type: str,
    draft_id: str | None = None,
    details: dict[str, Any] | None = None,
) -> None:
    conn.execute(
        """
        INSERT INTO audit_events (created_at, event_type, draft_id, details_json)
        VALUES (?, ?, ?, ?)
        """,
        (
            utc_now_iso(),
            event_type,
            draft_id,
            json.dumps(details or {}, ensure_ascii=True, sort_keys=True),
        ),
    )
