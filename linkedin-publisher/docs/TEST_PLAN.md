# Test Plan

## Scope Through P10

The current automated test suite covers:

- SQLite schema creation.
- Draft create, import, list, detail, edit, and revision history.
- Review workflow status transitions.
- Invalid review transitions.
- LinkedIn OAuth authorization URL generation.
- Local token storage and auth status.
- LinkedIn text post payload generation.
- LinkedIn Posts API headers.
- LinkedIn API error mapping for 401, 403, 429, and 500.
- Approved-only publish guard.
- Explicit confirmation guard.
- Token missing guard.
- Member URN missing guard.
- Expired token guard.
- Empty text guard.
- Rejected draft publish guard.
- Pending review draft publish guard.
- Published draft re-publish guard.
- Dry-run publish payload generation without status mutation.
- Publish success status/URN/export persistence.
- Publish failure status/error persistence.
- Minimal web UI import, edit, and approval flow.
- Automatic `.env` loading from the current working directory.
- Weak/default `APP_SECRET_KEY` blocking token storage.
- Personal profile URN enforcement.
- `w_member_social` preflight enforcement.
- Web typed `PUBLISH` confirmation.
- Failed draft recovery to `pending_review`.
- Duplicate publish claim guard.

## Current Verification Command

```bash
python -m pytest tests -q
```

From the repository root:

```bash
python -m pytest linkedin-publisher\tests -q
```

## Manual Tests Still Required

These require real LinkedIn developer credentials and should not be faked:

- Real OAuth redirect round trip.
- Verification of the authenticated member URN for the Posts API `author` field.
- One explicit approved test post to the user's personal LinkedIn profile.
- Confirmation that LinkedIn returns and the app stores the expected post URN.

Do not run the real post test until the user explicitly provides a test post and confirms that it may be published.
