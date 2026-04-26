#!/usr/bin/env bash
# Imperium of Man — updater
# Pulls latest external skills + plugin marketplace.
set -euo pipefail

REPO_ROOT="$(cd "$(dirname "$0")/.." && pwd)"
AGENTS_DIR="${HOME}/.agents/skills"
SKILLS_JSON="${REPO_ROOT}/scripts/external-skills.json"

bold() { printf "\033[1m%s\033[0m\n" "$*"; }
ok()   { printf "  \033[32m✓\033[0m %s\n" "$*"; }
warn() { printf "  \033[33m⚠\033[0m %s\n" "$*"; }

bold "==> Updating marketplace repo (self)"
git -C "${REPO_ROOT}" pull --ff-only && ok "marketplace pulled"

bold "==> Updating external skills"
jq -r '.skills[].name' "${SKILLS_JSON}" | while read -r name; do
  target="${AGENTS_DIR}/${name}"
  if [ -d "${target}/.git" ]; then
    if git -C "${target}" pull --ff-only >/dev/null 2>&1; then
      ok "${name} updated"
    else
      warn "${name} pull failed (maybe sparse-checkout or detached) — manual check"
    fi
  else
    warn "${name} no .git — skip"
  fi
done

bold "==> Updating Claude plugins"
if command -v claude >/dev/null; then
  claude plugin marketplace update imperium-of-guilliman 2>/dev/null && ok "marketplace metadata refreshed"
fi

bold "==> Done."
