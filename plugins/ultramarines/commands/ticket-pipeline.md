---
description: "Lean ticket pipeline — 4 blocks with explicit user stop-points: ANALYZE → IMPLEMENT → GATE → TEST. Commit + PR stay manual. Retry guarded by scripts/check-iter.sh (cap 1)."
argument-hint: "[ticket-id or text] [--skip=cause,security,test] [--cap=N]"
allowed-tools: ["Agent", "Read", "Bash", "Edit", "Write", "Grep"]
---

# /ticket-pipeline (lean Option A)

Orchestrate ticket through 4 disciplined blocks. **Auto inside a block, STOP between blocks.** Retry capped by hard guard, not honor system.

> **Doctrine**: every agent is bound by `plugins/ultramarines/CODEX_ASTARTES.md` (Universal Tenets I + Tenet 11 retry-guard). Read once before tweaking pipeline behavior.

> **Manual gate**: pipeline ends at TEST. **Commit** and **PR** stay manual — invoke skill `ticket-commit` and `gh pr create` yourself. Pipeline NEVER auto-commits, NEVER auto-pushes, NEVER auto-opens PR.

## Input

`$ARGUMENTS`:
- ticket-id (`MWL-123`) or pasted ticket text
- `--skip=cause,security,test` (optional)
- `--cap=N` (optional, default `1` — retry cap per step)

## State file

Pipeline writes to `.imperium/runs/<ticket-id>/state.json`. Local-only (gitignored). Retry guard reads + bumps counters there.

To inspect / reset:
```bash
bash scripts/check-iter.sh --show <ticket-id>
bash scripts/check-iter.sh --reset <ticket-id>
```

---

## Block 1 — ANALYZE (auto)

**Agents:** `librarian` → `inquisitor` (skip inquisitor if pure feature, or `--skip=cause`).

1. Invoke `librarian` with ticket. Wait for analysis (summary, requirements, ambiguities, readiness).
2. **Internal stop** — if librarian readiness = `needs-clarification`, halt + ask user.
3. Invoke `inquisitor` with librarian's output (bug only). Wait for root cause + confidence.
4. **Internal stop** — if inquisitor confidence = `low` and no clear next step, halt + ask user.

### → STOP 1: Approve approach

Then invoke `techmarine` for plan (1-2 approaches + recommendation).

**Halt and prompt user:**
```
Block 1 done. Techmarine proposed:
  Approach A — [...]
  Approach B — [...]
  Recommended: A

Approve which? (A/B/modify/abort)
```

User reply gates Block 2.

---

## Block 2 — IMPLEMENT (auto, retry cap 1)

**Agent:** `chapter-master`.

**Retry guard (mandatory per Tenet 11):**
```bash
bash scripts/check-iter.sh "$TICKET" chapter_master "$CAP"
```
Run BEFORE every chapter-master invocation (including first). Paste guard output in response. Non-zero exit → HALT, hand to user. Do NOT skip the guard call.

1. Run guard.
2. Invoke `chapter-master` with approved approach. Edits code.
3. If lint/typecheck fails → run guard again, retry once. If guard exits 1 → halt.

### → STOP 2: Diff review

**Halt and prompt user:**
```
Block 2 done.
Files changed: [list]
Diff: run `git diff` to review.

Continue to security gate? (yes/abort/modify)
```

User reply gates Block 3.

---

## Block 3 — GATE (auto, no retry)

**Agents:** `apothecary` → `dark-angels`. Skippable via `--skip=security` (apothecary still runs).

1. Invoke `apothecary` with diff. Get blast radius + regression matrix + rollback plan.
2. Invoke `dark-angels` with diff + apothecary output. Get severity-classified findings + recommendation (`clean` / `needs-fix-before-test` / `HALT-pipeline`).

**Hard halt** — if dark-angels reports `HALT-pipeline` (any critical/high finding):
- State HALT explicitly with `file:line` + remediation.
- Hand back to user. Do NOT proceed to test.
- User must fix manually then re-run pipeline (or fix + re-invoke chapter-master + dark-angels).

### → STOP 3: Confirm before test

**Halt and prompt user:**
```
Block 3 done.
Apothecary risk: [low/med/high]
Dark-angels: [clean / N findings — list severity]

Continue to test? (yes/abort)
```

If dark-angels = clean and apothecary risk = low, user can pre-approve via `--auto-test` (future flag). Default = stop.

---

## Block 4 — TEST (auto, retry cap 1)

**Agent:** `tech-priest`.

**Precondition:** dark-angels result must be `clean`. If `needs-fix-before-test`, do NOT enter Block 4.

**Retry guard (mandatory per Tenet 11):**
```bash
bash scripts/check-iter.sh "$TICKET" tech_priest "$CAP"
```
Run BEFORE every tech-priest invocation. Paste guard output. Non-zero exit → HALT.

1. Run guard.
2. Invoke `tech-priest`. Tool auto-chosen per doctrine (Maestro for ≥3-step E2E via skill `maestro`, agent-device for ≤2-step / exploratory).
3. If test fail → run guard, retry once with hand-back to chapter-master. If guard exits 1 → halt + hand to user.

### → STOP 4: Pipeline end (manual hand-off)

Pipeline complete. **Do NOT commit, do NOT push, do NOT open PR.**

```
✅ Pipeline done. Manual next steps (none auto-run):

  1. `git diff` to re-review final state
  2. Skill `ticket-commit` to commit (when user OK)
  3. Skill `ticket-summary` to write QA note
  4. `gh pr create` thủ công
  5. Skill `ticket-close` to close ticket

State file: .imperium/runs/<ticket-id>/state.json (kept for resume)
```

#### Optional auto-fire — Cawl meta-eval

If the `primaris` plugin is installed, auto-invoke Cawl to score this run and write a per-ticket eval report.

**Existence check (graceful)**:

```bash
test -d plugins/primaris/agents && test -f plugins/primaris/agents/cawl.md && echo CAWL_AVAILABLE || echo CAWL_SKIP
```

If `CAWL_AVAILABLE`:

- Invoke `Task(subagent_type="primaris:cawl", ticket_id="$TICKET")`.
- Append the returned report path to the pipeline output: `Eval report: plugins/primaris/eval/<filename>`.

If `CAWL_SKIP`:

- Print one-line note: `primaris plugin not installed — skipping Cawl meta-eval.`
- Continue without error.

This step is non-blocking. Failures (Cawl crash, missing playbook) print a single warning line and do not affect pipeline status.

---

## Final summary table

```
## Pipeline Result: [ticket-id]

| Block | Agents | Status | Iter |
|---|---|---|---|
| 1 ANALYZE   | librarian → inquisitor → techmarine | done | — |
| 2 IMPLEMENT | chapter-master                       | done | N/CAP |
| 3 GATE      | apothecary → dark-angels             | clean / N findings | — |
| 4 TEST      | tech-priest                          | pass/fail | N/CAP |

### Files changed
[list]

### Test evidence
[paths]

### Security findings
[count by severity, or "clean"]

### Next (user-action, NOT auto)
- Review diff
- Skill ticket-commit
- gh pr create
- Skill ticket-close
```

## User control

- **Skip step:** `--skip=cause,security,test` (valid keys: `cause`, `security`, `test`)
- **Bump cap:** `--cap=2` (default 1) — only when expected legitimate retry need
- **Stop midway:** reply at any STOP point with `abort`
- **Force past dark-angels HALT:** requires explicit `confirm-override` reply in same turn (Tenet 3 — risky-op confirmation)
- **Reset state:** `bash scripts/check-iter.sh --reset <ticket-id>` then re-run pipeline

## Language

Per Codex Tenet 5 — bilingual: primary = user language (Việt), secondary = English. Code stays English.
