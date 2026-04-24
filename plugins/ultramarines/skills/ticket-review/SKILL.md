---
name: ticket-review
description: Review completed implementations against Jira requirements, acceptance criteria, screenshot or design-image references, UX expectations, and engineering quality standards. This skill should be used after code has been written and before finalizing the work, when practical review findings, correction guidance, state coverage checks, and test gap detection are needed without automatically committing changes or closing the ticket.
progressive_disclosure:
  entry_point:
    summary: "Review implementation quality, requirement coverage, and security-sensitive behavior after coding, then produce actionable correction guidance and a readiness recommendation."
    when_to_use: "Use after implementation exists and needs validation against Jira, design references, UX expectations, security-sensitive constraints, and engineering quality before final approval."
    quick_start: "1. Read Jira and scope 2. Inspect the implementation 3. Compare against ticket and screenshots 4. Check state, UX, structure, security, and tests 5. List required changes and QA checks 6. End with ready or needs revision"
  references:
    - references/review-workflow.md
    - references/implementation-review-template.md
    - references/react-native-review-checklist.md
    - references/nextjs-review-checklist.md
    - references/ui-state-coverage-checklist.md
    - references/test-coverage-checklist.md
    - references/manual-qa-checklist-template.md
    - references/title-format-guide.md
    - ../../docs/security/security-risk-checklist.md
    - ../../docs/security/react-native-security-checklist.md
    - ../../docs/security/nextjs-security-checklist.md
    - ../../docs/security/security-severity-guide.md
    - ../../docs/design/design-extraction-setup.md
    - ../../docs/design/design-context-template.md
---

# Ticket Review

## Overview

Use this skill to review a completed implementation before finalizing the work. Read Jira ticket data through MCP when available, compare the implementation against the ticket, acceptance criteria, and screenshot or design-image references when provided, and produce practical correction guidance focused on real delivery quality. Treat security-sensitive behavior as part of delivery quality, especially for auth, permissions, tokens, storage, logging, uploads, deep links, WebViews, and trusted-data boundaries.

Keep the workflow review-oriented. Identify what appears correct, what is incomplete, what likely mismatches the ticket or UX intent, what states or tests are missing, and what should be corrected next. Do not automatically commit changes or close the ticket.

Always respond in the user's current language. If the user writes in Vietnamese, reply in Vietnamese. If the user writes in English, reply in English. Keep technical terms in their original form when that is clearer.

## When to Use This Skill

Activate when:
- Code has already been written and needs review against a Jira ticket
- Acceptance criteria need to be checked against the current implementation
- A screenshot or design image needs to be used as a visual reference for review
- UI/UX quality, state coverage, and test coverage need to be assessed before finalizing
- A reviewer needs actionable correction guidance rather than only raw findings
- A final recommendation is needed on whether the work is ready or still needs revision

Do not activate when:
- The problem is still at ticket triage or planning stage
- No implementation exists yet
- The user wants coding changes immediately rather than a review first
- The task is only to summarize the ticket without checking the code

## The Iron Law

Review the implementation against evidence. Use Jira and acceptance criteria as the source of truth, use screenshots and logs as supporting references, and do not claim visual or behavioral certainty that cannot be verified from code and available artifacts.

## Core Principles

1. **Requirement-first review**: Start from the ticket and acceptance criteria before judging code structure.
2. **Delivery-focused findings**: Prioritize issues that materially affect behavior, UX, maintainability, or release confidence.
3. **State-aware review**: Check loading, error, empty, disabled, retry, and transitional states, not just the happy path.
4. **Actionable correction guidance**: Convert findings into a practical list of required changes and a correction order.
5. **Evidence and assumptions separated**: Distinguish what is observed in code from what is inferred from screenshots or likely runtime behavior.
6. **Security-aware review**: Treat sensitive data exposure, missing authorization checks, unsafe storage, and trust-boundary mistakes as first-class findings.

## Quick Start

1. Read the Jira issue via MCP when available and extract ticket ID, issue type, summary, description, comments, and acceptance criteria.
2. Inspect the implementation diff or changed files that correspond to the ticket.
3. Compare the code against the ticket requirements and acceptance criteria.
4. Review screenshots or design images when present, but treat them as supporting references rather than exact spec documents.
   When the image is important to requirement or UX verification, execute `python3 ../../scripts/extract_design_context.py path/to/image.png --include-raw` and compare the normalized note with the implementation.
5. Check UI state coverage, UX risks, security-sensitive behavior, code quality, and test coverage using the reference checklists.
6. Use [security-risk-checklist](../../docs/security/security-risk-checklist.md) and the framework-specific checklist when the ticket touches sensitive flows.
7. Produce the final review using [implementation-review-template](./references/implementation-review-template.md).
8. End with `ready` or `needs revision`.
9. Generate the standard title string from [title-format-guide](./references/title-format-guide.md) or `scripts/generate_review_title.py`.

## Input Priority

Use inputs in this order:
1. Jira ticket and acceptance criteria
2. Changed code and implementation diff
3. Existing planning or analysis context
4. Screenshots or design images
5. HAR, Charles, zip, JSON, or text logs if they help explain runtime behavior

If the implementation contradicts the ticket, prioritize the contradiction over stylistic review details.

## Review Rules

- Focus on findings that affect correctness, UX, maintainability, or test confidence.
- Do not pretend code alone proves pixel-perfect UI quality.
- State assumptions explicitly when screenshots are the only design reference.
- Prefer parser-normalized design context over ad-hoc OCR when a screenshot is central to the review.
- Call out likely missing runtime states even if the happy path exists.
- Prefer concise findings with practical impact over exhaustive commentary.
- For React Native work, pay attention to navigation behavior, async state, device variations, keyboard and gesture flows, and platform-specific UX.
- For Next.js work, pay attention to route behavior, server/client boundaries, auth, loading and error states, cache or revalidation implications, and runtime environment assumptions.
- Explicitly review auth and permission checks, token or secret handling, secure storage use, PII exposure, analytics or log leakage, input validation, upload or file handling, deep links, WebViews, and trusted vs untrusted data boundaries when relevant.
- If a material security-sensitive path is unclear, state the assumption and keep the recommendation conservative.
- Treat duplicated UI logic, hardcoded styles or tokens, and brittle component structure as review findings when they materially raise delivery risk.
- Treat missing tests as part of implementation incompleteness, not as an optional afterthought.

## Output Contract

Produce the final review output in this order:
- Ticket summary
- What appears correctly implemented
- What appears incomplete
- Mismatches with ticket/design
- Missing states
- UX risks
- Code quality concerns
- Security findings
- Test coverage gaps
- Required changes
- Suggested correction order
- Final QA checklist
- Recommendation: ready / needs revision

Also include:
- Suggested title
- Suggested correction summary title
- Suggested follow-up implementation summary title

## Review Focus Areas

### Requirement Match

Check whether:
- the user-visible behavior appears to satisfy the ticket
- acceptance criteria are fully covered
- the implementation scope drifted beyond or fell short of the requested change

### UI and UX

Check whether:
- states are represented clearly
- interactions are coherent and reversible
- copy, spacing, visual hierarchy, and disabled behavior appear intentional
- likely UX regressions exist even if the code compiles

### Structure and Maintainability

Check whether:
- logic is duplicated unnecessarily
- styles or tokens are hardcoded in brittle ways
- components carry too many responsibilities
- state, transformation, and rendering concerns are poorly separated

### Test Readiness

Check whether:
- critical behavior is covered by unit, integration, or end-to-end tests where appropriate
- regression-prone branches are untested
- the test set reflects likely failure modes

## Navigation

- **[Review Workflow](./references/review-workflow.md)** - Load for the end-to-end review sequence and prioritization logic.
- **[Implementation Review Template](./references/implementation-review-template.md)** - Load for the main output structure.
- **[React Native Review Checklist](./references/react-native-review-checklist.md)** - Load for RN-specific UX, state, navigation, and platform review.
- **[Next.js Review Checklist](./references/nextjs-review-checklist.md)** - Load for Next.js-specific route, rendering, caching, and auth review.
- **[UI State Coverage Checklist](./references/ui-state-coverage-checklist.md)** - Load to verify loading, error, empty, disabled, and transitional states.
- **[Test Coverage Checklist](./references/test-coverage-checklist.md)** - Load to assess the quality and sufficiency of tests.
- **[Manual QA Checklist Template](./references/manual-qa-checklist-template.md)** - Load to prepare final QA steps before approval.
- **[Title Format Guide](./references/title-format-guide.md)** - Load to generate `type: TICKET-ID | summary`.
- **[Security Risk Checklist](../../docs/security/security-risk-checklist.md)** - Load when the implementation touches auth, data, storage, logging, uploads, or trust boundaries.
- **[React Native Security Checklist](../../docs/security/react-native-security-checklist.md)** - Load for RN-specific storage, deep link, WebView, and device-surface review.
- **[Next.js Security Checklist](../../docs/security/nextjs-security-checklist.md)** - Load for Next.js-specific auth, server/client, exposure, and caching review.
- **[Security Severity Guide](../../docs/security/security-severity-guide.md)** - Load to describe the severity of security findings consistently.
- **[Design Extraction Setup](../../docs/design/design-extraction-setup.md)** - Load when screenshots or design images need to be converted into structured Markdown before review.
- **[Design Context Template](../../docs/design/design-context-template.md)** - Load when you need a normalized design note to compare visible UI evidence with the implementation.

## Key Reminders

- Review first. Do not auto-commit or auto-close the ticket.
- Treat Jira and acceptance criteria as the baseline.
- Separate observed findings from assumptions.
- Prioritize issues that matter for shipping quality.
- Include correction guidance, not just criticism.
- Treat security-sensitive regressions as shipping blockers when they are material.
- Keep the final recommendation explicit.
- Always include the Jira ticket ID in the suggested title when available.

## Red Flags - STOP

Stop and correct course when:
- Claiming visual perfection from code alone
- Ignoring acceptance criteria because the code looks clean
- Omitting missing states or UX risks from a UI-heavy ticket
- Ignoring a material auth, permission, token, storage, logging, upload, validation, deep-link, WebView, or trust-boundary issue
- Focusing on low-value nitpicks while larger requirement gaps remain
- Treating missing tests as acceptable on risky behavior changes
- Forgetting to propose required changes and a correction order
- Generating a title that does not match `type: TICKET-ID | summary`

## Integration Notes

- Use with Jira MCP to refresh ticket facts during review.
- Pair naturally with `ticket-analysis` and `ticket-planner` as earlier phases.
- Use image review only as a supportive reference when design tooling is not available.
- Hand off corrections to implementation work only after the user approves the review findings.
