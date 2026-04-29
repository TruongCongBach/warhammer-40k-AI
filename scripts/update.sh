#!/usr/bin/env bash
# Imperium of Guilliman — updater
# Default: re-checkout pinned commit for each external skill (NO upstream pull).
# Usage:
#   ./scripts/update.sh           — sync local clones to pinned commits in external-skills.json
#   ./scripts/update.sh --bump    — fetch upstream HEAD for every skill, rewrite external-skills.json with new SHAs
set -euo pipefail

export GIT_TERMINAL_PROMPT=0

REPO_ROOT="$(cd "$(dirname "$0")/.." && pwd)"
AGENTS_DIR="${HOME}/.agents/skills"
REPOS_DIR="${AGENTS_DIR}/.repos"
SKILLS_JSON="${REPO_ROOT}/scripts/external-skills.json"

bold() { printf "\033[1m%s\033[0m\n" "$*"; }
ok()   { printf "  \033[32m✓\033[0m %s\n" "$*"; }
warn() { printf "  \033[33m⚠\033[0m %s\n" "$*"; }
err()  { printf "  \033[31m✗\033[0m %s\n" "$*" >&2; }

MODE="sync"
if [ "${1:-}" = "--bump" ]; then
  MODE="bump"
fi

bold "==> Updating marketplace repo (self)"
git -C "${REPO_ROOT}" pull --ff-only && ok "marketplace pulled"

if [ "${MODE}" = "bump" ]; then
  bold "==> Bumping pinned commits to upstream HEAD"
  command -v jq >/dev/null || { err "jq missing — brew install jq"; exit 1; }
  tmp=$(mktemp)
  cp "${SKILLS_JSON}" "${tmp}"

  jq -c '.skills[]' "${SKILLS_JSON}" | while read -r entry; do
    name=$(echo "$entry" | jq -r '.name')
    repo=$(echo "$entry" | jq -r '.repo')
    enabled=$(echo "$entry" | jq -r '.enabled // true')
    [ "${enabled}" != "true" ] && continue

    new_sha=$(git ls-remote "${repo}" HEAD 2>/dev/null | awk '{print $1}')
    if [ -z "${new_sha}" ]; then
      warn "${name} ls-remote fail — kept old pin"
      continue
    fi

    old_sha=$(echo "$entry" | jq -r '.commit // empty')
    if [ "${old_sha}" = "${new_sha}" ]; then
      ok "${name} already at HEAD ${new_sha:0:8}"
    else
      jq --arg name "${name}" --arg sha "${new_sha}" \
        '(.skills[] | select(.name == $name) | .commit) = $sha' "${tmp}" > "${tmp}.new"
      mv "${tmp}.new" "${tmp}"
      ok "${name} ${old_sha:0:8} → ${new_sha:0:8}"
    fi
  done

  mv "${tmp}" "${SKILLS_JSON}"
  warn "external-skills.json updated. Review diff + commit. Then run ./scripts/update.sh (without --bump) to sync local clones."
  exit 0
fi

bold "==> Syncing external skills to pinned commits"
mkdir -p "${REPOS_DIR}"

jq -c '.skills[]' "${SKILLS_JSON}" | while read -r entry; do
  name=$(echo "$entry" | jq -r '.name')
  repo=$(echo "$entry" | jq -r '.repo')
  commit=$(echo "$entry" | jq -r '.commit // empty')
  enabled=$(echo "$entry" | jq -r '.enabled // true')

  [ "${enabled}" != "true" ] && { warn "${name} disabled — skip"; continue; }
  [ -z "${commit}" ] && { err "${name} no pin — run --bump first"; continue; }

  repo_dir="${REPOS_DIR}/${name}"
  if [ ! -d "${repo_dir}/.git" ]; then
    warn "${name} not cloned — run ./scripts/install.sh"
    continue
  fi

  current=$(git -C "${repo_dir}" rev-parse HEAD 2>/dev/null || echo "unknown")
  if [ "${current}" = "${commit}" ]; then
    ok "${name} already @ ${commit:0:8}"
    continue
  fi

  if ! git -C "${repo_dir}" cat-file -e "${commit}^{commit}" 2>/dev/null; then
    git -C "${repo_dir}" fetch --quiet origin "${commit}" 2>/dev/null || git -C "${repo_dir}" fetch --quiet origin || true
  fi
  if git -C "${repo_dir}" checkout --quiet "${commit}" 2>/dev/null; then
    ok "${name} ${current:0:8} → ${commit:0:8}"
  else
    err "${name} checkout ${commit:0:8} fail"
  fi
done

bold "==> Refreshing Claude plugin metadata"
if command -v claude >/dev/null; then
  claude plugin marketplace update imperium-of-guilliman 2>/dev/null && ok "marketplace metadata refreshed" || warn "marketplace refresh fail"
fi

bold "==> Done."
