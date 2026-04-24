# Security Severity Guide

Use this guide to describe security risk consistently inside ticket workflows.

## Low

Use when:
- no sensitive data or permission boundary is affected
- the issue is mostly hygiene, clarity, or low-impact hardening
- exploitation is unlikely and impact is limited

Typical phrasing:
- `Low security relevance`
- `No clear security blocker, but worth tightening during implementation`

## Medium

Use when:
- auth, permissions, tokens, or user data are involved
- the ticket may expose incorrect behavior if assumptions are wrong
- mitigation is straightforward but should not be skipped

Typical phrasing:
- `Medium security risk if the current assumption is wrong`
- `Implementation should proceed only with explicit validation of the auth/data boundary`

## High

Use when:
- authorization may be bypassed
- sensitive data may leak through logs, client exposure, caching, or storage
- an unsafe upload, WebView, redirect, or trust boundary could be exploited
- the issue should block implementation approval or release readiness until clarified

Typical phrasing:
- `High security risk`
- `Needs security review before implementation/approval`

## Usage Rules

- Choose the lowest severity that still matches the likely impact
- Explain why the severity applies in one short sentence
- If certainty is low, say that directly instead of overstating severity
