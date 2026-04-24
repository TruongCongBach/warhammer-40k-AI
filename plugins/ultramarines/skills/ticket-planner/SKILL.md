---
name: ticket-planner
description: Create implementation plans after ticket analysis but before coding. This skill should be used when a Jira ticket, prior analysis, screenshots, design images, HAR or Charles logs, or zipped artifacts need to be turned into one or more concrete fix or feature approaches, with affected areas, risks, edge cases, and test planning, while explicitly stopping short of implementation.
progressive_disclosure:
  entry_point:
    summary: "Turn ticket analysis into concrete implementation approaches, affected areas, security mitigations, and test preparation without writing code."
    when_to_use: "Use after triage or investigation is complete enough to compare fix directions, estimate impact, include security-sensitive constraints, and decide whether implementation should proceed."
    quick_start: "1. Load ticket and prior analysis 2. Confirm the problem and constraints 3. Propose approach A and B if relevant 4. Map affected modules and dependencies 5. List risks, security mitigations, edge cases, and tests 6. End with proceed, needs clarification, or needs security review"
  references:
    - references/planning-workflow.md
    - references/fix-planning-template.md
    - references/risk-tradeoff-template.md
    - references/react-native-planning-checklist.md
    - references/nextjs-planning-checklist.md
    - references/edge-case-checklist.md
    - references/title-format-guide.md
    - ../../docs/security/security-risk-checklist.md
    - ../../docs/security/react-native-security-checklist.md
    - ../../docs/security/nextjs-security-checklist.md
    - ../../docs/security/security-severity-guide.md
    - ../../docs/design/design-extraction-setup.md
    - ../../docs/design/design-context-template.md
---

# Ticket Planner

## Overview

Use this skill to convert ticket analysis into a practical implementation plan before coding starts. Read Jira data through MCP when available, accept a previous analysis as the main input, use screenshots or logs as supporting evidence, and produce one or more concrete approaches with risks, affected areas, suggested tests, and security mitigations when the work touches sensitive surfaces.

Keep the workflow planning-only. Recommend how the work should likely be implemented, but do not write code, patch files, or present implementation snippets unless a later prompt explicitly requests it.

Always respond in the user's current language. If the user writes in Vietnamese, reply in Vietnamese. If the user writes in English, reply in English. Keep technical terms in their original form when that is clearer.

## When to Use This Skill

Activate when:
- A ticket analysis already exists and the next step is choosing an implementation direction
- A bug needs one or more fix approaches before coding begins
- A feature task needs one or more delivery approaches before coding begins
- A team needs likely affected modules, files, or areas called out in advance
- Risks, tradeoffs, state boundaries, and API dependencies need to be clarified first
- A test-preparation plan is needed before implementation starts

Do not activate when:
- The task is still at raw triage and the underlying problem is not yet understood
- The user has already approved an approach and wants code now
- The request is only to summarize the ticket with no planning detail

## The Iron Law

Plan from evidence, not intuition. Use the ticket and prior analysis as the baseline, use images and logs only as supporting context, and stop at recommended approaches and validation planning unless implementation is explicitly requested later.

## Core Principles

1. **Analysis-first planning**: Start from confirmed problem framing, not from preferred solutions.
2. **Concrete but non-coding**: Name likely modules, data boundaries, and state changes without writing code.
3. **Option-aware decision making**: Provide approach A and approach B when the tradeoff is real.
4. **Risk-led scope control**: Surface regressions, migration costs, edge cases, and dependencies early.
5. **Test preparedness**: End with suggested tests that should exist before or alongside implementation.
6. **Security-aware planning**: When the work touches auth, permissions, tokens, storage, validation, uploads, logging, or trust boundaries, call out mitigations before coding starts.

## Quick Start

1. Read the Jira issue via MCP when available and capture ticket ID, issue type, summary, status, priority, and constraints.
2. Accept previous ticket analysis as the main problem definition.
3. Re-check screenshots, design images, logs, or artifacts only as supporting evidence when they materially affect the plan.
   When screenshot detail matters, execute `python3 ../../scripts/extract_design_context.py path/to/image.png --include-raw` and use the resulting Markdown note rather than ad-hoc OCR text.
4. Restate the problem to solve in one concise engineering paragraph or bullet set.
5. Propose approach A and approach B when the alternatives are meaningfully different.
6. Map likely affected modules, files, or areas, including state handling and API/data dependencies.
7. Assess security-sensitive boundaries with [security-risk-checklist](../../docs/security/security-risk-checklist.md) and the framework-specific checklist when relevant.
8. List risks, security mitigations, tradeoffs, edge cases, and suggested tests to prepare.
9. End with `proceed`, `needs clarification first`, or `needs security review`.
10. Generate the standard title string from [title-format-guide](./references/title-format-guide.md) or `scripts/generate_plan_title.py`.

## Input Priority

Use inputs in this order:
1. Jira ticket and acceptance criteria
2. Existing analysis from the prior step
3. Comments and clarifications from stakeholders
4. Screenshots or design images
5. HAR, Charles, zip, JSON, or text logs

If supporting artifacts contradict the prior analysis, call out the contradiction before proposing approaches.

## Planning Rules

- Treat prior analysis as the starting point, not as a guaranteed truth.
- Distinguish clearly between confirmed constraints and planning assumptions.
- Prefer one recommended approach, but include an alternative when the decision is not obvious.
- Keep file and module references likely, not absolute, unless confirmed by the codebase or ticket context.
- Prefer parser-normalized design context over free-form screenshot interpretation when choosing a UI implementation approach.
- For React Native work, think through navigation, async state, platform-specific behavior, gesture and keyboard interactions, offline and retry behavior, and native-module boundaries when relevant.
- For Next.js work, think through server/client boundaries, routing, caching, revalidation, auth, loading and error states, SEO, and deployment environment behavior when relevant.
- Explicitly plan around auth, permissions, role checks, token handling, secure storage, PII exposure, analytics or log leakage, input validation, upload paths, deep links, WebViews, and trusted vs untrusted data boundaries when relevant.
- If the approach depends on a sensitive assumption that is not confirmed, flag `needs security review` instead of pretending the plan is safe.
- Use screenshots or logs to shape the plan, not to overstate certainty.
- Keep the output short enough to approve quickly, but specific enough that an engineer can start implementation from the plan.

## Output Contract

Produce the final planning output in this order:
- Ticket summary
- Problem to solve
- Proposed approach A
- Proposed approach B if relevant
- Why this approach is recommended
- Likely affected modules / files / areas
- State handling to consider
- API/data dependencies
- Security risks / mitigations
- Risks / tradeoffs
- Edge cases
- Suggested tests to prepare
- Recommendation: proceed / needs clarification first / needs security review

Also include:
- Suggested title
- Suggested implementation summary title

## Approach Guidance

### For Bug Fixes

Prefer approaches that:
- minimize regression surface
- preserve intended behavior outside the reported failure
- reduce ambiguity in state transitions or data handling
- can be validated with a narrow, explicit test set

### For Features

Prefer approaches that:
- fit the current architecture
- limit future rework
- define clear ownership across UI, state, and API boundaries
- keep acceptance criteria traceable to planned changes

## Affected Areas Guidance

When naming likely affected modules or files, describe:
- screen or route entry points
- shared components
- hooks, stores, reducers, context, or service layers
- API clients, request builders, mappers, validators, or serializers
- configuration, feature flags, environment-specific paths, or caching layers

Keep the wording probabilistic when certainty is limited.

## Navigation

- **[Planning Workflow](./references/planning-workflow.md)** - Load for the full sequence from analysis input to final recommendation.
- **[Fix Planning Template](./references/fix-planning-template.md)** - Load for the main output structure.
- **[Risk / Tradeoff Template](./references/risk-tradeoff-template.md)** - Load when several options or regressions need comparison.
- **[React Native Planning Checklist](./references/react-native-planning-checklist.md)** - Load for RN-specific state, navigation, platform, and native-boundary planning.
- **[Next.js Planning Checklist](./references/nextjs-planning-checklist.md)** - Load for Next.js-specific routing, server/client, caching, and deployment planning.
- **[Edge Case Checklist](./references/edge-case-checklist.md)** - Load to challenge the proposed approach before implementation.
- **[Title Format Guide](./references/title-format-guide.md)** - Load to generate `type: TICKET-ID | summary`.
- **[Security Risk Checklist](../../docs/security/security-risk-checklist.md)** - Load when the ticket touches auth, data, storage, logging, uploads, or trust boundaries.
- **[React Native Security Checklist](../../docs/security/react-native-security-checklist.md)** - Load for RN-specific storage, deep link, WebView, and device-surface planning.
- **[Next.js Security Checklist](../../docs/security/nextjs-security-checklist.md)** - Load for Next.js-specific auth, server/client, exposure, and caching planning.
- **[Security Severity Guide](../../docs/security/security-severity-guide.md)** - Load to describe security impact and mitigation urgency consistently.
- **[Design Extraction Setup](../../docs/design/design-extraction-setup.md)** - Load when screenshots or design images need to be converted into structured Markdown before planning.
- **[Design Context Template](../../docs/design/design-context-template.md)** - Load when you need a normalized design note to reason about layout, text, and interaction clues.

## Key Reminders

- Plan only. Do not code.
- Use prior analysis as input, not as unquestioned truth.
- Keep recommendations evidence-based and practical.
- Prefer concise bullet points over long essays.
- State assumptions explicitly when artifacts are incomplete.
- Include a second approach only when it adds real decision value.
- Always end with `proceed`, `needs clarification first`, or `needs security review`.
- Always include the Jira ticket ID in the suggested title when available.

## Red Flags - STOP

Stop and correct course when:
- Starting to describe code-level implementation details or snippets
- Presenting only one approach when tradeoffs are clearly unresolved
- Listing affected files with false certainty
- Ignoring state handling or API dependencies for UI-heavy tickets
- Ignoring a material auth, permission, token, storage, logging, upload, validation, deep-link, WebView, or server/client boundary risk
- Ignoring screenshots or logs that materially change the plan
- Recommending `proceed` even though the required constraints are still ambiguous
- Forgetting the suggested tests section
- Generating a title that does not match `type: TICKET-ID | summary`

## Integration Notes

- Use with Jira MCP to refresh ticket facts when needed.
- Pair naturally with `ticket-analysis` as the preceding step.
- Use image or artifact inspection tools only to support planning decisions.
- Hand off to implementation-oriented skills only after the user approves the plan.
