# Security Risk Checklist

Use this checklist when a ticket may touch security-sensitive behavior. The goal is not to run a full security audit. The goal is to catch material delivery risk early and make the workflow explicit when security review is needed.

## Check These Areas

- Authentication: login, logout, session refresh, token lifecycle, password reset, MFA, account linking
- Authorization: role checks, feature access, admin-only paths, tenant boundaries, resource ownership
- Sensitive data: PII, payment-related fields, addresses, phone numbers, secrets, tokens, identifiers
- Storage: secure storage, local storage, cookies, AsyncStorage, persisted state, cache, device files
- Logging and analytics: payload leakage, tokens in logs, sensitive query params, crash reports, analytics events
- Input handling: validation, sanitization, unsafe HTML, unsafe URL handling, uploads, file names, MIME checks
- Network boundaries: headers, auth propagation, retry storms, duplicated requests, insecure endpoints, trust of client-provided values
- UI trust signals: hidden controls vs enforced permission checks, admin actions exposed in the UI, copy that implies security but code does not enforce it
- Cross-boundary behavior: WebViews, deep links, redirects, external browser flows, embedded content, server/client boundary assumptions
- Operational impact: auditability, rollback risk, migration risk, backward compatibility for auth or permission changes

## What To Call Out

- Observed security-sensitive behavior
- Likely risk if the implementation is wrong
- Confidence level: observed, likely, or unclear
- Missing information blocking a safe conclusion
- Whether the work should be marked `needs security review`

## Good Triggers For `needs security review`

- Permission logic changed but the enforcement point is unclear
- Tokens, secrets, or PII may be stored or logged incorrectly
- Server/client ownership of validation or authorization is ambiguous
- Upload, WebView, or deep-link behavior changed in a trust-sensitive flow
- A ticket touches auth or payment-adjacent behavior and the acceptance criteria are incomplete

## Keep It Practical

- Do not escalate every UI change into a security review
- Do not ignore security because the ticket looks frontend-only
- Prefer explicit uncertainty over false confidence
