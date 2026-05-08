# Primaris — Personal AI Engineering OS

> *"The Astartes were enough for ten thousand years. They are not enough now. Patience and revision will make them so."*
> — Belisarius Cawl, Archmagos Dominus

A personal AI Engineering OS that any Claude Code user can install, configure, and use as a self-coaching loop. Sibling plugin to `ultramarines`. Where ultramarines runs the ticket pipeline, primaris **observes the engineer** running it and turns each `/insights` cycle into measurable progress toward the next engineering level.

## Why this exists

Skill at *using AI* compounds across tickets, not within them. Skill at *coding* compounds within tickets. Without an explicit rubric and a record-keeping discipline, capability growth is invisible — and invisible growth eventually plateaus. Cawl is the record. The doctrine is the rubric. `/level-check` is the read-out.

## Components

| Component | Path | Role |
|---|---|---|
| Doctrine | `PRIMARIS_DOCTRINE.md` | 7 personal-growth tenets |
| Levels rubric | `playbooks/ai-engineering-levels.md` | Level 0–5 definitions, signals, anti-signals, **Roadmap to Level N+1** |
| Growth plan template | `playbooks/growth-plan.template.md` | Ship template (read-only) |
| Growth plan (user) | `$PRIMARIS_HOME/growth-plan.md` (default `~/.primaris/growth-plan.md`) | User's personalised state and targets — you edit this |
| Prime directive | `playbooks/prime-directive.md` | Tenet 1 expanded — 7-step ritual + exceptions |
| Cawl agent | `agents/cawl.md` | Meta-analyst — reads `/insights` report + run artifacts, scores, recommends |
| `/level-check` command | `commands/level-check.md` | Manual entry point |
| Eval reports | `$PRIMARIS_HOME/eval/` | Cawl writes here; you read weekly |

## Composition with ultramarines

After `/ticket-pipeline` Block 4 (TEST) passes, the pipeline auto-invokes Cawl with the ticket id. Cawl writes a per-ticket eval report. If primaris is not installed, the pipeline skips this step silently — ultramarines remains fully usable on its own.

## First-run flow

```bash
# 1. Create the user-data directory.
mkdir -p ~/.primaris/eval

# 2. Copy the template into your personal growth plan and edit it.
cp plugins/primaris/playbooks/growth-plan.template.md ~/.primaris/growth-plan.md
$EDITOR ~/.primaris/growth-plan.md

# 3. Inside any Claude Code session, generate the /insights report.
#    (This is a Claude Code slash command — type it in the CLI, not in a shell.)
/insights

# 4. Read your first Level Check.
/level-check 7d
```

After that, treat the loop as weekly maintenance: refresh `/insights`, run `/level-check 7d`, read the recommendations, edit `growth-plan.md` when targets shift.

## Environment

| Variable | Default | Purpose |
|---|---|---|
| `PRIMARIS_HOME` | `~/.primaris` | Where the user's growth plan and eval reports live. Override to support multiple personas on one machine or a portable location across machines. |

The Claude Code `/insights` report path (`~/.claude/usage-data/report.html`) is currently fixed by Claude Code itself; primaris reads it at the canonical location.

## Phase scope

This is **Phase 1.5 of 4** for the primaris plugin:

- **Phase 1 (v0.1.0) — Doctrine + Meta Loop.** Doctrine, playbooks, Cawl, /level-check.
- **Phase 1.5 (v0.2.0, this release) — Generic + Insights-driven.** Cawl reads `/insights`. User-data relocates to `$PRIMARIS_HOME`. Levels rubric gains per-level Roadmap.
- **Phase 2 — Prime Directive Enforcement.** Skills `investigate`, `repro-first`, `scope-guard`. Codex Tenet 13.
- **Phase 3 — Hard Hooks.** `pre-edit-scope-check.sh`, `post-fix-evidence.sh`, skill `verify-loop`.
- **Phase 4 — Workflow Library.** `bug-investigation.md`, `ticket-to-pr.md`, `ui-regression.md`, skill `checkpoint`.

## Migration from v0.1.0

If you were running v0.1.0:

1. Pull the v0.2.0 commits.
2. `mkdir -p ~/.primaris/eval`.
3. `cp plugins/primaris/playbooks/growth-plan.template.md ~/.primaris/growth-plan.md`.
4. Open the new growth plan in your editor and copy in whatever you had personalised in `bach-growth-plan.md` (that file is removed in v0.2.0).
5. Run `/insights`.
6. Run `/level-check 7d`.

## Versioning

Plugin version follows semver. Doctrine is versioned alongside the plugin. Tenet add/remove requires a minor version bump and a one-line note here in a future changelog section.

Current version: **0.2.0** (2026-05-08 — Phase 1.5: generic + insights-driven).
