# Scoped Commit Workflow

## Purpose

Follow this workflow to create a conservative, issue-scoped commit from the current worktree.

## Step 1: Re-anchor on the Jira Issue

Read:
- ticket ID
- issue type
- summary
- acceptance criteria
- approved implementation or review context

Use this to define what kinds of files should reasonably belong to the issue.

## Step 2: Inspect the Current Worktree

Collect:
- `git status --short`
- unstaged file list
- staged file list if any
- untracked file list
- targeted per-file diffs when scope is ambiguous

Do not jump to staging yet.

## Step 3: Review File Relevance

For each changed file, ask:
- does this file support the ticket behavior directly?
- does the diff align with the issue summary?
- is this file a side effect of local work, tooling, or another issue?

Use [file-relevance-review-checklist](./file-relevance-review-checklist.md).

## Step 4: Review Suspicious Paths

Treat these with extra caution:
- lockfiles
- package manifests
- generated files
- IDE files
- broad config changes
- docs unrelated to the issue
- snapshots or build artifacts

Use [suspicious-file-warning-checklist](./suspicious-file-warning-checklist.md).

## Step 5: Classify the Files

Split changed files into:
- recommended for commit
- excluded or needing review

When uncertain, place the file in `needs review`.

## Step 6: Generate the Commit Title

Generate:
- `type: TICKET-ID | summary`

Use the Jira ticket to infer the type where possible.

## Step 7: Stage Conservatively

Stage only:
- exact recommended paths

Never use:
- `git add .`
- broad directory staging without explicit review

## Step 8: Commit Only If Safe

Commit only when:
- the selected files clearly match the issue
- excluded files are intentionally left out
- no unresolved uncertainty could contaminate the commit

If uncertainty remains, stop with `review needed`.
