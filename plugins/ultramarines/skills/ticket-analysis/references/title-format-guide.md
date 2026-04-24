# Title Format Guide

## Purpose

Generate a short, standard ticket-related title for commit messages, ticket comments, and implementation summaries.

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
- Avoid filler words and long explanations.

## Good Examples

- `fix: ML-39 | implement UI for quotes`
- `feat: ML-52 | add search filter to order history`
- `chore: ML-61 | refactor address form validation`
- `refactor: ML-77 | simplify checkout state handling`
- `fix: APP-214 | fix validation for phone input`

## Suggested Output Section

```markdown
Suggested title
- fix: ML-39 | implement UI for quotes

Suggested commit message
- fix: ML-39 | implement UI for quotes

Suggested ticket comment title
- fix: ML-39 | implement UI for quotes
```

## Script Usage

Run:

```bash
python3 scripts/generate_ticket_title.py --ticket-id ML-39 --issue-type bug --summary "implement UI for quotes"
```
