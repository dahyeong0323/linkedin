# LinkedIn Publisher

Local-first LinkedIn Publisher Module for reviewing, approving, and publishing drafts produced by the separate LinkedIn writing skill.

## Status

Version: `0.1.1`

v0.1.1 is ready as a local MVP code release. Draft storage, import, review workflow, minimal web UI, LinkedIn OAuth wiring, Posts API client, approved-only publish flow, and guardrail tests are available.

Real LinkedIn OAuth and real posting still require user-provided LinkedIn developer credentials, granted `w_member_social`, and a verified `LINKEDIN_MEMBER_URN`.

## Scope

- Separate from `../linkedin-style-writer-skill`
- Python + FastAPI
- SQLite
- Minimal server-rendered web UI
- Personal profile text-only publishing through the official LinkedIn API

## Local Setup

```bash
python -m venv .venv
.venv\Scripts\activate
python -m pip install -e ".[dev]"
copy .env.example .env
python -m uvicorn linkedin_publisher.main:app --reload
```

Then open:

```text
http://localhost:8000
```

## Phase Notes

P7-P9 include OAuth and publishing code, but a real LinkedIn post still requires local `.env` credentials, granted `w_member_social`, a verified `LINKEDIN_MEMBER_URN`, and an explicitly approved draft.

P10 adds guardrail coverage for blocked publish states, missing/expired auth, empty text, dry-run behavior, and mocked LinkedIn API errors.

P11 adds release artifacts: `VERSION`, `CHANGELOG.md`, and `docs/RELEASE_CHECKLIST.md`.

v0.1.1 adds pre-live-post safety fixes:

- `.env` is loaded automatically for CLI and FastAPI settings.
- Live publish uses an atomic `approved -> publishing` claim before calling LinkedIn.
- Web live publish requires typing `PUBLISH`.
- Failed drafts can be explicitly recovered to `pending_review`, then must be re-approved.
- OAuth token storage is blocked if `APP_SECRET_KEY` is unset or still `change_me`.
- v0.1 accepts only `urn:li:person:` author URNs.
- Live publish requires stored scopes to include `w_member_social`.

## CLI Helpers

```bash
publisher init-db
publisher import-draft path\to\draft.md
publisher list
publisher show draft_20260626_0001
publisher approve draft_20260626_0001
publisher reject draft_20260626_0001
publisher recover-failed draft_20260626_0001
publisher auth-status
publisher publish draft_20260626_0001 --confirm
```

`publisher publish` refuses to run unless `--confirm` is present.

## Web Flow

1. Open `/drafts`.
2. Import a draft.
3. Edit the final text.
4. Approve the draft.
5. Open the publish confirmation page.
6. Type `PUBLISH` and confirm publishing.

The app blocks publishing unless the draft is approved, LinkedIn auth is connected, token expiration is acceptable, the member URN is configured, and the confirmation page submits the publish action.

## LinkedIn Configuration

Create `.env` from `.env.example` and fill:

```env
APP_ENV=local
APP_SECRET_KEY=replace_with_a_strong_random_secret
DATABASE_URL=sqlite:///./data/app.db

LINKEDIN_CLIENT_ID=
LINKEDIN_CLIENT_SECRET=
LINKEDIN_REDIRECT_URI=http://localhost:8000/auth/linkedin/callback
LINKEDIN_SCOPES=openid profile w_member_social
LINKEDIN_MEMBER_URN=
LINKEDIN_API_VERSION=202605
```

Do not set `LINKEDIN_MEMBER_URN` by guessing from OIDC `sub`. Verify the Posts API author URN first.

Do not leave `APP_SECRET_KEY` as `change_me`. LinkedIn OAuth token storage is blocked until this value is changed to a strong local secret. Keep it stable after connecting LinkedIn, because stored tokens are encrypted with this value.

## Verification

From the workspace root:

```bash
python -m pytest linkedin-publisher\tests -q
```

From `linkedin-publisher`:

```bash
$env:PYTHONPATH='src'
python -m linkedin_publisher.cli --help
python -m linkedin_publisher.cli auth-status
```

## Known Limits

- Local-only MVP.
- Personal profile text-only posting only.
- No company page posting.
- No image/document/carousel posting.
- No analytics in v0.1.
- No scraping or browser automation.
- No automated engagement actions.
- Real LinkedIn posting has not been live-tested until credentials and explicit test-post approval are provided.
