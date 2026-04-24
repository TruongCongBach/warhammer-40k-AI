# Fix Planning Workflow

## Purpose

Follow this workflow to turn a ticket analysis into a clear implementation plan without writing code.

## Step 1: Confirm the Baseline

Start from:
- Jira issue data
- previous analysis
- acceptance criteria
- supporting screenshots or logs if they materially affect the plan

Restate the problem in engineering terms before proposing solutions.

## Step 2: Define the Planning Constraints

Capture:
- platform or runtime boundaries
- architectural constraints
- data dependencies
- environment assumptions
- backward compatibility concerns
- rollout or urgency considerations

If these constraints are missing, list them before deciding an approach.

## Step 3: Generate One or More Approaches

Propose:
- approach A as the default option
- approach B only when there is a genuine alternative with different tradeoffs

For each approach, describe:
- the main change strategy
- which layer changes first
- how the user-visible behavior improves
- how risk is contained

Keep the language concrete but non-coding.

## Step 4: Map Affected Areas

Identify likely:
- screens or routes
- components
- hooks, stores, reducers, contexts
- service or API layers
- validation, mapping, caching, or feature-flag logic
- platform-specific boundaries

When certainty is low, mark the area as likely rather than confirmed.

## Step 5: Review State and Data Boundaries

Call out:
- state ownership
- transient loading and error states
- retry or refresh flows
- cache invalidation or stale-data concerns
- API contract dependencies
- serialization, validation, or transformation layers

This step is required for both bugs and feature work.

## Step 6: Pressure-Test the Plan

Review:
- regression risk
- migration risk
- edge cases
- platform-specific behavior
- rollout complexity
- observability or debugging impact

Use [risk-tradeoff-template](./risk-tradeoff-template.md) and [edge-case-checklist](./edge-case-checklist.md).

## Step 7: Suggest Tests to Prepare

Plan tests before implementation:
- happy path
- error path
- state transition checks
- boundary conditions
- platform-specific checks
- integration or end-to-end coverage when appropriate

Tie each test suggestion to a likely failure mode or regression risk.

## Step 8: Make the Recommendation

End with:
- `proceed` when the approach is sufficiently constrained and testable
- `needs clarification first` when uncertainty could materially change the implementation strategy

State the smallest missing clarification that would unblock implementation.
