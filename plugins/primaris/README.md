# Primaris — Personal AI Engineering OS

> *"The Astartes were enough for ten thousand years. They are not enough now. Patience and revision will make them so."*
> — Belisarius Cawl, Archmagos Dominus

Personal AI Engineering OS for Bach. Sibling plugin to `ultramarines`. Where ultramarines runs the ticket pipeline, primaris **observes the engineer** running the pipeline and turns each ticket into measurable progress toward the next engineering level.

## Why this exists

Skill at *using AI* is not the same as skill at *coding*. The first is a capability that compounds across tickets; the second compounds within a ticket. Without an explicit rubric and a record-keeping discipline, capability growth is invisible — and invisible growth eventually plateaus. Cawl is the record. The doctrine is the rubric. `/level-check` is the read-out.

## Components

| Component | Path | Role |
|---|---|---|
| Doctrine | `PRIMARIS_DOCTRINE.md` | 7 personal-growth tenets |
| Levels rubric | `playbooks/ai-engineering-levels.md` | Level 0–5 definitions, signals, anti-signals |
| Growth plan | `playbooks/bach-growth-plan.md` | Current state, 30/90-day targets — Bach edits this |
| Prime directive | `playbooks/prime-directive.md` | Tenet 1 expanded — 7-step ritual + exceptions |
| Cawl agent | `agents/cawl.md` | Meta-analyst — reads run artifacts, scores them, recommends |
| `/level-check` command | `commands/level-check.md` | Manual entry point |
| Eval reports | `eval/` | Cawl writes here; Bach reads weekly |

## Composition with ultramarines

After `/ticket-pipeline` Block 4 (TEST) passes, the pipeline auto-invokes Cawl with the ticket id. Cawl writes a per-ticket eval report. If primaris is not installed, the pipeline skips this step silently — ultramarines remains fully usable on its own.

## First-run flow

1. Install via `imperium-of-guilliman` marketplace (already registered).
2. Open `playbooks/bach-growth-plan.md` and confirm or edit current state and targets.
3. Run any ticket through `/ticket-pipeline` — eval report appears under `plugins/primaris/eval/`.
4. Weekly: run `/level-check 7d` to read the trend.
5. Monthly: review `playbooks/bach-growth-plan.md` and update targets if they no longer match observed reality.

## Phase scope

This is **Phase 1 of 4** for the primaris plugin:

- **Phase 1 — Doctrine + Meta Loop** (this release). Doctrine, playbooks, Cawl, /level-check.
- **Phase 2 — Prime Directive Enforcement.** Skills `investigate`, `repro-first`, `scope-guard`. Codex Tenet 13.
- **Phase 3 — Hard Hooks.** `pre-edit-scope-check.sh`, `post-fix-evidence.sh`, skill `verify-loop`.
- **Phase 4 — Workflow Library.** `bug-investigation.md`, `ticket-to-pr.md`, `ui-regression.md`, skill `checkpoint`.

## Versioning

Plugin version follows semver. Doctrine is versioned alongside the plugin. Tenet add/remove requires a minor version bump and a one-line note here in a future changelog section.

Current version: **0.1.0** (2026-05-07 — Phase 1 ship).
