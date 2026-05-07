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
