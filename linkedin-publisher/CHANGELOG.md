# Changelog

## 0.1.1 - 2026-06-27

### Fixed

- Load `.env` automatically from the current working directory and package root for consistent CLI/FastAPI configuration.
- Use an atomic `approved -> publishing` publish claim before calling the LinkedIn API.
- Require typed `PUBLISH` confirmation in the web publish form.
- Add explicit failed-draft recovery to `pending_review` instead of direct re-approval.
- Block LinkedIn token storage when `APP_SECRET_KEY` is missing or still `change_me`.
- Restrict v0.1 live publish author URNs to personal profile URNs starting with `urn:li:person:`.
- Require stored token scopes to include `w_member_social` before live publish.

### Verified

- Automated test suite: `37 passed`.

## 0.1.0 - 2026-06-27

### Added

- Local FastAPI app for LinkedIn draft review and publishing workflow.
- SQLite persistence for drafts, draft revisions, auth tokens, and audit events.
- Draft import, list, detail, edit, approve, reject, and revision request flow.
- Minimal server-rendered web UI for draft review.
- CLI helpers for database initialization, draft import/list/show, approve/reject, auth status, and publish.
- LinkedIn OAuth wiring for authorization URL, callback, token exchange, userinfo fetch, and local token storage.
- LinkedIn Posts API client for personal profile text-only post payloads.
- Approved-only publish flow with explicit confirmation page.
- Publish success/failure persistence, LinkedIn post URN storage, audit events, and published text export.
- LinkedIn Developer App setup guide.
- Guardrail test coverage for unsafe publish states, missing auth, missing member URN, expired token, empty text, dry-run behavior, and mocked LinkedIn API errors.

### Guardrails

- No automatic publishing.
- No scraping.
- No browser automation.
- No automated likes, comments, follows, connection requests, or engagement.
- No company page posting.
- No image, document, or carousel posting.
- No analytics fetch in v0.1.
- Publishing requires an approved draft, explicit confirmation, stored LinkedIn auth token, non-expired token, and verified `LINKEDIN_MEMBER_URN`.
- OIDC `sub` is not automatically treated as the Posts API author URN.

### Known Issues

- Real LinkedIn OAuth round trip has not been live-tested because local LinkedIn developer credentials were not provided.
- Real LinkedIn post creation has not been live-tested because `LINKEDIN_CLIENT_ID`, `LINKEDIN_CLIENT_SECRET`, granted `w_member_social`, and verified `LINKEDIN_MEMBER_URN` are still required.
- Token encryption is local MVP protection based on `APP_SECRET_KEY`; changing `APP_SECRET_KEY` invalidates stored tokens.
- LinkedIn public post URLs are not derived from every returned post URN.
- The app is local-only and not hardened for public deployment or multi-user use.

### Verified

- Automated test suite: `27 passed`.
- CLI smoke check confirms `publish` and `auth-status` commands are available.
