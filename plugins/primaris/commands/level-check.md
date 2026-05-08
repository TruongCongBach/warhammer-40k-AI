---
description: "Score the engineer's recent work against the Primaris growth rubric. Reads Claude Code /insights report (~/.claude/usage-data/report.html) plus optional ticket-pipeline run artifacts and prior eval reports. Manual entry point — non-destructive, read-only."
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

1. **Resolve `PRIMARIS_HOME`.** Default `~/.primaris`. Honor `$PRIMARIS_HOME` if exported.

   ```bash
   PRIMARIS_HOME="${PRIMARIS_HOME:-$HOME/.primaris}"
   ```

2. **Check `~/.claude/usage-data/report.html`.**

   ```bash
   REPORT="$HOME/.claude/usage-data/report.html"
   if [ ! -f "$REPORT" ]; then
     echo "No /insights report at $REPORT."
     echo "Run /insights in any Claude Code session, then re-run /level-check."
     exit 0
   fi
   AGE_DAYS=$(( ( $(date +%s) - $(stat -f %m "$REPORT" 2>/dev/null || stat -c %Y "$REPORT") ) / 86400 ))
   if [ "$AGE_DAYS" -gt 7 ]; then
     echo "Report is stale ($AGE_DAYS days old). Run /insights to refresh, then re-run /level-check."
     exit 0
   fi
   ```

3. **Check `$PRIMARIS_HOME/growth-plan.md`.**

   ```bash
   GROWTH="$PRIMARIS_HOME/growth-plan.md"
   if [ ! -f "$GROWTH" ]; then
     echo "WARNING: no growth plan at $GROWTH."
     echo "Cawl will use defaults from playbooks/growth-plan.template.md."
     echo "Run init flow to personalise (see plugin README)."
   fi
   ```

4. **Parse `$ARGUMENTS`** to determine `mode = period | per-ticket` and the value.
   - `(empty)` → `period=30d`.
   - `7d` / `30d` / `90d` → `period=<value>`.
   - matches `^[A-Z]+-[0-9]+$` (e.g. `MWL-123`) → `mode=per-ticket`, value = ticket id.
5. **(Per-ticket mode only)** Confirm `.imperium/runs/<ticket-id>/` exists. If not, halt with: `No run artifacts for <ticket-id>. Run /ticket-pipeline <ticket-id> first or pass a different argument.` Exit clean.
6. **Invoke `cawl`** with the parsed args:
   - Period: `Task(subagent_type="primaris:cawl", period="<period>", report_path="$REPORT", primaris_home="$PRIMARIS_HOME")`.
   - Per-ticket: `Task(subagent_type="primaris:cawl", ticket_id="<id>", report_path="$REPORT", primaris_home="$PRIMARIS_HOME")`.
7. **Receive Cawl's output** — markdown report file path (under `$PRIMARIS_HOME/eval/`) + console summary.
8. **Print the console summary** verbatim.
9. **Echo the saved report path**: `Full report: $PRIMARIS_HOME/eval/<filename>`.

## Empty state

This command exits cleanly (not as an error) in two situations:

1. `~/.claude/usage-data/report.html` is missing — user has not run `/insights` yet. Output:

   ```
   No /insights report at ~/.claude/usage-data/report.html.
   Run /insights in any Claude Code session, then re-run /level-check.
   ```

2. The report exists but `mtime` is older than 7 days. Output:

   ```
   Report is stale (<N> days old). Run /insights to refresh, then re-run /level-check.
   ```

In either case the command exits without invoking Cawl. No file is written.

A third soft case: `$PRIMARIS_HOME/growth-plan.md` is missing. The command emits a one-line warning and proceeds — Cawl falls back to template defaults but eval quality is reduced. The user is invited to run the init flow (see plugin README) to personalise.

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

Per Codex Tenet 5 — bilingual: primary = user language, secondary = English. Code stays English. Eval report content is English (reusable, machine-comparable across periods).
