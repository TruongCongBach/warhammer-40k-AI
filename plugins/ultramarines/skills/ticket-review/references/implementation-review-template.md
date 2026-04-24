# Implementation Review Template

## Purpose

Use this template for the final review result. Keep it concise, practical, and ready to hand back to the implementing engineer.

## Template

```markdown
Suggested title
- type: TICKET-ID | short summary

Suggested correction summary title
- type: TICKET-ID | short summary

Suggested follow-up implementation summary title
- type: TICKET-ID | short summary

Ticket summary
- Ticket: TICKET-ID
- Type: bug | feature | chore | refactor | hotfix
- Summary: ...
- Acceptance criteria found: ...

What appears correctly implemented
- ...

What appears incomplete
- ...

Mismatches with ticket/design
- ...

Missing states
- Loading: ...
- Error: ...
- Empty: ...
- Disabled: ...
- Transitional or retry states: ...

UX risks
- ...

Code quality concerns
- ...

Test coverage gaps
- ...

Required changes
- ...

Suggested correction order
- 1. ...
- 2. ...
- 3. ...

Final QA checklist
- ...

Recommendation
- Ready | Needs revision
- Reason: ...
```

## Writing Rules

- Prefer high-signal findings over exhaustive commentary.
- Separate likely issues from confirmed issues when certainty is limited.
- Avoid code dumps.
- Keep required changes specific enough to act on.
