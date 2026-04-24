---
name: ticket-close
description: Prepare final Jira closure content after implementation has been reviewed and approved. This skill should be used only when an approved change summary needs to be turned into a concise final ticket comment, QA closure note, closure summary, and status update for future readers, without writing or modifying code.
progressive_disclosure:
  entry_point:
    summary: "Turn approved implementation context into clean final Jira closure content, QA handoff notes, short future-reader summaries, and a concise security note when relevant."
    when_to_use: "Use only after the fix or feature is approved and the next step is to leave a clear, consistent final Jira record."
    quick_start: "1. Read ticket and approved change summary 2. Extract what was fixed, what QA should verify, and any security note 3. Draft final comment and QA handoff 4. Add concise closure summary and status update 5. Generate final titles"
  references:
    - references/closure-workflow.md
    - references/final-ticket-comment-template.md
    - references/qa-handoff-template.md
    - references/closure-summary-template.md
    - references/concise-status-update-template.md
    - references/title-format-guide.md
    - ../../docs/security/security-risk-checklist.md
    - ../../docs/security/security-severity-guide.md
---

# Ticket Close

## Overview

Use this skill to create the final communication artifacts for a Jira ticket after the work is approved. Read Jira context when available, accept the approved change summary, and produce a concise final ticket comment, QA closure note, short closure summary, and optional release-note-style summary that future readers can scan quickly. If the approved change touched security-sensitive behavior, preserve the minimum necessary note for QA and future readers.

Keep the workflow closure-only. Do not implement code, re-review the patch, or turn the output into an automated close-ticket action.

Always respond in the user's current language. If the user writes in Vietnamese, reply in Vietnamese. If the user writes in English, reply in English. Keep technical terms in their original form when that is clearer.

## When to Use This Skill

Activate when:
- A fix or feature has been approved and needs a final Jira comment
- QA needs a clean final closure note with clear validation focus
- Ticket history needs a short closure summary for future readers
- A concise status update is needed after work completion
- Comment style needs to stay consistent across tickets

Do not activate when:
- The work is still under review or awaiting approval
- No completed change summary exists yet
- The task is to code, review, or plan additional changes
- The user still needs an engineering-facing explanation of the implementation itself
- The user only wants a raw changelog or diff dump

## The Iron Law

Close the communication loop clearly. Explain what was fixed, what QA should verify, and any remaining notes or risks in a format that future readers can understand without reopening the full diff.

## Core Principles

1. **Closure-focused output**: Write for the final ticket record, not for internal implementation planning.
2. **Concise completeness**: Include enough context to explain outcome and validation without becoming verbose.
3. **QA-aware wording**: Call out what should be verified directly, not just what changed in code.
4. **Consistent structure**: Keep ticket comments and handoff notes easy to scan across tickets.
5. **Future-reader utility**: Make the outcome understandable months later without diff archaeology.
6. **Security-aware closure**: Mention security-sensitive impact only when it changes QA focus, release notes, or future debugging context.

## Quick Start

1. Read Jira ticket context when available and capture ticket ID, issue type, summary, and acceptance criteria.
2. Read the completed change summary and any approved review notes.
3. Extract:
   - what was fixed
   - what QA should verify
   - any risks, follow-up notes, or security note if relevant
4. Draft the final ticket comment using [final-ticket-comment-template](./references/final-ticket-comment-template.md).
5. Draft the QA handoff note using [qa-handoff-template](./references/qa-handoff-template.md).
6. Add a short closure summary and concise status update using the reference templates.
7. Add an optional release-note-style summary only when the change is user-visible or broadly relevant.
8. Generate the standard title string from [title-format-guide](./references/title-format-guide.md) or `scripts/generate_closure_title.py`.

## Input Priority

Use inputs in this order:
1. Jira ticket context
2. approved change summary
3. implementation review outcome
4. QA notes or validation guidance
5. additional release or handoff context if relevant

If the approved summary and ticket scope do not align, note the discrepancy instead of hiding it.

## Closure Rules

- Keep the final comment concise and structured.
- Prefer concrete wording such as what behavior changed and what QA should verify.
- Avoid generic statements such as "done" or "fixed issue".
- Keep risks and notes short, and include them only when they matter.
- Include a security note only when the ticket changed auth, permissions, data exposure, storage, logging, uploads, or trust-boundary behavior in a way QA or future readers should know.
- Use release-note-style wording only when the change would make sense outside the immediate ticket context.
- Keep the short closure summary readable for someone scanning ticket history.
- Keep the tone professional and low-friction.

## Output Contract

Produce the final closure output in this order:
- Suggested title
- Final ticket comment
- QA handoff note
- What was fixed
- What QA should verify
- Risks / notes if any
- Security note if relevant
- Short closure summary
- Optional release-note-style summary if relevant

Also include:
- Suggested ticket comment title
- Suggested QA handoff title

## Comment Guidance

### Final Ticket Comment

Use the final comment to explain:
- what was fixed or delivered
- what changed at a user-visible or workflow level
- what QA should focus on
- any important note worth preserving in the ticket

### QA Handoff Note

Use the QA note to highlight:
- the primary flow to validate
- the states or scenarios most likely to regress
- any platform or environment detail that matters for verification

Treat this note as the final QA closure handoff, not as a broader engineering summary.

### Short Closure Summary

Use the short closure summary as:
- a compact ticket-history entry
- a future-reader snapshot of the final outcome

## Navigation

- **[Closure Workflow](./references/closure-workflow.md)** - Load for the end-to-end closure sequence.
- **[Final Ticket Comment Template](./references/final-ticket-comment-template.md)** - Load for the main Jira comment structure.
- **[QA Handoff Template](./references/qa-handoff-template.md)** - Load for QA-focused validation notes.
- **[Closure Summary Template](./references/closure-summary-template.md)** - Load for a compact future-reader summary.
- **[Concise Status Update Template](./references/concise-status-update-template.md)** - Load for short completion updates.
- **[Title Format Guide](./references/title-format-guide.md)** - Load to generate `type: TICKET-ID | summary`.
- **[Security Risk Checklist](../../docs/security/security-risk-checklist.md)** - Load when the closure note should preserve a small but important security-sensitive context.
- **[Security Severity Guide](../../docs/security/security-severity-guide.md)** - Load to keep the tone of a security note proportional to its impact.

## Key Reminders

- Close the loop clearly.
- Keep the comment easy to scan.
- Tell QA what to verify, not just what changed.
- Keep risks and notes brief but explicit when needed.
- Preserve material security-sensitive context, but do not turn the closure comment into a full review report.
- Include the Jira ticket ID in suggested titles when available.
- Do not drift into implementation details unless they explain the outcome.

## Red Flags - STOP

Stop and correct course when:
- The ticket comment is vague or says only "done"
- QA handoff does not say what to verify
- The closure summary is too long to scan quickly
- The output repeats the entire implementation summary instead of condensing it
- A material security-sensitive change is omitted even though it changes QA focus or future debugging context
- The title does not match `type: TICKET-ID | summary`

## Integration Notes

- Use after `ticket-summary` or any approved implementation summary.
- Pair naturally with Jira workflows that require a final human-readable closure comment.
- Use the optional release-note-style section only when it adds value beyond the ticket itself.
