# Edge Case Checklist

## Purpose

Use this checklist to challenge the plan before implementation starts.

## Checklist

- Empty or null data
- Partial or stale data
- Slow network responses
- Request failure or timeout
- Unauthorized or expired session
- Duplicate submission or repeated tap/click
- Screen revisit after navigation back
- Background and foreground app transitions
- Race conditions between requests or state updates
- Feature flag disabled or partially enabled
- Different device sizes or browsers
- Unexpected but valid user input
- Localization or long-string overflow if relevant
- Analytics or tracking side effects if relevant

## Decision Rule

If any listed edge case would materially change the implementation approach, mark the plan as `needs clarification first`.
