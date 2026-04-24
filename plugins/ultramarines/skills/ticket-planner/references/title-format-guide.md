# Title Format Guide

## Purpose

Generate a short, standard planning title for implementation summaries and related planning outputs.

## Required Format

Use this exact format:

```text
type: TICKET-ID | short summary
```

## Type Inference Rules

- `bug` -> `fix`
- `new feature` -> `feat`
- `maintenance` or `internal cleanup` -> `chore`
- `code structure improvement without behavior change` -> `refactor`
- `urgent production bug` -> `hotfix`

When uncertain:
- prefer `fix` for bug tickets
- prefer `feat` for feature tickets

## Title Rules

- Always include the Jira ticket ID when available.
- Always include the pipe separator.
- Keep the summary concise and action-oriented.
- Prefer lowercase unless proper nouns require uppercase.

## Good Examples

- `fix: ML-39 | fix quote screen layout issue`
- `feat: ML-52 | add search filter to order history`
- `refactor: ML-77 | simplify checkout state handling`

## Output Section

```markdown
Suggested title
- fix: ML-39 | fix quote screen layout issue

Suggested implementation summary title
- fix: ML-39 | fix quote screen layout issue
```

## Script Usage

Run:

```bash
python3 scripts/generate_plan_title.py --ticket-id ML-39 --issue-type bug --summary "fix quote screen layout issue"
```
