# LinkedIn Publisher Review Handoff

This document explains which files should be reviewed, which files must not be shared, and what the reviewer should verify before approving the LinkedIn Publisher Module.

## 1. First Files To Review

Start with these files:

```text
linkedin-publisher/
  README.md
  docs/RELEASE_CHECKLIST.md
  CHANGELOG.md
  VERSION
  pyproject.toml
```

Purpose:

- Understand what the project is supposed to do.
- Confirm local setup and execution steps.
- Confirm the release scope.
- Confirm v0.1.0 release criteria.
- Confirm known limits and live LinkedIn testing prerequisites.

## 2. Core Code To Review

Review the full `src` tree:

```text
linkedin-publisher/src/
```

The exact file names differ from the early spec, but the important logic is here:

```text
linkedin-publisher/src/linkedin_publisher/
  cli.py
  models.py
  schemas.py
  config.py
  db.py
  draft_service.py
  review_service.py
  linkedin_auth.py
  linkedin_client.py
  publisher_service.py
  audit_log.py
  routes/
  templates/
```

Review these core behaviors:

1. Draft creation and storage.
2. Draft edit, approve, reject, and revision request state changes.
3. Blocking publish unless draft status is `approved`.
4. LinkedIn OAuth and token handling.
5. Status persistence after publish success or failure.

## 3. Tests To Review

Review the full test directory:

```text
linkedin-publisher/tests/
```

Important test coverage:

- Non-approved draft cannot be published.
- Already published draft cannot be published again.
- Missing token blocks publishing.
- Missing member URN blocks publishing.
- Expired token blocks publishing.
- Empty text blocks publishing.
- Dry-run does not call the real API or mutate publish status.
- LinkedIn API failure marks the draft as `failed`.
- Publish success stores post URN and exported final text.
- Original draft and revision history are preserved.

Current automated verification:

```text
27 passed
```

## 4. Configuration And Security Files

Review:

```text
linkedin-publisher/.env.example
linkedin-publisher/.gitignore
linkedin-publisher/src/linkedin_publisher/config.py
```

Only `.env.example` should be shared.

Never share:

```text
.env
token_store.json
any file containing access_token
any file containing refresh_token
any file containing client_secret
real LinkedIn credentials
```

## 5. Recommended Sharing Method

The best review package is a zip of the `linkedin-publisher` folder with local/generated/private files excluded.

Exclude:

```text
.env
token_store.json
__pycache__/
.pytest_cache/
.venv/
dist/
build/
*.egg-info/
uvicorn*.log
data/*.db
data/*.db-*
```

PowerShell quick zip command:

```powershell
Compress-Archive -Path .\linkedin-publisher\* -DestinationPath .\linkedin-publisher-review.zip
```

Before sending the zip, confirm that it does not include:

```text
.env
access tokens
refresh tokens
client secrets
real LinkedIn credentials
local SQLite DB files with user data
```

## 6. Minimal Review Package

If sending only the minimum set of files, include:

```text
linkedin-publisher/README.md
linkedin-publisher/docs/RELEASE_CHECKLIST.md
linkedin-publisher/CHANGELOG.md
linkedin-publisher/VERSION
linkedin-publisher/pyproject.toml
linkedin-publisher/.env.example
linkedin-publisher/.gitignore
linkedin-publisher/src/
linkedin-publisher/tests/
```

## 7. Final Review Questions

The reviewer should verify:

1. Is there any path that can publish without explicit approval?
2. Is duplicate publishing possible after a draft is already `published`?
3. Can OAuth tokens, access tokens, refresh tokens, or client secrets leak through logs, files, tests, or exports?
4. If publishing fails, is the draft left in a safe and inspectable state?
5. Are dry-run and live publish clearly separated?
6. Can a new user run the app by following only the README?
7. Is the live LinkedIn posting checklist clear before any real post happens?

## 8. Current Live-Test Status

The code release is ready as a local MVP, but live LinkedIn posting has not been completed yet.

v0.1.1 also requires the web user to type `PUBLISH` before live publish and blocks token storage until `APP_SECRET_KEY` is changed from the default.

Live posting still requires:

```text
LINKEDIN_CLIENT_ID
LINKEDIN_CLIENT_SECRET
granted w_member_social
verified LINKEDIN_MEMBER_URN
explicit user-approved test post
```

Do not run a real LinkedIn post until all of the above are available and explicitly confirmed.
