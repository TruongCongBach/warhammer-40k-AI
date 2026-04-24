# Ticket Closure Workflow

## Purpose

Follow this workflow to turn approved implementation context into a clean final Jira closure record.

## Step 1: Re-anchor on the Ticket

Read:
- ticket summary
- issue type
- acceptance criteria
- any important ticket comments

Use this to keep the final closure note aligned with what the ticket was meant to resolve.

## Step 2: Read the Approved Change Summary

Gather:
- what was fixed or delivered
- what behavior changed
- any review-approved notes
- any QA focus already identified

Prefer synthesized change summaries over raw diffs.

## Step 3: Extract the Closure Essentials

Capture:
- what was fixed
- what QA should verify
- any risks or notes worth preserving
- whether a short release-note-style sentence would help

Keep this extraction concise.

## Step 4: Draft the Final Comment

Use [final-ticket-comment-template](./final-ticket-comment-template.md) to create a comment that:
- explains the result clearly
- remains easy to scan
- gives QA enough direction without becoming long-winded

## Step 5: Draft the QA Handoff

Use [qa-handoff-template](./qa-handoff-template.md) to call out:
- primary validation flow
- risky states or scenarios
- any platform or environment specifics

## Step 6: Add the Short Closure Variants

Produce:
- short closure summary
- concise status update
- optional release-note-style summary when relevant

These variants should help future readers understand the ticket outcome quickly.
