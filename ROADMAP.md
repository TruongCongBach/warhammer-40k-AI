# Imperium of Guilliman — Roadmap

Tracking what's next for the marketplace and plugins. Items are added when concrete need arises; not committing to all of them.

## Pipeline gaps

| Item | Status | Notes |
|------|--------|-------|
| `/ticket-pipeline` step 7 — auto-commit | **Out of scope** | User decision: commit stays manual via skill `ticket-commit`. No orchestrator step. |
| `/ticket-pipeline` step 8 — auto-PR | **Out of scope** | User decision: PR stays manual via `gh pr create`. |
| `/imperium status` discoverability command | Backlog | List enabled agents, skills, MCP server health. |
| `mcp-doctor` skill | Backlog | Diagnose MCP token validity, server up/down. |
| `/pipeline-resume` command | Backlog | Resume from last STOP using `.imperium/runs/<ticket-id>/state.json`. State file already written by retry guard. |

## Planned chapters (themed agents)

Add a chapter when a real workflow gap is identified. Scaffold = new `plugins/ultramarines/agents/<name>.md` + lore note in README + optional `/ticket-pipeline` insertion.

| Chapter | Role | Trigger to scaffold |
|---------|------|---------------------|
| `space-wolves` | Exploratory dogfood (wild, instinct-driven QA) | When `dogfood` skill alone proves insufficient and we want a wrapping agent with persona |
| `grey-knights` | Auth / permission / RBAC specialist | When auth-heavy ticket lands and dark-angels security pass + apothecary impact aren't enough granularity |
| `imperial-fists` | Defensive testing fortress (failure-mode + chaos test) | When a ticket touches a critical surface that needs negative-path coverage |
| `salamanders` | UI / design review (artisans of the forge) | When design-system or visual-regression review needs to be a dedicated agent step |
| `iron-hands` | Refactor / performance optimization | When refactor tickets become common and need a separate doctrine from chapter-master's surgical-scope rule |

## Skill backlog

| Item | Trigger |
|------|---------|
| `mcp-doctor` skill | First time MCP server fails silently and user has to diagnose by hand |

## Infra

| Item | Decision |
|------|---------|
| Repo CI workflow (validate JSON, lint frontmatter, dry-run install.sh) | **Skipped** — user decision, low value at current scale |
| Pin SHA for external skills | **Done** (Apr 2026) — `external-skills.json` carries `commit` field; `update.sh --bump` advances pins |

## Done (recent)

- May 2026 — `primaris` v0.2.0 (Phase 1.5 — generic + `/insights`-driven). Cawl reads `~/.claude/usage-data/report.html` as primary input. User-data relocates to `$PRIMARIS_HOME` (default `~/.primaris/`). `growth-plan.template.md` ships in plugin; `bach-growth-plan.md` removed. Levels rubric gains per-level `Roadmap to Level N+1` subsections. Doctrine + README + manifest de-Bach. v0.1.0 install upgrade path: copy template → fill → run `/insights` → run `/level-check 7d`.
- May 2026 — `primaris` plugin Phase 1 (doctrine + meta loop). 7-tenet `PRIMARIS_DOCTRINE.md`, 3 playbooks (`ai-engineering-levels.md`, `bach-growth-plan.md`, `prime-directive.md`), `cawl` meta-analyst agent, `/level-check` command. Auto-fires after `/ticket-pipeline` Block 4 (graceful skip if not installed). Phase 2 (Prime Directive enforcement) next.
- Apr 2026 — `maestro` skill bundled (mobile E2E authoring with selectors/CI/GraalJS references + flow templates)
- Apr 2026 — `dark-angels` security review agent (Tier 1-6 threat model, halts pipeline on critical/high)
- Apr 2026 — Pin SHA for external skills + `update.sh --bump` flag
- Apr 2026 — `tech-priest` and `mobile-issue-reproducer` cite skill `maestro` per Tenet 7
- Apr 2026 — Codex Tenet 5 clarified: code EN, response bilingual user-lang + EN
- Apr 2026 — Lean pipeline (Option A) — 4 blocks with explicit STOP between (analyze / impl / gate / test)
- Apr 2026 — Iteration cap **enforced** via `scripts/check-iter.sh` + Codex Tenet 11 (state file at `.imperium/runs/<ticket-id>/state.json`, hard exit on cap)
- Apr 2026 — Per-run artifact log (`.imperium/runs/<ticket-id>/log.md`) auto-written by retry guard
- Apr 2026 — `astropath` skill + agent (external research with cited evidence — Tier 1-7 source ladder, Context7 MCP integration, `gh` CLI patterns) + Codex Tenet 12 external-research discipline
- Apr 2026 — librarian / inquisitor / techmarine reference astropath as on-demand research helper
