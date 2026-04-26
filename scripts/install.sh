#!/usr/bin/env bash
# Imperium of Man — installer
# Run on a fresh machine to set up: marketplace, plugins, external skills, MCP env, Maestro.
set -euo pipefail

# Never prompt for git credentials — fail fast on private/missing repos.
export GIT_TERMINAL_PROMPT=0
export GIT_ASKPASS=/bin/echo
export SSH_ASKPASS=/bin/echo

REPO_ROOT="$(cd "$(dirname "$0")/.." && pwd)"
AGENTS_DIR="${HOME}/.agents/skills"
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

# ---------- external skills ----------
bold "==> Cloning external skills"
mkdir -p "${AGENTS_DIR}" "${CLAUDE_SKILLS}"
SKILLS_JSON="${REPO_ROOT}/scripts/external-skills.json"

jq -c '.skills[]' "${SKILLS_JSON}" | while read -r entry; do
  name=$(echo "$entry" | jq -r '.name')
  repo=$(echo "$entry" | jq -r '.repo')
  subdir=$(echo "$entry" | jq -r '.subdir // empty')
  enabled=$(echo "$entry" | jq -r '.enabled // true')
  target="${AGENTS_DIR}/${name}"

  if [ "${enabled}" != "true" ]; then
    warn "${name} disabled in external-skills.json — skip"
    continue
  fi

  if [ -d "${target}/.git" ] || [ -d "${target}" ]; then
    warn "${name} already exists at ${target} — skip clone"
  else
    if [ -n "${subdir}" ]; then
      tmpdir=$(mktemp -d)
      if ! git clone --depth 1 "${repo}" "${tmpdir}/repo" >/dev/null 2>&1; then
        err "clone fail: ${repo} — skip ${name}"
        rm -rf "${tmpdir}"
        continue
      fi
      if [ -d "${tmpdir}/repo/${subdir}" ]; then
        mv "${tmpdir}/repo/${subdir}" "${target}"
        # keep .git pointer for updates: re-clone full so update.sh can git pull
        rm -rf "${target}/.git" 2>/dev/null || true
        (cd "${target}" && git init -q && git remote add origin "${repo}" && \
         git config core.sparseCheckout true && \
         echo "${subdir}/*" > .git/info/sparse-checkout) 2>/dev/null || true
        ok "${name} (sparse from ${repo})"
      else
        err "${name}: subdir ${subdir} not found in ${repo}"
      fi
      rm -rf "${tmpdir}"
    else
      git clone --depth 1 "${repo}" "${target}" >/dev/null 2>&1 && ok "${name}" || { err "clone fail: ${repo}"; continue; }
    fi
  fi

  # Symlink to ~/.claude/skills (only if target exists)
  link="${CLAUDE_SKILLS}/${name}"
  if [ -d "${target}" ] && [ ! -e "${link}" ]; then
    ln -s "${target}" "${link}" && ok "  linked → ~/.claude/skills/${name}"
  fi
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
