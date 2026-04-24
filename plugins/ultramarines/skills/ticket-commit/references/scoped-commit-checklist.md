# Scoped Commit Checklist

## Purpose

Use this checklist before staging or committing.

## Checklist

- Jira ticket ID and summary are known.
- The current issue scope is understood.
- All changed files have been reviewed.
- Recommended files clearly support the issue.
- Unrelated or suspicious files are excluded.
- No `git add .` or broad staging is used.
- The commit title matches `type: TICKET-ID | summary`.
- The commit is safe even if excluded files remain in the worktree.

## Decision Rule

If any changed file might belong to the issue but is still unclear, do not commit automatically. Mark the result as `review needed`.
