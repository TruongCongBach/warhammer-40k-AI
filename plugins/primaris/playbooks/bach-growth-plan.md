# Bach — Growth Plan

> Living document. Bach edits this when targets shift. Cawl reads it to align weekly recommendations.

**Last updated:** 2026-05-07

---

## Current state

- **Level:** Advanced Context Engineer (Level 3), approaching Early Hermes (Level 4).
- **Strongest evidence base:** Ultramarines pipeline in active use, Codex Astartes adopted, retry guard enforced via `scripts/check-iter.sh`, astropath external-research discipline, dark-angels security gate.
- **Weakest evidence base:** Root cause is sometimes inferred rather than proved before code; scope drift on multi-file changes; first-pass accuracy still requires multiple iterations on tricky bugs.

## Strengths to preserve

- Verification discipline (real-device, Charles, Maestro flow).
- Commit hygiene (ticket-scoped, manual review of `git status`).
- Workflow engineering (multi-agent pipeline, retry guard, halt-on-uncertainty).

## Weaknesses to fix

- **Root-cause enforcement.** Move from "investigate → attempt fix → verify → fail → refine → verify" to "investigate → prove root cause → smallest fix → verify". Forward link: Phase 2 ships `/investigate` skill.
- **First-pass accuracy.** Reduce average iterations per ticket toward 1.0–1.5. Hypothesis-driven debugging instead of patch-and-test.
- **Upfront scope constraint.** Declare allowed/forbidden files at ticket start. Forward link: Phase 3 ships `pre-edit-scope-check.sh` hook.

## 30-day targets (review by 2026-06-06)

- ≥80% of bug tickets prove root cause (Tenet 1 ritual visible in run log) before first edit.
- Scope drift events ≤1 per week (Cawl flags drift = files changed outside declared scope, or commits straying from the ticket subject).
- ≥1 multi-agent orchestration run per week outside `/ticket-pipeline` (e.g. parallel `Explore` + research + plan).
- Average iterations per ticket ≤1.8.
- ≥4 weekly `/level-check` reports filed by 2026-06-06.

## 90-day targets (review by 2026-08-06)

- Reach Hermes (Level 4) — ≥80% of Level 4 capability checklist hit, with ≥3 signals per week and zero anti-signals across the previous 4 weeks.
- ≥1 self-correcting workflow shipped (autonomous AI verify → re-plan → retry within cap).
- Cawl recommendations referenced in ≥50% of subsequent commit messages or session notes (acted on, not archived).
- Phase 2 (Prime Directive enforcement) and Phase 3 (hard hooks) shipped and in active use.

## Cawl's working assumptions

When scoring, Cawl should treat the following as Bach's stable preferences (do not flag as anti-signals):

- Vietnamese-primary user-facing prose, English code/commits — per Codex Tenet 5.
- Caveman compression mode is acceptable communication, not a regression.
- Manual commit/PR steps preferred over automation — per Ultramarines pipeline doctrine.
- Tenet violations are tracked but a single violation in a 7-day window is "neutral", not "falling".
