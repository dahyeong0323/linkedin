from __future__ import annotations

import argparse

from linkedin_publisher.db import init_db
from linkedin_publisher.draft_service import get_draft, import_draft_file, list_drafts
from linkedin_publisher.errors import PublisherError
from linkedin_publisher.linkedin_auth import get_auth_status
from linkedin_publisher.publisher_service import publish_draft
from linkedin_publisher.review_service import approve_draft, recover_failed_draft, reject_draft


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="publisher")
    sub = parser.add_subparsers(dest="command", required=True)

    sub.add_parser("init-db")

    import_parser = sub.add_parser("import-draft")
    import_parser.add_argument("path")
    import_parser.add_argument("--source-material", default="")
    import_parser.add_argument("--language", default="en")
    import_parser.add_argument("--content-pillar")

    sub.add_parser("list")

    show_parser = sub.add_parser("show")
    show_parser.add_argument("draft_id")

    approve_parser = sub.add_parser("approve")
    approve_parser.add_argument("draft_id")

    reject_parser = sub.add_parser("reject")
    reject_parser.add_argument("draft_id")

    recover_parser = sub.add_parser("recover-failed")
    recover_parser.add_argument("draft_id")

    publish_parser = sub.add_parser("publish")
    publish_parser.add_argument("draft_id")
    publish_parser.add_argument("--confirm", action="store_true")
    publish_parser.add_argument("--dry-run", action="store_true")

    sub.add_parser("auth-status")

    return parser


def main(argv: list[str] | None = None) -> None:
    parser = build_parser()
    args = parser.parse_args(argv)
    try:
        if args.command == "init-db":
            init_db()
            print("Database initialized")
        elif args.command == "import-draft":
            draft = import_draft_file(
                args.path,
                source_material=args.source_material,
                language=args.language,
                content_pillar=args.content_pillar,
            )
            print(f"Imported {draft.id}")
        elif args.command == "list":
            for draft in list_drafts():
                preview = draft.publish_text.splitlines()[0][:80] if draft.publish_text else ""
                print(f"{draft.id}\t{draft.status.value}\t{draft.language}\t{preview}")
        elif args.command == "show":
            draft = get_draft(args.draft_id)
            print(f"{draft.id} [{draft.status.value}]")
            print(draft.publish_text)
        elif args.command == "approve":
            draft = approve_draft(args.draft_id)
            print(f"Approved {draft.id}")
        elif args.command == "reject":
            draft = reject_draft(args.draft_id)
            print(f"Rejected {draft.id}")
        elif args.command == "recover-failed":
            draft = recover_failed_draft(args.draft_id)
            print(f"Recovered {draft.id} to {draft.status.value}")
        elif args.command == "publish":
            result = publish_draft(
                args.draft_id,
                confirmed=args.confirm,
                dry_run=args.dry_run,
            )
            if result.dry_run:
                print(result.payload)
            else:
                print(f"Published {result.draft.id}: {result.post_urn}")
        elif args.command == "auth-status":
            status = get_auth_status()
            print(f"connected={status.connected}")
            print(f"scopes={status.scopes or ''}")
            print(f"expires_at={status.expires_at or ''}")
            print(f"member_urn={status.member_urn or '[NEEDS_VERIFICATION]'}")
    except PublisherError as exc:
        parser.exit(1, f"error: {exc}\n")


if __name__ == "__main__":
    main()
