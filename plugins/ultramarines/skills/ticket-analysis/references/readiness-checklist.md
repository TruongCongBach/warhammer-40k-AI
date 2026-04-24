# Readiness for Implementation Checklist

## Purpose

Use this checklist before recommending implementation.

## Checklist

- Ticket ID and issue type are known.
- Business impact is clear enough to prioritize the work.
- Expected behavior is explicit.
- Actual behavior is explicit.
- Acceptance criteria exist or can be reasonably inferred and stated.
- Core reproduction context is known: platform, route, user state, or environment.
- Attached images or logs have been reviewed when they exist.
- At least one plausible fix direction exists.
- Likely affected areas are identified.
- Key risks are known.
- Missing information is either minor or clearly listed as follow-up.

## Decision Rule

Recommend `Ready to implement` only when missing information is unlikely to change the fix direction materially.

Recommend `Not yet ready` when:
- the failure mode is still ambiguous
- the affected boundary is unknown
- acceptance criteria are missing and could change scope
- logs or screenshots contradict the ticket narrative
- critical reproduction details are absent
