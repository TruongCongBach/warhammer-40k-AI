# Primaris Doctrine

> *"The flesh is weak. The mind is unproven. Both can be made stronger — by record, by trial, by patient revision."*
> — Belisarius Cawl, Archmagos Dominus, Forge of Mars

The doctrine that guides **the engineer's personal engineering growth** across tickets. Read this before invoking the `cawl` agent, modifying a playbook, or interpreting a `/level-check` report.

## Boundary with the Codex Astartes

| File | Scope | Audience |
|---|---|---|
| `plugins/ultramarines/CODEX_ASTARTES.md` | **Pipeline rule** — how an agent behaves *inside* a ticket run | Every Ultramarines agent |
| `plugins/primaris/PRIMARIS_DOCTRINE.md` | **Personal growth rule** — how the engineer grows *across* tickets | Cawl + the engineer |

The two doctrines do not overlap. Codex governs ticket execution. Primaris governs the meta-loop that observes ticket execution and turns it into measurable progress.

---

## The 7 Tenets

### Tenet 1 — No Root Cause → No Code (Prime Directive)

For every issue: reproduce → gather evidence → enumerate hypotheses → prove/disprove → identify the true root cause → define the smallest fix surface → THEN code. Symptom-patching is forbidden.

See `playbooks/prime-directive.md` for the 7-step ritual, exceptions (typo / single-line config / doc-only), and anti-pattern examples.

### Tenet 2 — Smallest Fix Surface

Before editing, declare allowed files and out-of-scope files. Bug fix ≠ refactor pass; feature add ≠ cleanup tour. Out-of-scope edits are an explicit reject — bring them back as their own ticket.

### Tenet 3 — Verify Before Done

No "done" without verification on the right surface: real device for mobile, SSR/hydration for web, cache/memo/query-key for data layers. Verification artifact (screenshot, log, trace) is required.

### Tenet 4 — Commit Hygiene Sacred

Ticket-scoped commits only. Run `git status` and `git diff --stat` before every commit. Stage by name, never `git add -A`. The commit log is a permanent audit trail; treat it that way.

### Tenet 5 — Evidence Over Claim

"Claude says so" is no longer acceptable. Every claim that drives a decision must be backed by a screenshot, log line, trace, or grep result. Memory and pattern-matching are starting points, not proof.

### Tenet 6 — AI = Workforce, Not Assistant

Default to orchestration: parallel sub-agents for independent work, verifier agents for self-correction, dedicated agents per domain. Treat single-prompt back-and-forth as a regression toward Level 1.

### Tenet 7 — Continuous Self-Audit

Cawl observes after every ticket and at every weekly `/level-check`. The reports are read, not archived. Ignored reports = a violation of this tenet, equivalent to running without instrumentation.

See `$PRIMARIS_HOME/growth-plan.md` (default `~/.primaris/growth-plan.md`) for current targets and `playbooks/ai-engineering-levels.md` for the level rubric.

---

## Versioning

This doctrine is versioned with the primaris plugin. Bumps follow semver on `plugin.json`. Tenet additions or removals require a minor version bump and a one-line note in the plugin README changelog.

Current version: **1.0** (2026-05-07 — initial canonization, Phase 1).
