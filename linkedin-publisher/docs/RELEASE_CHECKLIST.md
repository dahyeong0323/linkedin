# Release Checklist

## v0.1.1 Scope

The v0.1.1 release is a local-first LinkedIn Publisher Module for:

- Draft import.
- Draft review.
- Draft editing.
- Explicit approval.
- Approved-only LinkedIn personal profile text posting.
- Publish logging.
- Guardrail tests.

## Checklist

- [x] Existing writing skill remains separate and unmodified.
- [x] SQLite DB initialization is implemented.
- [x] Draft import is implemented.
- [x] Draft list/detail UI is implemented.
- [x] Draft edit is implemented.
- [x] Approve/reject/revision request workflow is implemented.
- [x] Approved-only publish guard is implemented.
- [x] Publish confirmation page is implemented.
- [x] LinkedIn OAuth routes are implemented.
- [x] LinkedIn text-only Posts API client is implemented.
- [x] Post URN storage is implemented.
- [x] Publish failure logging is implemented.
- [x] `.env` is ignored by git.
- [x] Token values are not logged by app code.
- [x] README is updated.
- [x] Test plan is documented.
- [x] Automated tests pass.
- [x] `.env` is loaded automatically by config.
- [x] Live publish uses atomic `approved -> publishing` claim.
- [x] Web live publish requires typed `PUBLISH` confirmation.
- [x] Failed drafts can be explicitly recovered to `pending_review`.
- [x] Weak/default `APP_SECRET_KEY` blocks token storage.
- [x] v0.1 publish accepts only personal profile URNs.
- [x] Live publish requires `w_member_social`.
- [ ] Real LinkedIn Developer App credentials have been provided.
- [ ] Real OAuth callback has been completed locally.
- [ ] Authenticated member URN has been verified for Posts API `author`.
- [ ] Real LinkedIn test post has been explicitly approved and published.

## Verification Commands

Run from the workspace root:

```bash
python -m pytest linkedin-publisher\tests -q
```

Run from `linkedin-publisher`:

```bash
$env:PYTHONPATH='src'
python -m linkedin_publisher.cli --help
python -m linkedin_publisher.cli auth-status
```

## Release Decision

v0.1.1 is ready as a local MVP code release.

It is not yet live-verified against LinkedIn production APIs. Live verification requires user-provided LinkedIn developer app credentials, granted `w_member_social`, a verified `LINKEDIN_MEMBER_URN`, and explicit approval of a test post.
