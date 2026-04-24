# Implementation Review Workflow

## Purpose

Follow this workflow to review a completed implementation against Jira, design intent, UX expectations, and engineering quality standards.

## Step 1: Re-anchor on the Ticket

Read:
- ticket summary
- description
- acceptance criteria
- comments or clarifications
- linked evidence such as screenshots or logs

Convert the ticket into a short list of required observable outcomes before judging the code.

## Step 2: Inspect the Actual Implementation

Review:
- changed files
- relevant modules and components
- nearby tests
- runtime-specific boundaries such as navigation, data fetching, caching, or auth

Focus on what was changed and what should have changed but appears untouched.

## Step 3: Compare Requirement Coverage

Check:
- what appears correctly implemented
- what appears incomplete
- what appears out of scope or inconsistent with the ticket
- whether acceptance criteria map to actual behavior paths in the code

If certainty is limited, state that explicitly.

## Step 4: Review UI and UX Risk

When the ticket affects user-facing behavior, check:
- state coverage
- disabled paths
- feedback loops after actions
- consistency with screenshots or design references
- likely confusion, friction, or dead-end states

Use [ui-state-coverage-checklist](./ui-state-coverage-checklist.md) to keep this review systematic.

## Step 5: Review Structure and Maintainability

Check for:
- duplicated UI logic
- hardcoded values that should be tokens or shared constants
- weak separation between state, data transformation, and rendering
- difficult-to-extend conditional logic
- brittle coupling between components and services

Only surface maintainability concerns that are likely to matter for this delivery.

## Step 6: Review Test Coverage

Check:
- whether tests cover the intended behavior
- whether risky branches are untested
- whether tests match the new state transitions
- whether manual QA still carries too much risk because test coverage is weak

Use [test-coverage-checklist](./test-coverage-checklist.md).

## Step 7: Convert Findings into Corrections

Produce:
- required changes
- suggested correction order
- a final QA checklist

Prefer a correction order that reduces retesting churn:
1. requirement or behavior gaps
2. missing states or UX blockers
3. structural cleanup needed for correctness or maintainability
4. test gaps

## Step 8: Make the Recommendation

End with:
- `ready` when requirement match and review confidence are sufficient
- `needs revision` when significant gaps, risks, or uncertainties remain

State the minimum set of corrections required to move the implementation to ready.
