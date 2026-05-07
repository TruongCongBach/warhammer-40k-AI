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
