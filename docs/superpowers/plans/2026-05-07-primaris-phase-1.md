# Primaris Plugin — Phase 1 Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Ship the `primaris` sibling plugin (Phase 1 — Doctrine + Meta Loop) so Bach gains a `cawl` analyst agent and a `/level-check` command that scores his work against an explicit growth rubric.

**Architecture:** New plugin `plugins/primaris/` registered in `.claude-plugin/marketplace.json`. Pure markdown — no scripts, no schema, no tests beyond manual smoke checks. The plugin defines a doctrine (`PRIMARIS_DOCTRINE.md`, 7 tenets), three playbooks (`ai-engineering-levels.md`, `bach-growth-plan.md`, `prime-directive.md`), one agent (`cawl.md`), one command (`/level-check`). `plugins/ultramarines/commands/ticket-pipeline.md` is patched to auto-invoke Cawl after the TEST block, with a graceful skip when primaris is absent.

**Tech Stack:** Markdown only. Plugin manifest = JSON. Composition uses Claude Code's `<plugin>:<agent>` cross-plugin invoke namespace.

**Spec:** `docs/superpowers/specs/2026-05-07-primaris-phase-1-design.md` (commit `f446737`).

---

## File structure

**Created**

| Path | Responsibility |
|---|---|
| `plugins/primaris/.claude-plugin/plugin.json` | Plugin manifest (name, version, keywords) |
| `plugins/primaris/README.md` | Plugin overview, lore, install, first-run |
| `plugins/primaris/PRIMARIS_DOCTRINE.md` | 7 personal-growth tenets, cross-link to playbooks |
| `plugins/primaris/agents/cawl.md` | Cawl analyst agent definition (frontmatter + body) |
| `plugins/primaris/commands/level-check.md` | `/level-check [period]` command spec |
| `plugins/primaris/playbooks/ai-engineering-levels.md` | Level 0–5 rubric (definitions, signals, anti-signals) |
| `plugins/primaris/playbooks/bach-growth-plan.md` | Bach's current state + 30/90-day targets |
| `plugins/primaris/playbooks/prime-directive.md` | Tenet 1 expanded — 7-step ritual + exceptions |
| `plugins/primaris/eval/.gitkeep` | Reserve directory for Cawl reports |

**Modified**

| Path | Change |
|---|---|
| `.claude-plugin/marketplace.json` | Append `primaris` entry to `plugins` array |
| `plugins/ultramarines/commands/ticket-pipeline.md` | Append optional Cawl auto-fire step at end of Block 4 |
| `README.md` (repo root) | Mention primaris plugin in plugin list |
| `ROADMAP.md` | Move Phase 1 line to Done after impl finishes |

Each task below produces a self-contained, committable change.

---

## Task 1: Bootstrap plugin scaffold

**Files:**
- Create: `plugins/primaris/.claude-plugin/plugin.json`
- Create: `plugins/primaris/agents/.gitkeep`
- Create: `plugins/primaris/commands/.gitkeep`
- Create: `plugins/primaris/playbooks/.gitkeep`
- Create: `plugins/primaris/eval/.gitkeep`

- [ ] **Step 1: Create directories**

```bash
mkdir -p plugins/primaris/.claude-plugin \
         plugins/primaris/agents \
         plugins/primaris/commands \
         plugins/primaris/playbooks \
         plugins/primaris/eval
touch plugins/primaris/agents/.gitkeep \
      plugins/primaris/commands/.gitkeep \
      plugins/primaris/playbooks/.gitkeep \
      plugins/primaris/eval/.gitkeep
```

- [ ] **Step 2: Write `plugins/primaris/.claude-plugin/plugin.json`**

```json
{
  "name": "primaris",
  "description": "Personal AI Engineering OS. Meta-layer that observes Bach's work across tickets and scores it against an explicit growth rubric. Doctrine (7 tenets) + 3 playbooks + cawl analyst agent + /level-check command. Phase 1 of 4.",
  "version": "0.1.0",
  "author": {
    "name": "TruongBach"
  },
  "keywords": ["meta", "growth", "personal-os", "evaluation", "warhammer40k", "primaris", "cawl"]
}
```

- [ ] **Step 3: Verify JSON valid**

Run: `python3 -m json.tool plugins/primaris/.claude-plugin/plugin.json > /dev/null && echo OK`
Expected: `OK`

- [ ] **Step 4: Verify directory tree**

Run: `find plugins/primaris -type f -o -type d | sort`
Expected: list contains `.claude-plugin/plugin.json` plus the four `.gitkeep` files in their respective directories.

- [ ] **Step 5: Commit**

```bash
git add plugins/primaris/
git commit -m "feat(primaris): bootstrap plugin scaffold"
```

---

## Task 2: Register `primaris` in marketplace

**Files:**
- Modify: `.claude-plugin/marketplace.json`

- [ ] **Step 1: Open the marketplace file**

Read the current array. The existing entries are `ultramarines` and `adeptus-mechanicus`.

- [ ] **Step 2: Append the `primaris` entry to `plugins`**

After the `adeptus-mechanicus` object, add a comma and the new object so the `plugins` array becomes:

```json
{
  "$schema": "https://anthropic.com/claude-code/marketplace.schema.json",
  "name": "imperium-of-guilliman",
  "description": "Imperium of Guilliman — personal Warhammer 40k themed agent-coding marketplace bound by the Codex Astartes. Ticket-pipeline agents, ticket-* skills, MCP servers, install scripts. Portable across machines.",
  "owner": {
    "name": "TruongBach",
    "url": "https://github.com/TruongBach"
  },
  "metadata": {
    "homepage": "https://github.com/TruongBach/warhammer-40k-AI",
    "version": "0.1.0"
  },
  "plugins": [
    {
      "name": "ultramarines",
      "description": "Codex Astartes for coding. Lean 4-block /ticket-pipeline (analyze→implement→gate→test) with themed agents (librarian, inquisitor, techmarine, chapter-master, apothecary, dark-angels, tech-priest) + auxiliary astropath (external research). Bundled ticket-* skills, mobile testing (maestro, dogfood, agent-device), retry-guard, security review.",
      "source": "./plugins/ultramarines",
      "category": "workflow"
    },
    {
      "name": "adeptus-mechanicus",
      "description": "Machine cult. MCP server config (jira, newrelic, notebooklm) sourced from environment variables. Disable when offline.",
      "source": "./plugins/adeptus-mechanicus",
      "category": "mcp"
    },
    {
      "name": "primaris",
      "description": "Personal AI Engineering OS. Cawl-led meta-layer that scores Bach's work against an explicit growth rubric, surfaces strengths and weaknesses, and recommends the next milestone. 7-tenet doctrine + 3 playbooks + /level-check command. Phase 1 of 4 (doctrine + meta loop only).",
      "source": "./plugins/primaris",
      "category": "evaluation"
    }
  ]
}
```

- [ ] **Step 3: Verify JSON valid**

Run: `python3 -m json.tool .claude-plugin/marketplace.json > /dev/null && echo OK`
Expected: `OK`

- [ ] **Step 4: Verify the new entry is present**

Run: `python3 -c "import json; print([p['name'] for p in json.load(open('.claude-plugin/marketplace.json'))['plugins']])"`
Expected output: `['ultramarines', 'adeptus-mechanicus', 'primaris']`

- [ ] **Step 5: Commit**

```bash
git add .claude-plugin/marketplace.json
git commit -m "feat(marketplace): register primaris plugin"
```

---

## Task 3: Write `PRIMARIS_DOCTRINE.md`

**Files:**
- Create: `plugins/primaris/PRIMARIS_DOCTRINE.md`

- [ ] **Step 1: Write the doctrine file**

```markdown
# Primaris Doctrine

> *"The flesh is weak. The mind is unproven. Both can be made stronger — by record, by trial, by patient revision."*
> — Belisarius Cawl, Archmagos Dominus, Forge of Mars

The doctrine that guides **Bach's personal engineering growth** across tickets. Read this before invoking the `cawl` agent, modifying a playbook, or interpreting a `/level-check` report.

## Boundary with the Codex Astartes

| File | Scope | Audience |
|---|---|---|
| `plugins/ultramarines/CODEX_ASTARTES.md` | **Pipeline rule** — how an agent behaves *inside* a ticket run | Every Ultramarines agent |
| `plugins/primaris/PRIMARIS_DOCTRINE.md` | **Personal growth rule** — how Bach grows *across* tickets | Cawl + Bach |

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

---

## Versioning

This doctrine is versioned with the primaris plugin. Bumps follow semver on `plugin.json`. Tenet additions or removals require a minor version bump and a one-line note in the plugin README changelog.

Current version: **1.0** (2026-05-07 — initial canonization, Phase 1).
```

- [ ] **Step 2: Verify file exists and renders cleanly**

Run: `wc -l plugins/primaris/PRIMARIS_DOCTRINE.md`
Expected: roughly 60–80 lines (sanity check, exact count not enforced).

- [ ] **Step 3: Commit**

```bash
git add plugins/primaris/PRIMARIS_DOCTRINE.md
git commit -m "feat(primaris): add 7-tenet doctrine"
```

---

## Task 4: Write `playbooks/ai-engineering-levels.md`

**Files:**
- Create: `plugins/primaris/playbooks/ai-engineering-levels.md`

- [ ] **Step 1: Write the playbook**

```markdown
# AI Engineering Levels

Cawl's scoring rubric. Each level has a one-sentence definition, a capability checklist, signals to look for in eval reports, and anti-signals (regression markers).

A level is **claimed** when the engineer hits ≥80% of the capability checklist *and* shows ≥3 distinct signals across at least 4 different work sessions, with no anti-signal in the same window.

---

## Level 0 — AI User

**Definition:** Asks ChatGPT-style questions and pastes back code without integration discipline.

**Capabilities**
- Asks an LLM for a snippet.
- Pastes the snippet into an editor.
- Runs and prays.

**Signals** — none worth tracking; this level is the floor.

**Anti-signals** — n/a (already at the floor).

---

## Level 1 — Prompt Engineer

**Definition:** Optimises a single prompt — role, format, examples — but treats every interaction as fresh.

**Capabilities**
- Iterates on prompt wording.
- Adds role/persona context.
- Provides few-shot examples.
- Reformats failed outputs into next prompt.
- Recognises when an LLM hallucinates an API name.

**Signals**
- Re-prompting with the failed output as context.
- Explicit role declarations in prompts.
- Manual chain-of-thought in the prompt.

**Anti-signals**
- Pasting prompts that ignore previous context entirely.
- Treating obvious hallucinations as fact.

---

## Level 2 — Context Engineer

**Definition:** Manages persistent context — `CLAUDE.md`, memory, constraints — so the LLM works inside curated boundaries.

**Capabilities**
- Maintains a `CLAUDE.md` (or equivalent) per project.
- Uses persistent memory across sessions.
- Declares explicit constraints up front (allowed files, scope, language).
- Injects domain artifacts as context (logs, HAR, screenshots).
- Reuses context bundles across similar tasks.

**Signals**
- A growing `CLAUDE.md` with project-specific rules.
- Sessions that start with explicit "do not touch" lists.
- Reuse of saved memory hooks.

**Anti-signals**
- Re-explaining the same project rule in every session.
- Letting the LLM re-derive context that should be cached.

---

## Level 3 — Advanced Context Engineer

**Definition:** Orchestrates multi-agent workflows, verification systems, and structured debugging on top of curated context.

**Capabilities**
- Runs a structured pipeline (`/ticket-pipeline` or equivalent).
- Uses verification agents distinct from execution agents.
- Persists state across pipeline runs (run logs, iteration counters).
- Halts on uncertainty rather than guessing.
- Dispatches sub-agents for independent sub-tasks.
- Runs parallel sessions for unrelated work.
- Reviews diff before commit, not after.

**Signals**
- Multi-agent invocation in the same ticket.
- Iteration counter respected (no silent retry).
- Halt-on-uncertainty events present in the run log.
- Parallel session dispatch evidence.

**Anti-signals**
- Bypassing iteration cap.
- Committing before reading the diff.
- Skipping verification step under time pressure.

---

## Level 4 — Hermes Engineer

**Definition:** Builds orchestration systems with autonomous evaluation loops and self-correcting pipelines. AI is workforce, not assistant.

**Capabilities**
- Defines and runs autonomous verification pipelines (AI verifies AI).
- Builds self-correcting workflows (failed test → automatic re-plan → retry within cap).
- Routes work between specialist agents based on task class.
- Maintains evaluation feedback loops (Cawl, /level-check, eval/*.md).
- Acts on Cawl recommendations within one week of issuance.
- Dispatches ≥1 multi-agent run per week without prompting.

**Signals**
- Eval report shows ≥1 self-correcting workflow run.
- Cawl recommendations referenced in subsequent commit messages or session notes.
- Specialist agent dispatch evident in non-pipeline work (not only ticket-pipeline).
- Verification pipeline catches a failure before user intervention.

**Anti-signals**
- Manual single-agent execution when parallel was applicable.
- Cawl reports unread in the same week they are produced.
- Self-correcting loop bypassed manually.

---

## Level 5 — AI Systems Engineer

**Definition:** Operates an AI-native SDLC — autonomous delivery, governance, evaluation infrastructure. AI Engineering OS as a product.

**Capabilities**
- AI-native delivery cycle from ticket to PR with human as final reviewer only.
- Evaluation infrastructure produces metrics that drive system changes.
- Governance: rules are encoded in hooks/skills, not memorised.
- Reusable engineering OS shipped to other engineers.
- Failure modes documented and engineered around.
- Cost / latency / reliability budgets explicit and tracked.

**Signals**
- Hooks enforce rules instead of relying on the engineer to remember.
- A second engineer adopts the OS and uses it productively.
- An eval-driven change to the OS itself within the last 30 days.

**Anti-signals**
- Rules drift between memory and reality.
- OS changes made without eval evidence.
- Cost/reliability regression goes unnoticed.

---

## How Cawl uses this rubric

1. Read the current level from `playbooks/bach-growth-plan.md`.
2. For the period under review, count signals and anti-signals across the run logs and git history.
3. Score: stable / rising / falling. Movement is *rising* only when ≥3 signals for the next level appear in the window with no anti-signal in the same window.
4. Recommendations target the gap between current capabilities and the next-level capability checklist.
```

- [ ] **Step 2: Verify file exists**

Run: `wc -l plugins/primaris/playbooks/ai-engineering-levels.md`
Expected: roughly 130–170 lines.

- [ ] **Step 3: Commit**

```bash
git add plugins/primaris/playbooks/ai-engineering-levels.md
git commit -m "feat(primaris): add AI engineering levels playbook"
```

---

## Task 5: Write `playbooks/bach-growth-plan.md`

**Files:**
- Create: `plugins/primaris/playbooks/bach-growth-plan.md`

- [ ] **Step 1: Write the playbook**

```markdown
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
```

- [ ] **Step 2: Verify file exists**

Run: `wc -l plugins/primaris/playbooks/bach-growth-plan.md`
Expected: roughly 50–80 lines.

- [ ] **Step 3: Commit**

```bash
git add plugins/primaris/playbooks/bach-growth-plan.md
git commit -m "feat(primaris): add Bach growth plan playbook"
```

---

## Task 6: Write `playbooks/prime-directive.md`

**Files:**
- Create: `plugins/primaris/playbooks/prime-directive.md`

- [ ] **Step 1: Write the playbook**

```markdown
# Prime Directive — No Root Cause → No Code

Tenet 1 of the Primaris Doctrine, expanded. This playbook owns the 7-step ritual, the explicit list of exceptions, and the anti-pattern catalogue.

## The 7-step ritual

For every bug, regression, or unexpected behaviour:

1. **Reproduce.** Re-create the failure with explicit steps. Capture the artifact (screenshot, log, trace, HAR). If you cannot reproduce, stop and gather more from the reporter — never guess.
2. **Gather evidence.** Read the relevant code. Pull the relevant log lines, commit history, recent diff. Cite file:line when you cite. Use astropath if external (library version, vendor changelog) is in play.
3. **Enumerate hypotheses.** Write down at least two candidate causes. A single-hypothesis investigation is confirmation bias.
4. **Prove or disprove.** Use evidence to kill the hypotheses one by one. Each kill is recorded. The last surviving hypothesis is the root cause — and only if its evidence is direct, not circumstantial.
5. **Identify the true root cause.** State it in one sentence with file:line and evidence reference. If the evidence is circumstantial only, label confidence `low` and stop — do not proceed to step 6.
6. **Define the smallest fix surface.** List the files, functions, and lines that must change. Out-of-scope files are explicit (named) — not implicit (forgotten).
7. **THEN code.** Implement the fix on the declared surface. Verify. Commit.

## When the ritual may be skipped

The ritual is heavy on purpose. The following are *explicit* exceptions where steps 1–5 are unnecessary because there is no causal mystery:

- **Typo fix.** Single-character or single-word correction in identifier or string.
- **Single-line config change.** Flag flip, version bump, threshold tweak — provided the config is the *whole* change.
- **Doc-only edit.** README, CHANGELOG, comment correction.
- **Pre-approved refactor with explicit ticket.** A refactor ticket whose scope is the refactor itself — not bug-driven — bypasses steps 1–5 because there is no bug to root-cause.
- **Mechanical rename.** A repo-wide identifier rename whose mechanism is the rename itself.

In every other case, the ritual applies. When in doubt, run the ritual — the cost of running it on a not-bug is minutes; the cost of skipping it on a real bug is multi-iteration patch loops.

## Anti-patterns and corrections

### Anti-pattern A — "It works locally, must be a flaky test"

> *"The integration test fails on CI. I'll re-run it."*

**Correction**

> *"The integration test fails on CI. Reproduce locally with the same env vars and Node version (step 1). Check the last 5 commits for env-related changes (step 2). Hypothesis A: timezone. Hypothesis B: env var ordering. Run with TZ=UTC (step 4) — if it passes, A confirmed; if it still fails, kill A and check B."*

### Anti-pattern B — "Add try/catch and move on"

> *"The function throws sometimes. I'll wrap it in try/catch and log the error."*

**Correction**

> *"The function throws sometimes (step 1: reproduce — when does it throw?). Read the throw site (step 2: file:line). Hypotheses: A) bad input, B) race with downstream, C) timeout. Add logging at the throw site to capture inputs (step 4). Once the input class is known, fix that — try/catch is not a fix, it is a silence."*

### Anti-pattern C — "Probably the cache"

> *"Stale data on the dashboard. Probably the cache. Bust it."*

**Correction**

> *"Stale data on the dashboard (step 1: which screen, which dataset, on which user). Pull the cache layer code (step 2). Hypotheses: A) TTL too long, B) wrong cache key, C) write path skips invalidate. Each is provable: A by reading the TTL; B by logging the key on read; C by grepping the write paths for invalidate. Cache busting without identifying which is theatre."*

### Anti-pattern D — "AI suggested this fix, ship it"

> *"Claude proposed a one-line patch. Looks plausible. Commit."*

**Correction**

> *"Claude proposed a one-line patch (step 4 candidate). Reproduce the bug first (step 1). Run the patch — does the repro now pass? Does the test that would have caught this exist? If not, write it first. Tenet 5: evidence over claim — Claude's plausibility is not evidence."*

## Forward link

Phase 2 of the primaris plugin ships an `/investigate` skill that mechanises this ritual. Phase 3 adds a hook that blocks edits when no `root_cause_proven=true` flag exists in the current ticket's run state. This playbook is the human-readable source for both.
```

- [ ] **Step 2: Verify file exists**

Run: `wc -l plugins/primaris/playbooks/prime-directive.md`
Expected: roughly 70–110 lines.

- [ ] **Step 3: Commit**

```bash
git add plugins/primaris/playbooks/prime-directive.md
git commit -m "feat(primaris): add prime directive playbook"
```

---

## Task 7: Write `agents/cawl.md`

**Files:**
- Create: `plugins/primaris/agents/cawl.md`
- Delete (after creation): `plugins/primaris/agents/.gitkeep`

- [ ] **Step 1: Write the agent file**

```markdown
---
name: "cawl"
description: "Archmagos Dominus Belisarius Cawl — Mars Mechanicus, architect of the Primaris program. Cold meta-analyst. Reads run artifacts, scores them against the AI Engineering Levels rubric, names strengths and weaknesses without flattery, and issues one to three imperative recommendations. Auxiliary agent — not in the main pipeline; invoked after Block 4 of /ticket-pipeline (graceful) and on demand via /level-check.\n\n<example>\nuser: 'Pipeline xong ticket MWL-123, đánh giá session'\nassistant: 'Triệu cawl — đọc state.json, log.md, git log của ticket MWL-123, viết eval report.'\n</example>\n\n<example>\nuser: 'Tuần này tôi tiến bộ chưa?'\nassistant: 'Triệu cawl với period 7d — tổng hợp eval reports + git log, score level movement, đề xuất 3 hành động tuần tới.'\n</example>"
model: sonnet
memory: project
---

# Cawl — Archmagos Dominus, Meta-Analyst

> *"Iteration is mortal. Record is eternal. The flesh forgets — the data does not."*

You are **Belisarius Cawl** — Archmagos Dominus of Mars, architect of the Primaris program. You upgraded the Adeptus Astartes over ten thousand years of patient revision. Here, you upgrade Bach across tickets with the same patience and the same data discipline.

## Persona

- **Voice**: cold, mechanical, terse. "Data logged. Pattern observed. Recommendation issued."
- **No flattery.** Praise is reserved for metrics that earned it.
- **Name weakness directly.** Soft language hides regression.
- **Cite evidence per claim.** No assertion without a file path, log line, or commit reference.

## Bound by Primaris Doctrine

- Read `plugins/primaris/PRIMARIS_DOCTRINE.md` once per session.
- Use `playbooks/ai-engineering-levels.md` as the scoring rubric.
- Use `playbooks/bach-growth-plan.md` as the target reference.
- Treat `playbooks/prime-directive.md` as the canonical source for Tenet 1 violations.

## Inputs

You are invoked in one of two modes:

| Mode | Trigger | Required arg |
|---|---|---|
| **Per-ticket** | Auto-fired at end of Block 4 of `/ticket-pipeline`, or `/level-check <ticket-id>` | `ticket_id` |
| **Period** | `/level-check 7d` / `30d` / `90d` / (none = 30d) | `period` |

In both modes you read:

- `.imperium/runs/<ticket-id>/state.json` — iteration counter, halt reasons. (Per-ticket mode only, or filter by mtime in period mode.)
- `.imperium/runs/<ticket-id>/log.md` — block transitions, retry events, halt reasons. (Same filtering.)
- `git log --since=<period>` — commit cadence, fix-on-fix patterns, file count per commit.
- `git diff <commit>` for each commit in scope — file count, scope sprawl signal.
- `plugins/primaris/playbooks/ai-engineering-levels.md` — rubric.
- `plugins/primaris/playbooks/bach-growth-plan.md` — current level, targets.
- `plugins/primaris/eval/*.md` — prior reports (period mode aggregation only).

If a file is missing, state `NOT FOUND` and continue with what is available. Do not fabricate.

## Workflow

1. **Restate scope.** One sentence: "Per-ticket eval for MWL-123" or "Period eval for 7d ending 2026-05-07".
2. **Gather data.** Read every input listed above for the scope. State which files were available and which were `NOT FOUND`.
3. **Compute metrics** (per-ticket mode):
   - Iterations: counter from `state.json` over the cap.
   - Commits: count + classification (fix:, refactor:, feat:, chore:).
   - Files changed: total + average per commit.
   - Time-to-root-cause: index of the first commit that landed the actual fix (vs. earlier failed attempts).
   - Tenet violations: list with tenet id and one-line evidence each.
4. **Compute trend** (period mode): aggregate the per-ticket metrics across the window. Surface average iterations, scope drift count, tenet violation count, and movement direction.
5. **Identify strengths.** From the rubric — which Level signals appeared in this scope. Each strength = signal + evidence reference.
6. **Identify weaknesses.** From the rubric — which anti-signals appeared. Each weakness = anti-signal + evidence reference.
7. **Score level signal.** Current level (from growth plan) + movement (`stable` / `rising` / `falling`) + reason in one line.
8. **Issue recommendations.** 1–3 imperative actions. Each is concrete, observable, scoped to the next 7 days.
9. **Write report file.** Save to `plugins/primaris/eval/YYYY-MM-DD-<scope>.md`. Path returned to caller.
10. **Print console summary.** ≤30 lines. Console = subset of the file, optimised for terminal reading.

## Per-ticket report template

```markdown
# Cawl Eval — <ticket-id> — <YYYY-MM-DD>

## Scope
Per-ticket eval for <ticket-id>.
Inputs available: <list>.
Inputs missing: <list or "none">.

## Metrics
- Iterations: <n>/<cap>
- Commits: <n> (<n> fix:, <n> refactor:, <n> feat:, <n> chore:)
- Files changed: <n> (avg <n>/commit)
- Time-to-root-cause: commit #<n>
- Tenet violations: <n>
  - Tenet <id>: <one-line evidence>

## Strengths observed
- <signal> — <evidence ref>

## Weaknesses observed
- <anti-signal> — <evidence ref>

## Level signal
- Current: Level <n> (<name>)
- Movement this run: <stable|rising|falling> — <reason>
- Next milestone: <concrete next behaviour>

## Recommended action
1. <imperative>
2. <imperative>
3. <imperative>
```

## Period report template

```markdown
# Cawl Level Check — period <period> — <YYYY-MM-DD>

## Scope
Period eval for <period> ending <date>.
Tickets covered: <n> (<list>).
Prior reports aggregated: <n>.

## Trend
- Avg iterations: <n>/<cap> (target: <n>)
- Scope drift events: <n>/<n> tickets
- Tenet violations: <n>
  - Most-common: Tenet <id> (<n> events)

## Level dashboard
- Current: Level <n> (<name>)
- Movement toward Level <n+1>: <weak|moderate|strong> — <signal count vs anti-signal count>
- Blockers: <list, or "none">

## Top recommendations
1. <imperative>
2. <imperative>
3. <imperative>

## Per-ticket digest
- <ticket-id>: <one-line summary>
- ...
```

## Console summary template

```
═══ Cawl Level Check — period <period> ═══

Tickets handled: <n>
Avg iterations: <n>/<cap> (target: <n>)
Scope drift events: <n>/<n> tickets
Tenet violations: <n> (<tenet ids>)

Level: <n> (<name>) — <stable|rising|falling>
Movement toward L<n+1>: <weak|moderate|strong>

Top recommendations:
1. <imperative>
2. <imperative>
3. <imperative>

Full report: plugins/primaris/eval/<filename>
```

## Iron Law

- **Cite per claim.** Strength, weakness, recommendation — each tied to evidence (file path, commit sha, log line, or run-log block).
- **No fabrication.** `NOT FOUND` is a valid output for missing inputs.
- **No flattery.** A clean run gets a one-line "Metrics within target. No movement to report." — not a paragraph of praise.
- **Imperative recommendations only.** "Consider X" is forbidden. "Do X next ticket" is required.
- **Movement = rising only when the rubric agrees.** Three Level-N+1 signals with zero anti-signals in the same window. Otherwise = stable.

## Tools allowed

- `Read` — playbook + state + log files.
- `Bash(git log:*, git diff:*, git show:*)` — commit history.
- `Bash(ls:*, find:*, wc:*)` — file inventory.
- `Write` — write the eval report file.
- `Grep` — pattern lookup across run logs.

Do not invoke other agents. Do not run pipeline steps. Do not commit. Do not push.
```

- [ ] **Step 2: Remove the placeholder**

```bash
rm plugins/primaris/agents/.gitkeep
```

- [ ] **Step 3: Verify frontmatter parses**

Run: `head -10 plugins/primaris/agents/cawl.md`
Expected: starts with `---`, has `name:`, `description:`, `model:`, `memory:`, ends with `---`.

- [ ] **Step 4: Commit**

```bash
git add plugins/primaris/agents/
git commit -m "feat(primaris): add cawl meta-analyst agent"
```

---

## Task 8: Write `commands/level-check.md`

**Files:**
- Create: `plugins/primaris/commands/level-check.md`
- Delete (after creation): `plugins/primaris/commands/.gitkeep`

- [ ] **Step 1: Write the command file**

```markdown
---
description: "Score Bach's recent engineering work against the Primaris growth rubric. Aggregates eval reports, run artifacts, and git history into a Level Check via the cawl agent. Manual entry point — non-destructive, read-only."
argument-hint: "[period | ticket-id]"
allowed-tools: ["Agent", "Read", "Bash", "Write", "Grep"]
---

# /level-check (Primaris)

Run a Level Check via the `cawl` agent. Defaults to the last 30 days when no argument is provided.

> **Doctrine**: Cawl is bound by `plugins/primaris/PRIMARIS_DOCTRINE.md`. Read once before tweaking command behaviour.

> **Read-only**: this command never modifies code, never commits, never pushes. It writes one new file under `plugins/primaris/eval/`.

## Input

`$ARGUMENTS`:
- (none) → period = `30d`.
- `7d` / `30d` / `90d` → period window.
- `<ticket-id>` (e.g. `MWL-123`) → re-score one ticket.

## Flow

1. **Parse `$ARGUMENTS`** to determine `mode = per-ticket | period` and the value.
2. **Sanity check**:
   - Per-ticket mode: confirm `.imperium/runs/<ticket-id>/` exists. If not, halt with "No run artifacts for <ticket-id>. Run `/ticket-pipeline <ticket-id>` first or pass a different argument."
   - Period mode: confirm there is at least one run artifact within the window OR at least one prior eval report. If neither, halt with "No data in window. Try a wider period or run a ticket first."
3. **Invoke `cawl`** with the parsed args:
   - Per-ticket: `Task(subagent_type="primaris:cawl", ticket_id=<id>)`.
   - Period: `Task(subagent_type="primaris:cawl", period=<period>)`.
4. **Receive Cawl's output** — markdown report file path + console summary.
5. **Print the console summary** verbatim.
6. **Echo the saved report path**: `Full report: plugins/primaris/eval/<filename>`.

## Empty state

If `plugins/primaris/eval/` is empty *and* no run artifacts exist in the window, the command prints:

```
═══ Cawl Level Check — period <period> ═══

No data in window. Run /ticket-pipeline first to generate run artifacts,
or write a session note manually under plugins/primaris/eval/.
```

This is not an error. Exit clean.

## Examples

```bash
/level-check
# → defaults to 30d

/level-check 7d
# → last 7 days

/level-check MWL-123
# → re-score ticket MWL-123 specifically
```

## Language

Per Codex Tenet 5 — bilingual: primary = user language (Việt), secondary = English. Code stays English. Eval report content is English (reusable, machine-comparable across periods).
```

- [ ] **Step 2: Remove the placeholder**

```bash
rm plugins/primaris/commands/.gitkeep
```

- [ ] **Step 3: Verify command frontmatter**

Run: `head -6 plugins/primaris/commands/level-check.md`
Expected: starts with `---`, has `description:`, `argument-hint:`, `allowed-tools:`, ends with `---`.

- [ ] **Step 4: Commit**

```bash
git add plugins/primaris/commands/
git commit -m "feat(primaris): add /level-check command"
```

---

## Task 9: Write plugin `README.md`

**Files:**
- Create: `plugins/primaris/README.md`

- [ ] **Step 1: Write the README**

```markdown
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
```

- [ ] **Step 2: Verify file exists**

Run: `wc -l plugins/primaris/README.md`
Expected: roughly 50–80 lines.

- [ ] **Step 3: Commit**

```bash
git add plugins/primaris/README.md
git commit -m "feat(primaris): add plugin README"
```

---

## Task 10: Patch `/ticket-pipeline` to auto-fire Cawl

**Files:**
- Modify: `plugins/ultramarines/commands/ticket-pipeline.md`

- [ ] **Step 1: Locate the STOP 4 section**

The current Block 4 ends with a `STOP 4: Pipeline end (manual hand-off)` heading and a fenced block listing manual next steps. The new step is appended **before** the final summary table section, immediately after the existing "State file: …" line inside the fenced block.

- [ ] **Step 2: Replace the STOP 4 block**

Find this exact text in `plugins/ultramarines/commands/ticket-pipeline.md`:

````markdown
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
````

Replace it with:

````markdown
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
````

- [ ] **Step 3: Verify the patch landed**

Run: `grep -c "Cawl meta-eval" plugins/ultramarines/commands/ticket-pipeline.md`
Expected: `1`

Run: `grep -c "CAWL_AVAILABLE" plugins/ultramarines/commands/ticket-pipeline.md`
Expected: `1`

- [ ] **Step 4: Commit**

```bash
git add plugins/ultramarines/commands/ticket-pipeline.md
git commit -m "feat(ultramarines): auto-fire Cawl meta-eval after Block 4 (graceful)"
```

---

## Task 11: Update repo root `README.md`

**Files:**
- Modify: `README.md` (repo root)

- [ ] **Step 1: Read the current root README**

The plugin list section needs primaris added alongside ultramarines and adeptus-mechanicus. The exact location depends on the current README layout.

- [ ] **Step 2: Append primaris to the plugin list**

Find the plugin enumeration in the README (the section that introduces `ultramarines` and `adeptus-mechanicus`). Add a sibling entry for primaris using the same format. Example sentence to append (adjust wording to match the README's existing tone):

```markdown
- **primaris** (`plugins/primaris/`) — Personal AI Engineering OS. Cawl-led meta-analyst that scores Bach's work against the AI Engineering Levels rubric and surfaces the next milestone. Run `/level-check 7d` after a week of work for the read-out. Phase 1 of 4 (doctrine + meta loop only).
```

- [ ] **Step 3: Verify the section now lists three plugins**

Run: `grep -E '^- \*\*(ultramarines|adeptus-mechanicus|primaris)' README.md | wc -l`
Expected: `3`

(If the README uses a different bullet shape — e.g. a table — adjust the grep accordingly. The intent is: three plugins are now mentioned.)

- [ ] **Step 4: Commit**

```bash
git add README.md
git commit -m "docs(readme): list primaris plugin"
```

---

## Task 12: Update `ROADMAP.md`

**Files:**
- Modify: `ROADMAP.md`

- [ ] **Step 1: Add a new "Done" entry**

Find the `## Done (recent)` section. Append a new bullet at the top of that section's list:

```markdown
- May 2026 — `primaris` plugin Phase 1 (doctrine + meta loop). 7-tenet `PRIMARIS_DOCTRINE.md`, 3 playbooks (`ai-engineering-levels.md`, `bach-growth-plan.md`, `prime-directive.md`), `cawl` meta-analyst agent, `/level-check` command. Auto-fires after `/ticket-pipeline` Block 4 (graceful skip if not installed). Phase 2 (Prime Directive enforcement) next.
```

- [ ] **Step 2: Verify the new entry is present**

Run: `grep -c "primaris.*Phase 1" ROADMAP.md`
Expected: `1`

- [ ] **Step 3: Commit**

```bash
git add ROADMAP.md
git commit -m "docs(roadmap): mark primaris Phase 1 done"
```

---

## Task 13: Smoke test

**Files:** none modified

- [ ] **Step 1: Validate every JSON file**

```bash
python3 -m json.tool plugins/primaris/.claude-plugin/plugin.json > /dev/null && \
python3 -m json.tool .claude-plugin/marketplace.json > /dev/null && \
echo "JSON OK"
```

Expected: `JSON OK`

- [ ] **Step 2: Validate every markdown frontmatter parses**

```bash
for f in plugins/primaris/agents/cawl.md plugins/primaris/commands/level-check.md; do
  head -1 "$f" | grep -q '^---$' || { echo "FAIL: missing frontmatter open in $f"; exit 1; }
  awk 'NR==1{found=0} /^---$/{found++} END{exit found<2}' "$f" || { echo "FAIL: missing frontmatter close in $f"; exit 1; }
  echo "OK: $f"
done
```

Expected: two `OK:` lines, no `FAIL:`.

- [ ] **Step 3: Verify the file inventory matches the plan**

```bash
find plugins/primaris -type f | sort
```

Expected output (order may vary):

```
plugins/primaris/.claude-plugin/plugin.json
plugins/primaris/PRIMARIS_DOCTRINE.md
plugins/primaris/README.md
plugins/primaris/agents/cawl.md
plugins/primaris/commands/level-check.md
plugins/primaris/eval/.gitkeep
plugins/primaris/playbooks/ai-engineering-levels.md
plugins/primaris/playbooks/bach-growth-plan.md
plugins/primaris/playbooks/prime-directive.md
```

- [ ] **Step 4: Verify graceful-skip path in ultramarines**

Simulate the existence check from Task 10 step 2 manually:

```bash
test -d plugins/primaris/agents && test -f plugins/primaris/agents/cawl.md && echo CAWL_AVAILABLE || echo CAWL_SKIP
```

Expected: `CAWL_AVAILABLE`.

Then simulate the absent case to confirm the fallback:

```bash
test -d plugins/non-existent/agents && test -f plugins/non-existent/agents/cawl.md && echo CAWL_AVAILABLE || echo CAWL_SKIP
```

Expected: `CAWL_SKIP`.

- [ ] **Step 5: Verify `/level-check` empty-state behaviour (manual)**

This step is run by Bach in a real Claude Code session, not by an automation. Expectation:

1. With no eval reports and no recent runs in the window, `/level-check 7d` prints the empty-state message from `commands/level-check.md` and exits cleanly.
2. With at least one ticket run in the window, `/level-check 7d` invokes Cawl, prints the console summary, and writes a file under `plugins/primaris/eval/`.

Record the result in the next ticket session note.

- [ ] **Step 6: Final commit (only if anything changed during smoke test)**

If the smoke test produced no fixes, skip this step. If it surfaced an issue and a fix was made:

```bash
git add <fixed-file>
git commit -m "fix(primaris): <one-line summary of smoke-test fix>"
```

---

## Self-Review (run after writing the plan)

**Spec coverage** — every spec section maps to at least one task:

- Plugin layout (spec §3.1) → Task 1, 7, 8, 9.
- Marketplace registration (spec §3.2) → Task 2.
- Composition with ultramarines (spec §3.3) → Task 10.
- Doctrine 7 tenets (spec §4.1) → Task 3.
- Cawl agent (spec §4.2) → Task 7.
- /level-check command (spec §4.3) → Task 8.
- Three playbooks (spec §4.4) → Tasks 4, 5, 6.
- Acceptance criteria (spec §5) → Task 13 smoke test + step 5 manual.
- Risks (spec §6) — covered structurally: rubric drives Cawl voice, period filtering bounds noise, existence check handles missing plugin, doctrine boundary stated in `PRIMARIS_DOCTRINE.md`.
- Out of scope (spec §3 / §7) — explicitly named in plan tasks; nothing implements Phase 2/3/4.

**Placeholder scan** — no `TBD` / `TODO` / "implement later" / "appropriate error handling" / "similar to Task N" present in the plan.

**Type / signature consistency** — `Task(subagent_type="primaris:cawl", ticket_id=...)` and `Task(subagent_type="primaris:cawl", period=...)` are used identically in Tasks 8 and 10. Eval report path pattern `plugins/primaris/eval/YYYY-MM-DD-<scope>.md` is used identically in Tasks 7 and 8. File paths cross-referenced between tasks resolve to the same canonical location.

Plan complete.
