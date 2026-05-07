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
