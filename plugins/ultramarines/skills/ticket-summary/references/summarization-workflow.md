# Change Summarization Workflow

## Purpose

Follow this workflow to turn completed implementation context into a clear, durable handoff summary.

## Step 1: Anchor on the Ticket

Read:
- ticket summary
- issue type
- acceptance criteria
- comments that clarify intent

Use this to define what the change was supposed to achieve.

## Step 2: Gather Implementation Context

Read:
- implementation summary
- diff summary
- review findings
- correction summary if the implementation went through revisions

Prefer synthesized context over raw diffs when available.

## Step 3: State the Root Cause

Describe:
- what was broken or missing
- why it happened
- whether the cause is confirmed or inferred

Keep this statement short and technical.

## Step 4: State the Fix Approach

Describe:
- what strategy was used to correct the issue or deliver the feature
- how the change addresses the cause or requirement gap

Avoid line-by-line code narration.

## Step 5: Summarize What Changed

Capture:
- user-visible behavior changes
- key structural or state-management changes
- API or data-handling changes if relevant
- affected modules, screens, routes, or flows

This section should help readers understand scope fast.

## Step 6: Summarize Risk and Validation

Call out:
- likely regression areas
- QA focus areas
- concrete test scenarios

The summary should help QA know where to spend time first.

## Step 7: Produce Short Handoff Variants

Generate:
- short ticket history summary
- short engineering-reader summary
- title strings for commit, summary, and QA handoff

Keep these variants compact but still meaningful.
