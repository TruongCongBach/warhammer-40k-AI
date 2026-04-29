#!/usr/bin/env bash
# Iteration cap guard for /ticket-pipeline retry loops.
#
# Reads + bumps a counter in .imperium/runs/<ticket-id>/state.json under
# key "<step>_iter". Exits 0 if next iter <= cap, exits 1 (with reason on
# stderr) if cap exceeded. Pipeline orchestrator MUST run this BEFORE every
# retry call (chapter-master, tech-priest) and treat non-zero exit as HALT.
#
# Usage:
#   bash scripts/check-iter.sh <ticket-id> <step> [cap]
#
# Defaults:
#   cap = 1   (Option A — fail-fast lean pipeline; bump to 2 only via explicit arg)
#
# Examples:
#   bash scripts/check-iter.sh MWL-123 chapter_master 1   # 0 OK, 1 cap-hit
#   bash scripts/check-iter.sh MWL-123 tech_priest        # cap defaults to 1
#
# Sub-commands:
#   bash scripts/check-iter.sh --reset MWL-123            # wipe state for ticket
#   bash scripts/check-iter.sh --show MWL-123             # print state.json

set -euo pipefail

REPO_ROOT="$(cd "$(dirname "$0")/.." && pwd)"

err() { printf "  \033[31m✗\033[0m %s\n" "$*" >&2; }

# ---- sub-commands ----
if [ "${1:-}" = "--reset" ]; then
  ticket="${2:?usage: --reset <ticket-id>}"
  rm -rf "${REPO_ROOT}/.imperium/runs/${ticket}"
  echo "state cleared for ${ticket}"
  exit 0
fi
if [ "${1:-}" = "--show" ]; then
  ticket="${2:?usage: --show <ticket-id>}"
  state="${REPO_ROOT}/.imperium/runs/${ticket}/state.json"
  if [ -f "$state" ]; then cat "$state"; else echo '{}'; fi
  exit 0
fi

# ---- main ----
TICKET="${1:?usage: $0 <ticket-id> <step> [cap]}"
STEP="${2:?usage: $0 <ticket-id> <step> [cap]}"
CAP="${3:-1}"

command -v jq >/dev/null || { err "jq missing — brew install jq"; exit 2; }

RUN_DIR="${REPO_ROOT}/.imperium/runs/${TICKET}"
STATE="${RUN_DIR}/state.json"
LOG="${RUN_DIR}/log.md"
mkdir -p "$RUN_DIR"
[ -f "$STATE" ] || echo '{}' > "$STATE"

KEY="${STEP}_iter"
CURRENT=$(jq -r --arg k "$KEY" '.[$k] // 0' "$STATE")
NEXT=$((CURRENT + 1))

if [ "$NEXT" -gt "$CAP" ]; then
  err "HALT — ${STEP} iteration cap ${CAP} exceeded (would be ${NEXT}/${CAP})"
  echo "- $(date -u +%Y-%m-%dT%H:%M:%SZ) ${STEP}: HALT cap=${CAP} attempted=${NEXT}" >> "$LOG"
  exit 1
fi

# Bump counter atomically
tmp="${STATE}.tmp"
jq --arg k "$KEY" --argjson v "$NEXT" '.[$k] = $v | .updated_at = (now | todate)' "$STATE" > "$tmp"
mv "$tmp" "$STATE"

echo "- $(date -u +%Y-%m-%dT%H:%M:%SZ) ${STEP}: iter ${NEXT}/${CAP}" >> "$LOG"
echo "OK ${STEP} iter ${NEXT}/${CAP}"
exit 0
