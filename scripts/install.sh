#!/usr/bin/env bash
# Imperium of Guilliman — installer
# Run on a fresh machine to set up: marketplace, plugins, external skills, MCP env, Maestro.
set -euo pipefail

# Never prompt for git credentials — fail fast on private/missing repos.
export GIT_TERMINAL_PROMPT=0
export GIT_ASKPASS=/bin/echo
export SSH_ASKPASS=/bin/echo

REPO_ROOT="$(cd "$(dirname "$0")/.." && pwd)"
AGENTS_DIR="${HOME}/.agents/skills"
REPOS_DIR="${AGENTS_DIR}/.repos"
CLAUDE_SKILLS="${HOME}/.claude/skills"
ENV_FILE="${HOME}/.config/imperium-of-guilliman/env.sh"

bold() { printf "\033[1m%s\033[0m\n" "$*"; }
ok()   { printf "  \033[32m✓\033[0m %s\n" "$*"; }
warn() { printf "  \033[33m⚠\033[0m %s\n" "$*"; }
err()  { printf "  \033[31m✗\033[0m %s\n" "$*" >&2; }

# ---------- prerequisites ----------
bold "==> Checking prerequisites"
command -v git >/dev/null      || { err "git missing"; exit 1; }
command -v claude >/dev/null   || warn "claude CLI not found — install from https://claude.ai/code"
command -v node >/dev/null     || warn "node missing — needed for npx-based MCP servers"
command -v jq >/dev/null       || { err "jq missing — brew install jq"; exit 1; }

# ---------- marketplace + plugins ----------
bold "==> Registering marketplace + enabling plugins"
if command -v claude >/dev/null; then
  claude plugin marketplace add "${REPO_ROOT}" 2>/dev/null && ok "marketplace added" || warn "marketplace already added"
  claude plugin install ultramarines@imperium-of-guilliman 2>/dev/null && ok "ultramarines installed" || warn "ultramarines already installed"
  claude plugin install adeptus-mechanicus@imperium-of-guilliman 2>/dev/null && ok "adeptus-mechanicus installed" || warn "adeptus-mechanicus already installed"
else
  warn "skip — claude CLI not present"
fi

# ---------- external skills (pinned to commit SHA) ----------
bold "==> Cloning external skills (pinned commits)"
mkdir -p "${AGENTS_DIR}" "${REPOS_DIR}" "${CLAUDE_SKILLS}"
SKILLS_JSON="${REPO_ROOT}/scripts/external-skills.json"

jq -c '.skills[]' "${SKILLS_JSON}" | while read -r entry; do
  name=$(echo "$entry" | jq -r '.name')
  repo=$(echo "$entry" | jq -r '.repo')
  subdir=$(echo "$entry" | jq -r '.subdir // empty')
  commit=$(echo "$entry" | jq -r '.commit // empty')
  enabled=$(echo "$entry" | jq -r '.enabled // true')

  repo_dir="${REPOS_DIR}/${name}"
  skill_link="${AGENTS_DIR}/${name}"
  claude_link="${CLAUDE_SKILLS}/${name}"

  if [ "${enabled}" != "true" ]; then
    warn "${name} disabled in external-skills.json — skip"
    continue
  fi

  if [ -z "${commit}" ]; then
    err "${name} has no pinned commit in external-skills.json — skip (run ./scripts/update.sh --bump to populate)"
    continue
  fi

  # Clone full repo (blobless to save bandwidth) if missing
  if [ ! -d "${repo_dir}/.git" ]; then
    if ! git clone --filter=blob:none "${repo}" "${repo_dir}" >/dev/null 2>&1; then
      err "clone fail: ${repo}"
      continue
    fi
  fi

  # Pin to commit
  if ! git -C "${repo_dir}" cat-file -e "${commit}^{commit}" 2>/dev/null; then
    git -C "${repo_dir}" fetch --quiet origin "${commit}" 2>/dev/null || git -C "${repo_dir}" fetch --quiet origin || true
  fi
  if ! git -C "${repo_dir}" checkout --quiet "${commit}" 2>/dev/null; then
    err "${name} checkout ${commit:0:8} fail — repo may not contain that commit"
    continue
  fi

  # Validate subdir exists at this commit
  if [ -n "${subdir}" ]; then
    src="${repo_dir}/${subdir}"
  else
    src="${repo_dir}"
  fi
  if [ ! -d "${src}" ]; then
    err "${name}: subdir ${subdir} missing at commit ${commit:0:8}"
    continue
  fi

  # Symlink ~/.agents/skills/<name> → repo subdir
  if [ -L "${skill_link}" ] || [ -e "${skill_link}" ]; then
    rm -rf "${skill_link}"
  fi
  ln -s "${src}" "${skill_link}"

  # Symlink ~/.claude/skills/<name> → ~/.agents/skills/<name>
  if [ -L "${claude_link}" ] || [ -e "${claude_link}" ]; then
    rm -rf "${claude_link}"
  fi
  ln -s "${skill_link}" "${claude_link}"

  ok "${name} pinned @ ${commit:0:8} → ${skill_link} → ${claude_link}"
done

# ---------- MCP env ----------
bold "==> Setting up MCP environment"
mkdir -p "$(dirname "${ENV_FILE}")"
if [ ! -f "${ENV_FILE}" ]; then
  cp "${REPO_ROOT}/.env.example" "${ENV_FILE}"
  ok "created ${ENV_FILE} — fill in tokens then \`source ${ENV_FILE}\` in your shell rc"
else
  warn "${ENV_FILE} exists — not overwritten"
fi

# Suggest shell rc inclusion
SHELL_RC="${HOME}/.zshrc"
[ -n "${BASH_VERSION:-}" ] && SHELL_RC="${HOME}/.bashrc"
if ! grep -q "imperium-of-guilliman/env.sh" "${SHELL_RC}" 2>/dev/null; then
  warn "add this to ${SHELL_RC}:"
  echo "    [ -f ${ENV_FILE} ] && source ${ENV_FILE}"
fi

# ---------- Maestro ----------
bold "==> Installing Maestro (mobile E2E)"
if command -v maestro >/dev/null; then
  ok "maestro already installed: $(maestro --version 2>&1 | head -1)"
else
  if command -v brew >/dev/null; then
    brew tap mobile-dev-inc/tap 2>/dev/null || true
    brew install maestro 2>&1 | tail -5
    ok "maestro installed"
  else
    warn "brew not found — install Maestro manually: curl -Ls https://get.maestro.mobile.dev | bash"
  fi
fi

# ---------- agent-device + agent-browser CLI ----------
bold "==> Installing test/automation CLIs"
for pkg in agent-device agent-react-devtools agent-browser; do
  if ! command -v "$pkg" >/dev/null; then
    npm install -g "@callstack/${pkg}" 2>/dev/null && ok "${pkg} installed globally" || warn "${pkg} install fail — try: npx ${pkg}"
  else
    ok "${pkg} already installed"
  fi
done

bold "==> Done."
echo
echo "Next steps:"
echo "  1. Edit ${ENV_FILE} — fill ATLASSIAN_*, NEW_RELIC_API_KEY"
echo "  2. source ${ENV_FILE} (or restart shell)"
echo "  3. cd into a project and run: claude"
echo "  4. Try: /ticket-pipeline MWL-123"
