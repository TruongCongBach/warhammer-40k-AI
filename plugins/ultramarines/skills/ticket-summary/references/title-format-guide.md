# Title Format Guide

## Purpose

Generate short, standard titles for ticket history, commit summaries, and QA handoff.

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

## Good Examples

- `fix: ML-39 | implement UI for quotes`
- `fix: ML-39 | correct quote screen layout and empty state`
- `feat: ML-52 | add search filter to order history`

## Output Section

```markdown
Suggested title
- fix: ML-39 | correct quote screen layout and empty state

Suggested commit title
- fix: ML-39 | correct quote screen layout and empty state

Suggested summary title
- fix: ML-39 | correct quote screen layout and empty state

Suggested QA handoff title
- fix: ML-39 | correct quote screen layout and empty state
```

## Script Usage

Run:

```bash
python3 scripts/generate_change_title.py --ticket-id ML-39 --issue-type bug --summary "correct quote screen layout and empty state"
```
