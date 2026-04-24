---
name: ticket-commit
description: Prepare and perform issue-scoped commits for Jira work. This skill should be used after implementation is ready to commit, when the current git changes need to be reviewed conservatively, unrelated files need to be excluded, and only files that are clearly relevant to the current Jira issue should be staged and committed with the standard title format.
progressive_disclosure:
  entry_point:
    summary: "Review changed files, recommend a safe commit scope, and stage or commit only the files that clearly belong to the current Jira issue."
    when_to_use: "Use after coding is complete and before committing, especially when multiple changed files exist and accidental inclusion of unrelated work is a risk."
    quick_start: "1. Read Jira and current diff 2. Separate relevant files from uncertain ones 3. Generate the commit title 4. Stage only recommended files 5. Commit only when the scope is clearly safe"
  references:
    - references/scoped-commit-workflow.md
    - references/scoped-commit-template.md
    - references/scoped-commit-checklist.md
    - references/file-relevance-review-checklist.md
    - references/suspicious-file-warning-checklist.md
    - references/commit-message-format-guide.md
---

# Ticket Commit

## Overview

Use this skill to prepare and optionally perform a clean commit for one Jira issue without pulling in unrelated work. Read Jira ticket context when available, inspect the current git changes, classify files conservatively, generate the standard commit title, and stage only the files that clearly belong to the issue.

Keep the workflow commit-safety focused. Do not push, do not modify ticket status, do not comment on the ticket, and do not include uncertain files automatically.

Always respond in the user's current language. If the user writes in Vietnamese, reply in Vietnamese. If the user writes in English, reply in English. Keep technical terms in their original form when that is clearer.

## When to Use This Skill

Activate when:
- Implementation is done and a clean issue-scoped commit is needed
- Several changed files exist and only some belong to the current Jira issue
- A commit message must follow the standard `type: TICKET-ID | summary` format
- The user wants help deciding what is safe to stage and commit
- Unrelated or suspicious files might have been touched in the same worktree

Do not activate when:
- The implementation is still under active editing
- The correct file scope is still unclear and requires code review first
- The task is to push, open a PR, or update Jira status
- The user wants a broad snapshot commit of all current changes

## The Iron Law

Prefer under-including over over-including. If file relevance is unclear, do not stage it automatically. Put it in `needs review` and stop short of commit if the uncertainty could contaminate the issue scope.

## Core Principles

1. **Issue-scoped safety**: Commit only files that clearly support the current Jira issue.
2. **Conservative selection**: Exclude or flag files when relevance is not obvious.
3. **Explicit staging**: Stage exact paths, never `git add .` or broad directory adds without review.
4. **Commit clarity**: Generate a short, consistent commit title that matches the issue.
5. **No hidden side effects**: Do not push, rebase, amend, or modify ticket systems as part of this workflow.

## Quick Start

1. Read the Jira issue when available and capture ticket ID, issue type, summary, and acceptance criteria.
2. Inspect the current git worktree using `git status --short` and targeted diff inspection.
3. Review file relevance with [file-relevance-review-checklist](./references/file-relevance-review-checklist.md).
4. Review suspicious paths with [suspicious-file-warning-checklist](./references/suspicious-file-warning-checklist.md).
5. Execute `scripts/review_scoped_commit.py --ticket-id ML-39 --summary "fix quote screen layout issue"` to produce a conservative recommendation.
6. Generate the commit title from [commit-message-format-guide](./references/commit-message-format-guide.md) or `scripts/generate_scoped_commit_title.py`.
7. Stage only the recommended files.
8. Commit only when the final recommendation is `safe to commit`.

## Input Priority

Use inputs in this order:
1. Jira ticket context
2. current git changed files and diff
3. approved implementation or review context
4. any explicit user guidance about which files belong to the issue

If ticket scope and changed-file scope do not align, trust the narrower set and flag the rest for review.

## Safety Rules

- Never use `git add .` for this skill.
- Never commit a file whose relevance is uncertain.
- Place uncertain files in `Files excluded or needing review`.
- If uncertain files might materially affect correctness of the issue, recommend `review needed` instead of committing.
- Stage exact paths only.
- Commit only after the recommended file list is stable and explain why each included file belongs.

## Output Contract

Produce the final commit review output in this order:
- Ticket summary
- Changed files detected
- Files recommended for commit
- Files excluded or needing review
- Why these files are included
- Suggested commit title
- Suggested commit summary
- Final recommendation: safe to commit / review needed

## Commit Execution Rules

When the user wants the commit to be performed:
- stage only the selected files
- use the generated standard title
- do not push
- do not amend an older commit unless explicitly requested
- stop if the worktree still contains uncertain files that may belong to the same issue

## Git Workflow Guidance

### Review Phase

Inspect:
- `git status --short`
- per-file diffs for suspicious or mixed-scope changes
- generated files, locks, workspace files, and unrelated docs carefully

### Staging Phase

Stage:
- exact files only
- only the files that clearly belong to the issue

Avoid:
- broad path staging
- project-wide config changes unless the issue clearly required them

### Commit Phase

Commit only when:
- the selected files align with the ticket
- excluded files are safely unrelated or intentionally left out
- the commit title is clear and correctly formatted

## Navigation

- **[Scoped Commit Workflow](./references/scoped-commit-workflow.md)** - Load for the end-to-end sequence from diff review to safe commit.
- **[Scoped Commit Template](./references/scoped-commit-template.md)** - Load for the final review and commit output structure.
- **[Scoped Commit Checklist](./references/scoped-commit-checklist.md)** - Load before staging or committing.
- **[File Relevance Review Checklist](./references/file-relevance-review-checklist.md)** - Load when deciding whether a changed file truly belongs to the issue.
- **[Suspicious File Warning Checklist](./references/suspicious-file-warning-checklist.md)** - Load when config, lockfile, generated, or workspace changes appear.
- **[Commit Message Format Guide](./references/commit-message-format-guide.md)** - Load to generate `type: TICKET-ID | summary`.

## Key Reminders

- Commit narrowly.
- Stage exact files only.
- Prefer under-including when uncertain.
- Flag suspicious files instead of hand-waving them away.
- Keep the commit title short and action-oriented.
- Do not push or update Jira from this skill.

## Red Flags - STOP

Stop and correct course when:
- the plan includes `git add .`
- unrelated files are mixed into the recommended list
- generated or lock files appear without a clear reason
- workspace or editor files appear in the diff
- the commit title does not match `type: TICKET-ID | summary`
- the same issue appears to need files that are currently in `needs review`

## Integration Notes

- Use after `ticket-review` confirms the work is acceptable.
- Use before `ticket-summary` and `ticket-close` when a clean commit should exist first.
- Use explicit skill invocation on machines with many installed skills to avoid overlap with review or summary skills.
