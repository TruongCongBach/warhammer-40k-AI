# Ticket Analysis Template

## Purpose

Use this template for the main triage output. Keep it concise, evidence-based, and easy to scan.

## Template

```markdown
Suggested title
- type: TICKET-ID | short summary

Suggested commit message
- type: TICKET-ID | short summary

Suggested ticket comment title
- type: TICKET-ID | short summary

Ticket summary
- Ticket: TICKET-ID
- Type: bug | feature | chore | refactor | hotfix
- Status: ...
- Priority: ...
- Summary: ...
- Business impact: ...

Problem statement
- ...

Expected vs actual behavior
- Expected: ...
- Actual: ...

Acceptance criteria found
- ...

Missing information / ambiguities
- ...

Design/UI findings if image exists
- ...

Network/log findings if logs exist
- ...

Likely root causes
- Hypothesis 1: ...
- Hypothesis 2: ...

Proposed fix directions
- Direction 1: ...
- Direction 2: ...

Affected areas
- Frontend screens/components: ...
- Backend/API/services: ...
- State/navigation/cache/auth/forms: ...

Risks / tradeoffs
- ...

Questions to confirm before implementation
- ...

Recommendation
- Ready to implement | Not yet ready
- Reason: ...
```

## Writing Rules

- Prefer bullets over long prose.
- Separate facts from assumptions.
- Keep each bullet independently readable.
- Avoid raw log dumps and long copied ticket text.
- Use direct engineering language.
