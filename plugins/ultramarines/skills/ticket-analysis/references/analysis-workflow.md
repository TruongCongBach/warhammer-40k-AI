# Ticket Analysis Workflow

## Purpose

Follow this workflow to triage a Jira ticket into an engineering-ready analysis without starting implementation.

## Step 1: Read Jira Before Anything Else

Load the issue from Jira MCP and extract:
- ticket ID
- issue type
- status
- priority
- summary
- description
- acceptance criteria
- components or labels
- recent comments
- attachments or linked artifacts

Capture direct statements separately from inferred meaning.

## Step 2: Normalize the Problem

Convert ticket language into:
- business impact
- expected behavior
- actual behavior
- reproduction clues
- environments mentioned
- affected users or platforms

If the ticket mixes several problems, split them into distinct symptoms before analysis.

## Step 3: Identify Gaps

List missing facts explicitly:
- missing reproduction steps
- missing platform or environment
- missing API details
- missing exact screen or route
- missing acceptance criteria
- missing examples of failing input or output

Do not patch gaps with guessed facts. Keep them as open questions.

## Step 4: Review Visual Evidence

When a screenshot or design image exists:
- identify the visible screen or state
- note layout, copy, spacing, alignment, visibility, loading, empty, and error-state issues
- compare visible evidence against the ticket claim
- state what cannot be known from the image alone

Use [screenshot-review-template](./screenshot-review-template.md) to keep this section disciplined.

## Step 5: Review Traffic and Logs

When HAR, Charles, zip, JSON, text, or log files exist:
- inspect file type first
- unzip archives into a temporary directory when needed
- normalize the content where possible
- summarize failed, slow, repeated, or suspicious calls
- note whether the evidence points to frontend, backend, network, auth, configuration, or data issues

Use `scripts/inspect_ticket_artifacts.py` for a first pass, then refine the interpretation manually.

## Step 6: Form Hypotheses

Build 2-4 plausible root-cause hypotheses. For each hypothesis, note:
- why it fits the evidence
- what evidence weakens it
- which modules or services it would affect
- what check would confirm or disprove it quickly

Use [root-cause-hypothesis-template](./root-cause-hypothesis-template.md).

## Step 7: Propose Fix Directions

Stay at the planning level. For each direction, describe:
- intended correction
- likely code areas or systems involved
- tradeoffs
- risk of regression
- missing confirmation needed before coding

Keep the wording implementation-aware but non-coding.

## Step 8: Decide Readiness

Apply [readiness-checklist](./readiness-checklist.md) and end with one of two decisions:
- `Ready to implement`
- `Not yet ready`

If not ready, state exactly what evidence or clarification is still required.
