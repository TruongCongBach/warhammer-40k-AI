# UI State Coverage Checklist

## Purpose

Use this checklist to verify that the implementation covers more than the happy path.

## Checklist

- Initial loading state
- Background refresh state
- Empty state
- Error state
- Disabled state
- Success confirmation state if relevant
- Retry state after failure
- Partial data or degraded state
- Slow-network behavior
- Duplicate action prevention
- Transition state after submit, save, or navigation
- Unauthorized or expired-session state if relevant

## Review Rule

If a missing state would plausibly create user confusion, a dead end, or a repeated support issue, surface it as a material review finding.
