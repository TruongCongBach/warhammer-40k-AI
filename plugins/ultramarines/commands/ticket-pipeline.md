---
description: "Run full ticket pipeline: librarian → inquisitor → techmarine → chapter-master → apothecary → tech-priest. Pass ticket-id or ticket text as arg."
argument-hint: "[ticket-id or text]"
allowed-tools: ["Agent", "Read", "Bash", "Edit", "Write", "Grep"]
---

# /ticket-pipeline

Orchestrate full ticket pipeline (Codex Astartes — 6 disciplined steps).

> **Doctrine reference**: every agent in this pipeline is bound by `plugins/ultramarines/CODEX_ASTARTES.md` (Universal Tenets + per-agent Oath + hand-off contract + stop-points). Read it once before tweaking pipeline behavior. Stop-points listed here are mirrored in the Codex.

## Input

`$ARGUMENTS` — Jira ticket ID (e.g. `MWL-123`) or pasted ticket text/bug report.

## Steps

Run **sequentially**. Each step depends on previous output.

### 1. Librarian — Analyze
Invoke agent `librarian` with the ticket. Wait for structured analysis (summary, requirements, ambiguities, readiness).

**Stop if** readiness = `needs-clarification`. Ask user before continuing.

### 2. Inquisitor — Root cause
Only for **bug**/regression tickets. Skip for pure feature.
Invoke agent `inquisitor` with librarian's output. Wait for root cause + confidence.

**Stop if** confidence = `low` and no clear next step. Ask user.

### 3. Techmarine — Plan
Invoke agent `techmarine` with prior outputs. Get 1-2 approaches + recommendation.

**Stop and ask user** which approach to execute. Default to recommended.

### 4. Chapter-Master — Implement
Invoke agent `chapter-master` with approved approach. Edit code.

**Stop if** lint/typecheck fails. Hand back self-fix loop max 2 times, then ask user.

### 5. Apothecary — Impact
Invoke agent `apothecary` with diff. Get blast radius + regression matrix + rollback plan.

### 6. Tech-Priest — Test
Invoke agent `tech-priest` with apothecary's risk matrix. Tool auto-chosen (Maestro vs agent-device).

**Loop back** to chapter-master if test fail (max 2 iterations).

## Final Output

After all 6 steps, summarize:

```
## Pipeline Result: [ticket-id]

| Step | Agent | Status |
|---|---|---|
| 1 Analyze | librarian | done |
| 2 Cause | inquisitor | done / skipped |
| 3 Plan | techmarine | approach A |
| 4 Implement | chapter-master | done |
| 5 Impact | apothecary | risk: low/med/high |
| 6 Test | tech-priest | pass/fail |

### Files changed
[list]

### Test evidence
[paths]

### Next
- /ticket-commit để commit
- skill ticket-summary để viết QA note
- skill ticket-close để close ticket
```

## User control

User có thể skip step bằng `/ticket-pipeline [ticket] --skip=cause,test` (parse `--skip=` từ args).

User có thể dừng giữa chừng bằng cách reply trong stop point.

## Language

Match user language (Việt/Anh).
