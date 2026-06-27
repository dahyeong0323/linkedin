# LinkedIn Developer App Setup

Last verified against official Microsoft Learn / LinkedIn documentation on 2026-06-27.

## Goal

Configure a LinkedIn Developer App for local MVP testing of personal profile text-only posting through the official LinkedIn API.

This guide does not enable company page posting, scraping, browser automation, analytics, automated likes, automated comments, follows, connection requests, or collection of other people's LinkedIn data.

## Official References

- Getting Access to LinkedIn APIs: https://learn.microsoft.com/en-us/linkedin/shared/authentication/getting-access
- Sign In with LinkedIn using OpenID Connect: https://learn.microsoft.com/en-us/linkedin/consumer/integrations/self-serve/sign-in-with-linkedin-v2
- Posts API: https://learn.microsoft.com/en-us/linkedin/marketing/community-management/shares/posts-api
- Refresh Tokens with OAuth 2.0: https://learn.microsoft.com/en-us/linkedin/shared/authentication/programmatic-refresh-tokens

## Required Products And Scopes

For the MVP, request only the products/scopes needed for local personal profile posting:

| Product | Scope | Purpose |
|---|---|---|
| Sign in with LinkedIn using OpenID Connect | `openid` | Request an ID token. |
| Sign in with LinkedIn using OpenID Connect | `profile` | Retrieve basic authenticated member profile claims. |
| Share on LinkedIn | `w_member_social` | Post on behalf of the authenticated member. |

Do not request company page scopes for v0.1.

Do not request analytics scopes for v0.1.

## Create The LinkedIn App

1. Go to the LinkedIn Developer Portal.
2. Create a new app.
3. Complete required app identity fields.
4. Open the app's Products tab.
5. Request or enable:
   - Sign in with LinkedIn using OpenID Connect
   - Share on LinkedIn
6. Confirm `w_member_social` is granted before attempting to post.

If a required product or permission is not available, stop the implementation and mark the issue as `[NEEDS_USER_INPUT]`.

## Redirect URI

For local MVP development, configure this authorized redirect URI:

```text
http://localhost:8000/auth/linkedin/callback
```

It must match `.env` exactly:

```env
LINKEDIN_REDIRECT_URI=http://localhost:8000/auth/linkedin/callback
```

## Local Environment

Create `.env` from `.env.example` and fill:

```env
LINKEDIN_CLIENT_ID=
LINKEDIN_CLIENT_SECRET=
LINKEDIN_REDIRECT_URI=http://localhost:8000/auth/linkedin/callback
LINKEDIN_SCOPES=openid profile w_member_social
LINKEDIN_MEMBER_URN=
LINKEDIN_API_VERSION=202605
```

Never commit `.env`.

Never paste access tokens or refresh tokens into chat, logs, screenshots, or commit history.

## OAuth Notes

LinkedIn uses OAuth 2.0 for API authorization. The OIDC documentation says the current Sign In with LinkedIn flow uses `openid`, `profile`, and optional `email` scopes.

For this MVP, `email` is not required.

The OIDC userinfo endpoint returns a `sub` field, but the Posts API requires an author URN such as a member/person URN. Do not hardcode the author URN. During P7/P8, verify the exact member identifier mapping using official docs and an actual OAuth response. If it is uncertain, stop and mark `[NEEDS_VERIFICATION]`.

The current implementation intentionally does not infer `urn:li:person:{sub}` automatically. Set `LINKEDIN_MEMBER_URN` only after the authenticated member URN is verified for the Posts API author field.

## Posts API Notes

Official Posts API docs require:

- Endpoint: `POST https://api.linkedin.com/rest/posts`
- Header: `Authorization: Bearer <access token>`
- Header: `X-Restli-Protocol-Version: 2.0.0`
- Header: `Linkedin-Version: YYYYMM`
- Header: `Content-Type: application/json`

The docs also note that LinkedIn Marketing API versions sunset. Before implementing P8/P9, choose a currently supported `Linkedin-Version` from the official versioned API documentation.

## MVP Text-Only Payload Shape

The implementation may start from this shape only after the member author URN is verified:

```json
{
  "author": "urn:li:person:{verified_member_id}",
  "commentary": "Approved LinkedIn post text",
  "visibility": "PUBLIC",
  "distribution": {
    "feedDistribution": "MAIN_FEED",
    "targetEntities": [],
    "thirdPartyDistributionChannels": []
  },
  "lifecycleState": "PUBLISHED",
  "isReshareDisabledByAuthor": false
}
```

## Refresh Token Notes

LinkedIn documents that access tokens are valid for a limited period and refresh-token behavior depends on approved access. The MVP should support re-authentication when refresh is unavailable, expired, revoked, or not approved.

Store token expiration metadata. Do not assume refresh tokens will always be issued.

## Stop Conditions

Stop and ask for input if any of these are true:

- The app does not have `w_member_social`.
- The redirect URI cannot be configured exactly.
- OAuth returns scopes different from the requested scopes.
- The authenticated member identifier cannot be safely mapped to the Posts API `author`.
- The selected `Linkedin-Version` is not currently supported.
- LinkedIn returns 401, 403, or a permission/product error during a real post test.

## Implemented Local Endpoints

- `/auth/status`
- `/auth/linkedin`
- `/auth/linkedin/callback`
- `/drafts/{draft_id}/publish-confirm`
- `/drafts/{draft_id}/publish`

Publishing remains blocked until the user confirms the publish action from the confirmation page.
