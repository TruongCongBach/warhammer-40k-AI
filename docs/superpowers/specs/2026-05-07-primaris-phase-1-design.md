# Primaris Plugin — Phase 1 Design

**Date**: 2026-05-07
**Author**: Bach (TruongBach) + Claude (Opus 4.7)
**Status**: Approved (sections 1-5)
**Phase**: 1 of 4 (Doctrine + Meta Loop)

---

## Vision

Transform `warhammer-40k-AI` from a basic skill/agent/workflow set into a personal **AI Engineering OS** that helps Bach grow from `Advanced Context Engineer (Level 3)` toward `Hermes Engineer (Level 4)` and ultimately `AI Systems Engineer (Level 5)`.

The OS is delivered as a new sibling plugin `primaris` running alongside the existing `ultramarines` plugin. Ultramarines remains the ticket-pipeline specialist; primaris is the meta-layer that observes Bach's work, scores it against an explicit growth rubric, and feeds back actionable recommendations.

Inspired by *Belisarius Cawl*, the Archmagos Dominus who engineered the Primaris program — an upgrade path that makes Space Marines stronger over centuries. The plugin's role is identical: a long-horizon upgrade path, not a one-shot tool.

## Scope (Phase 1 only)

**In scope**

- New plugin `plugins/primaris/` registered in `.claude-plugin/marketplace.json`.
- `PRIMARIS_DOCTRINE.md` — 7 personal-growth tenets (mirror Codex Astartes pattern, shorter).
- 3 playbooks (`ai-engineering-levels.md`, `bach-growth-plan.md`, `prime-directive.md`).
- 1 agent — `cawl` — passive analyst that scores sessions against the rubric.
- 1 command — `/level-check [period]` — manual entry point.
- Composition: edit `plugins/ultramarines/commands/ticket-pipeline.md` to auto-invoke Cawl after the TEST block (graceful degrade if primaris is missing).

**Out of scope (deferred to later phases)**

- Phase 2 — Prime Directive enforcement (skills `investigate`, `repro-first`, `scope-guard`, `/investigate` command, Codex Tenet 13).
- Phase 3 — Hard hooks (`pre-edit-scope-check.sh`, `post-fix-evidence.sh`, skill `verify-loop`).
- Phase 4 — Workflow library (`bug-investigation.md`, `ticket-to-pr.md`, `ui-regression.md`, skill `checkpoint`).
- Phase 1.5 — Stop hook capturing non-ticket sessions.

Each later phase gets its own spec → plan → impl cycle.

## Architecture

### Plugin layout

```
plugins/primaris/
├── .claude-plugin/plugin.json
├── README.md
├── PRIMARIS_DOCTRINE.md
├── agents/
│   └── cawl.md
├── commands/
│   └── level-check.md
├── playbooks/
│   ├── ai-engineering-levels.md
│   ├── bach-growth-plan.md
│   └── prime-directive.md
└── eval/
    └── .gitkeep
```

### Marketplace registration

Add a second plugin entry in `.claude-plugin/marketplace.json` with the same author/source pattern as ultramarines. Plugin ID: `primaris`. Display name: `Primaris — Personal AI Engineering OS`. Version: `0.1.0`.

### Composition with ultramarines

Edit `plugins/ultramarines/commands/ticket-pipeline.md` to append a step at the end of the TEST block:

```markdown
**After TEST block passes** (optional, graceful):
- If primaris plugin is installed, invoke `cawl` agent via `Task(subagent_type="primaris:cawl", ticket_id=$TICKET_ID)`.
- Cawl reads run artifacts and writes an eval report under `plugins/primaris/eval/`.
- The pipeline echoes the eval report path in its final summary.
- If primaris is not installed the step is skipped silently — ultramarines remains fully usable on its own.
```

Cross-plugin agent invocation uses Claude Code's native `<plugin>:<agent>` namespace.

## Component design

### `PRIMARIS_DOCTRINE.md` — 7 Tenets

Each tenet is two to three sentences plus a cross-link to the playbook that owns its ritual.

1. **No Root Cause → No Code** (Prime Directive). Reproduce → evidence → hypotheses → prove/disprove → fix surface → THEN code. See `playbooks/prime-directive.md`.
2. **Smallest Fix Surface**. Declare allowed files before edit. Out-of-scope files are an explicit reject.
3. **Verify Before Done**. Real device / SSR / cache check before commit.
4. **Commit Hygiene Sacred**. Ticket-scoped commits only. `git status` and `git diff --stat` reviewed before every commit.
5. **Evidence Over Claim**. "Claude says so" → "Claude must prove it". Screenshot, log, trace beat vibes.
6. **AI = Workforce, Not Assistant**. Orchestrate sub-agents. Run parallel sessions. Build verify pipelines.
7. **Continuous Self-Audit**. Cawl observes. Eval reports reviewed weekly. Level signals tracked. See `playbooks/bach-growth-plan.md`.

The doctrine and the Codex Astartes (12 tenets, ultramarines plugin) do not overlap. Codex governs *pipeline rule* (how an agent behaves inside a ticket run). Primaris governs *personal growth rule* (how Bach grows across tickets). Both are cross-linked in their headers to make the boundary explicit.

### `agents/cawl.md` — Cawl analyst agent

**Identity**: Archmagos Dominus Belisarius Cawl, Mars Mechanicus. Persona: cold analyst, data-driven, no flattery, names weakness directly.

**Inputs**

- `ticket_id` (auto-fire path) or `period` (manual `/level-check 7d` path).
- Reads:
  - `.imperium/runs/<ticket-id>/state.json` — iteration counter, halt reasons.
  - `.imperium/runs/<ticket-id>/log.md` — block transitions, retry events.
  - `git log --since=<period>` — commit cadence, fix-on-fix patterns.
  - `git diff` per commit — file count, scope sprawl signals.
  - `playbooks/ai-engineering-levels.md` — rubric of capabilities and signals per level.
  - `playbooks/bach-growth-plan.md` — current level, targets, weaknesses to fix.

**Output**

- Markdown report saved at `plugins/primaris/eval/YYYY-MM-DD-<ticket-id-or-period>.md`.
- Console summary (≤30 lines) returned to the caller.

**Report structure**

```markdown
# Cawl Eval — <scope> — <date>

## Metrics
- Iterations: <n>/<cap>
- Commits: <n> (<n> fix:, <n> refactor)
- Files changed: <n> (avg <n>/commit)
- Time-to-root-cause: commit #<n>
- Tenet violations: <n>

## Strengths observed
- <bullet>

## Weaknesses observed
- <bullet>

## Level signal
- Current: <level>
- Movement this run: <up|neutral|down> — <reason>
- Next milestone: <concrete next behavior>

## Recommended action
- <imperative>
```

**Voice**: terse, mechanical. "Data logged. Pattern observed. Recommendation issued." Praise only when a metric earns it.

### `commands/level-check.md` — `/level-check [period]`

**Args**

- (none) → defaults to last 30d.
- `7d` / `30d` / `90d` → window filter.
- `<ticket-id>` → re-score a single ticket.

**Flow**

1. Parse `period`.
2. Gather inputs:
   - `plugins/primaris/eval/*.md` produced by previous Cawl runs.
   - `git log --since=<period>` (full hashes + stats).
   - `.imperium/runs/*/state.json` and `log.md` whose mtime falls inside the period.
3. Spawn `cawl` with the gathered data and the period context.
4. Cawl returns:
   - **Trend section** — average iterations, scope drift count, tenet violations across time.
   - **Level dashboard** — current level, signals tracked toward next level, blockers.
   - **Top 3 recommendations** — concrete actions for the upcoming week.
5. Save aggregate report at `plugins/primaris/eval/level-check-<date>.md`.
6. Print console summary (≤30 lines).

**Console summary template**

```
═══ Cawl Level Check — period <period> ═══

Tickets handled: <n>
Avg iterations: <n>/3 (target: <n>)
Scope drift events: <n>/<n> tickets
Tenet violations: <n> (<tenet ids>)

Level: <n> (<name>) — <stable|rising|falling>
Movement toward L<n+1>: <weak|moderate|strong>

Top recommendations:
1. <imperative>
2. <imperative>
3. <imperative>

Full report: plugins/primaris/eval/level-check-<date>.md
```

### Playbooks

#### `playbooks/ai-engineering-levels.md`

Sourced from the Personal Summary file already present in the repo root. Each level (0–5) gets:

- One-sentence definition.
- 5–7 capability checklist items.
- Concrete *signals to look for* in eval reports (behaviors that imply Bach reached this level).
- Concrete *anti-signals* (regression markers — behaviors that pull Bach back to the previous level).

Cawl uses this file as its scoring rubric.

#### `playbooks/bach-growth-plan.md`

- **Current state** — Advanced Context Engineer (Level 3), approaching Early Hermes.
- **Strengths to preserve** — verification discipline, commit hygiene, AI workflow engineering.
- **Weaknesses to fix** — root-cause enforcement, first-pass accuracy, scope constraint.
- **30-day targets** — ≥80% of tickets prove root cause before code; scope drift events ≤1/week; ≥1 multi-agent orchestration run/week.
- **90-day targets** — Hermes — autonomous verify pipelines; ≥1 self-correcting workflow shipped.

This is the only playbook Bach edits when targets shift. Cawl reads it to align its weekly recommendations.

#### `playbooks/prime-directive.md`

Tenet 1 expanded:

- 7-step ritual (reproduce → gather evidence → enumerate hypotheses → prove/disprove → identify root cause → define smallest fix surface → THEN code).
- Explicit *when to skip* exceptions (typo fix, single-line config, doc-only change).
- Anti-pattern examples paired with corrected versions.
- Forward link: Phase 2's `/investigate` command will mechanise this ritual.

## Acceptance criteria

- [ ] `plugins/primaris/` exists with all 7 core files (plugin.json, README, doctrine, cawl agent, level-check command, 3 playbooks).
- [ ] `.claude-plugin/marketplace.json` has a `primaris` entry.
- [ ] `/level-check` runs without crashing when `eval/` is empty.
- [ ] `/level-check 7d` produces a console summary and a saved aggregate report.
- [ ] `cawl` agent is invokable manually with `Task(subagent_type="primaris:cawl", ticket_id="MWL-123")`.
- [ ] `plugins/ultramarines/commands/ticket-pipeline.md` is updated and still runs end-to-end if primaris is absent (graceful degrade verified).
- [ ] Doctrine has all 7 tenets fully written (no placeholders).
- [ ] All 3 playbooks have full content (no placeholders).
- [ ] `README.md` for primaris explains plugin purpose, lore, install steps, and first-run flow.

## Risks and mitigations

| Risk | Mitigation |
|------|-----------|
| Cawl reports become vibes-based and not actionable. | Rubric is sourced from playbooks (concrete signals / anti-signals). Recommendations are required to be imperative ("do X next time"). |
| Eval reports accumulate into noise. | `/level-check` always filters by period. Aggregate reports compress per-ticket detail into trend lines. |
| Cross-plugin invoke fails when primaris is not installed. | Auto-fire step is wrapped with an existence check; failure path skips with a one-line warning. |
| Bach ignores reports — meta-loop dies. | Phase 2 will add a `/level-check` reminder hook to the Codex Astartes weekly cadence. Phase 1 only delivers the data. |
| Doctrine drift between Codex (12 tenets) and Primaris (7 tenets). | Both files cross-link headers explaining the boundary: Codex = pipeline rule, Primaris = personal growth rule. No overlap. |

## Open questions

None at design time. Implementation may surface refinements (e.g., exact metric thresholds in `bach-growth-plan.md` may shift after the first month of real data).

## Success measure for Phase 1

After 4 weeks of running primaris alongside ultramarines:

- ≥4 weekly `/level-check` reports exist.
- ≥1 recommendation from Cawl was acted on by Bach (visible in subsequent ticket runs).
- Bach can articulate his current level and the next-milestone behavior without re-reading the doctrine.

If those three signals hold, Phase 2 (Prime Directive enforcement) starts.
