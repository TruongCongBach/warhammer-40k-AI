# Manual QA Checklist Template

## Purpose

Use this template to prepare a final manual QA pass after corrections are applied.

## Template

```markdown
Final QA checklist
- Confirm the primary ticket flow works end to end.
- Confirm acceptance criteria are each observable in the implementation.
- Confirm loading, error, empty, and disabled states behave as expected.
- Confirm the main CTA or user action cannot be triggered into an invalid state.
- Confirm navigation or route return paths behave correctly.
- Confirm platform-specific behavior on the relevant target surfaces.
- Confirm no obvious visual regression against the screenshot or design reference.
- Confirm analytics, tracking, or side effects still behave if relevant.
- Confirm updated tests pass and cover the intended change.
```

## Usage Note

Trim or expand the checklist based on the ticket scope, but keep it focused on what could realistically block delivery quality.
