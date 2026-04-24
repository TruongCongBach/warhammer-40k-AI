---
name: ticket-summary
description: Summarize completed fixes or features for engineering handoff, QA context, and future readers before final ticket closure messaging. This skill should be used after implementation and review context exist, when a concise but complete explanation of root cause, fix approach, changed areas, regression risks, and validation focus is needed without writing or modifying code.
progressive_disclosure:
  entry_point:
    summary: "Turn completed implementation context into clear handoff summaries for ticket history, QA, and engineering readers, including security notes when relevant."
    when_to_use: "Use after a fix or feature is implemented and stable enough to explain the change clearly for engineers and QA, but before or alongside the final Jira closure note."
    quick_start: "1. Read ticket and implementation context 2. Identify root cause and fix approach 3. Summarize changed areas, risks, and security note if relevant 4. Add QA focus and test scenarios 5. Produce short handoff summaries and titles"
  references:
    - references/summarization-workflow.md
    - references/change-summary-template.md
    - references/root-cause-template.md
    - references/qa-handoff-template.md
    - references/regression-risk-template.md
    - references/short-ticket-history-template.md
    - references/title-format-guide.md
    - ../../docs/security/security-risk-checklist.md
    - ../../docs/security/security-severity-guide.md
---

# Ticket Summary

## Overview

Use this skill to explain a completed fix or feature in a way that engineers and QA can understand quickly. Read Jira ticket context when available, read implementation, diff, or review summaries, then produce a structured handoff that explains the root cause, fix approach, changed areas, regression risks, QA focus, and any security note that future readers should not miss.

Keep the workflow summarization-only. Do not implement code, rewrite the patch, or turn the summary into a commit workflow.

Always respond in the user's current language. If the user writes in Vietnamese, reply in Vietnamese. If the user writes in English, reply in English. Keep technical terms in their original form when that is clearer.

## When to Use This Skill

Activate when:
- A completed ticket needs an engineering-facing summary before or alongside final closure
- QA needs validation notes and focus areas tied to the completed change
- Review context needs to be condensed for future engineers
- A root cause and fix need to be explained clearly after implementation
- A concise engineering handoff is needed without exposing the whole diff

Do not activate when:
- The work is still in planning or review and not yet stable enough to summarize
- No implementation context exists yet
- The task is to write code or adjust the implementation
- The main goal is only to draft the final Jira closure comment
- The user only wants a raw changelog dump

## The Iron Law

Explain cause, change, and impact. Use Jira and implementation context to tell the reader what happened, why it happened, what was changed, and what still deserves validation. Avoid vague statements such as "fixed issue" without technical substance.

## Core Principles

1. **Human-readable engineering context**: Summaries should help QA and engineers understand the change fast.
2. **Cause before change**: Explain the root cause before describing the fix.
3. **Impact-oriented wording**: Show which areas changed and where regressions could appear.
4. **QA-ready output**: Include validation focus and concrete test scenarios, not only engineering prose.
5. **Concise completeness**: Keep the summary tight, but not so compressed that the reader loses the why.
6. **Security-aware handoff**: If the change affects auth, permissions, tokens, storage, logging, uploads, or trust boundaries, preserve that context in the handoff.

## Quick Start

1. Read the Jira issue when available and extract ticket ID, summary, issue type, and acceptance criteria.
2. Read implementation context such as diff summary, review findings, correction summary, or implementation summary.
3. Identify the root cause in one clear statement.
4. Identify the fix approach in one clear statement.
5. Summarize what changed and which areas were affected.
6. Call out regression risks, QA focus areas, and a security note if relevant.
7. Produce short ticket history and engineering-reader summaries.
8. Generate the standard title string from [title-format-guide](./references/title-format-guide.md) or `scripts/generate_change_title.py`.

## Input Priority

Use inputs in this order:
1. Jira ticket context
2. implementation summary or diff summary
3. review findings or correction summary
4. acceptance criteria and QA notes
5. screenshots, logs, or supporting artifacts if they help explain impact

If the ticket and implementation summary disagree, note the discrepancy instead of hiding it.

## Summarization Rules

- Prefer practical engineering language over abstract wording.
- Explain the root cause in concrete terms when known; otherwise mark it as likely or inferred.
- Summarize the fix approach as the chosen strategy, not as line-by-line code narration.
- Keep "what changed" scoped to the meaningful user-facing or architectural impact.
- Call out affected areas with enough specificity for QA and future debugging.
- Treat regression risk as part of the summary, not as an optional appendix.
- If the change has security-sensitive impact, summarize it plainly without turning the summary into a security report.
- Keep the short summaries compact enough for engineering handoff and summary comments.
- Do not use filler such as "minor changes" or "fixed some bugs".

## Output Contract

Produce the final summary in this order:
- Ticket summary
- Root cause
- Fix approach
- What changed
- Affected areas
- Regression risks
- Security note if relevant
- QA focus areas
- Suggested test scenarios
- Short summary for ticket history
- Short summary for engineering readers

Also include:
- Suggested title
- Suggested commit title
- Suggested summary title
- Suggested QA handoff title

## Handoff Guidance

### For QA Readers

Focus on:
- what behavior changed
- where regression is most likely
- which flows deserve direct verification
- which edge cases or states matter most

### For Engineering Readers

Focus on:
- why the bug or gap existed
- what strategy corrected it
- which modules or flows were affected
- what future maintainers should keep in mind

## Navigation

- **[Summarization Workflow](./references/summarization-workflow.md)** - Load for the end-to-end handoff sequence.
- **[Change Summary Template](./references/change-summary-template.md)** - Load for the main output structure.
- **[Root Cause Template](./references/root-cause-template.md)** - Load to phrase root cause and fix linkage clearly.
- **[QA Handoff Template](./references/qa-handoff-template.md)** - Load when the summary needs strong QA guidance.
- **[Regression Risk Template](./references/regression-risk-template.md)** - Load to summarize likely impact and areas to recheck.
- **[Short Ticket History Template](./references/short-ticket-history-template.md)** - Load for concise comment-friendly summaries.
- **[Title Format Guide](./references/title-format-guide.md)** - Load to generate `type: TICKET-ID | summary`.
- **[Security Risk Checklist](../../docs/security/security-risk-checklist.md)** - Load when the summary needs a concise note about auth, data, storage, logging, or trust-boundary impact.
- **[Security Severity Guide](../../docs/security/security-severity-guide.md)** - Load to phrase the importance of a security note consistently.

## Key Reminders

- Summarize. Do not code.
- Explain why, not just what.
- Keep the reader oriented to affected behavior and affected areas.
- Include regression risks and QA focus in every meaningful delivery summary.
- Preserve important security-sensitive context when it changes validation or rollback expectations.
- Prefer concise, high-signal bullets.
- Include Jira ticket ID in suggested titles when available.

## Red Flags - STOP

Stop and correct course when:
- The summary says "fixed issue" without root cause or change detail
- The output reads like a raw diff dump
- QA focus areas are missing from a user-facing change
- Regression risks are omitted even though shared logic changed
- A material security-sensitive change is hidden from QA or future readers
- The engineering summary is too vague to help a future maintainer
- The title does not match `type: TICKET-ID | summary`

## Integration Notes

- Use with Jira-backed workflows when ticket context is available.
- Pair naturally after `ticket-review` and before `ticket-close`.
- Use as the explanation layer for engineering handoff and QA context, not as the final Jira closure record.
