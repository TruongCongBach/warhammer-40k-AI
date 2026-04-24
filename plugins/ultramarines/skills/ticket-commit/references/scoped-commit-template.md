# Scoped Commit Template

## Purpose

Use this template for the final scoped-commit decision and commit preparation output.

## Template

```markdown
Ticket summary
- Ticket: TICKET-ID
- Type: bug | feature | chore | refactor | hotfix
- Summary: ...

Changed files detected
- ...

Files recommended for commit
- ...

Files excluded or needing review
- ...

Why these files are included
- ...

Suggested commit title
- type: TICKET-ID | short summary

Suggested commit summary
- Commit only the recommended files listed above.

Final recommendation
- Safe to commit | Review needed
- Reason: ...
```

## Rules

- Keep the file lists explicit.
- Explain the inclusion logic in plain engineering terms.
- If any file is uncertain, say so directly.
