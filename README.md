# Imperium of Guilliman

Personal Claude Code marketplace + plugins. Warhammer 40k themed agent-coding setup, bound by the **Codex Astartes** — every agent obeys the same doctrine before its own oath. Portable across machines: clone repo, run `scripts/install.sh`, fill env vars, ready.

> Named for **Roboute Guilliman**, Primarch of the Ultramarines and author of the Codex Astartes — the strict doctrine that turned warfare into discipline. Same idea here: turn agent-coding into discipline.

## What's inside

```
imperium-of-guilliman (marketplace)
├── ultramarines        # main plugin: ticket-pipeline agents + ticket-* skills + commands
│                       #   bound by plugins/ultramarines/CODEX_ASTARTES.md
└── adeptus-mechanicus  # MCP plugin: jira / newrelic / notebooklm (env-driven)
```

**Codex Astartes** = `plugins/ultramarines/CODEX_ASTARTES.md`. Universal tenets all agents follow + per-agent oaths + pipeline hand-off contract + stop-points. Read it before tweaking any agent.

**External skills** with confirmed upstream (currently `agent-device`, `agent-react-devtools`, `agent-browser`) are cloned by `install.sh` over **SSH** to `~/.agents/skills/` and symlinked to `~/.claude/skills/`. `update.sh` runs `git pull` on each → upstream updates flow through. SSH key required (`ssh -T git@github.com` to verify).

**Bundled skills** (everything else: `dogfood`, `react-doctor`, `vercel-react-best-practices`, `microsoft-foundry`, `skill-creator`, etc.) ship inside `plugins/ultramarines/skills/` — loaded automatically when the plugin is enabled, no clone needed. Update by editing in this repo + git push.

## Install

```bash
git clone https://github.com/<you>/warhammer-40k-AI.git ~/JmangoProjects/warhammer-40k-AI
cd ~/JmangoProjects/warhammer-40k-AI
./scripts/install.sh

# fill tokens
$EDITOR ~/.config/imperium-of-guilliman/env.sh
echo '[ -f ~/.config/imperium-of-guilliman/env.sh ] && source ~/.config/imperium-of-guilliman/env.sh' >> ~/.zshrc
source ~/.zshrc

# verify
claude
# inside: /plugin → see ultramarines + adeptus-mechanicus
```

## Update

```bash
./scripts/update.sh
```

Pulls marketplace + each external skill upstream.

## Ticket pipeline (Codex Astartes)

Slash command `/ticket-pipeline <ticket-id>` runs 6 disciplined steps. Each step = 1 themed agent.

| # | Agent | Vai trò | Skill chính |
|---|-------|---------|-------------|
| 1 | **librarian** | Đọc & phân tích ticket | `ticket-analysis` |
| 2 | **inquisitor** | Truy nguyên root cause | `karpathy-guidelines` + `ticket-analysis` |
| 3 | **techmarine** | Plan fix (1-2 approach + tradeoff) | `ticket-planner` |
| 4 | **chapter-master** | Execute (write code) | `clean-code-agent` + `karpathy-guidelines` |
| 5 | **apothecary** | Impact + regression matrix | `ticket-review` |
| 6 | **tech-priest** | Auto-test (Maestro / agent-device) | `agent-device`, `dogfood`, Maestro |

### Test tool selection (tech-priest)

| Case | Tool |
|------|------|
| Multi-step E2E (≥3 step), regression suite | **Maestro** |
| Single screen verify, exploratory | **agent-device** |
| Component runtime debug | **react-devtools** |

Auto-fallback: Maestro fail → agent-device manual repro.

## Lore mapping

- **Imperium of Guilliman** = marketplace (đế chế under Codex)
- **Ultramarines** = main coding chapter (Codex Astartes = strict discipline ↔ clean code)
- **Adeptus Mechanicus** = MCP / external services (machine cult)
- **Tech-Priest** = automated testing (chants binary canticles to machine spirit)
- **Apothecary** = regression assessor (medic, knows where the body bleeds)
- **Inquisitor** = root cause hunter (interrogates code)

Future chapters (when needed):
- `dark-angels` — security review (sworn secret hunters)
- `space-wolves` — exploratory dogfood (wild)
- `grey-knights` — auth/permission specialist
- `imperial-fists` — defensive testing fortress
- `salamanders` — UI/design review (artisans)
- `iron-hands` — refactor / perf optimization

## Self-written vs upstream

| Type | Where | Updated by |
|------|-------|-----------|
| Self-written skills (ticket-*, clean-code-agent, karpathy-guidelines) | `plugins/ultramarines/skills/` (bundled) | edit in this repo |
| Self-written agents (librarian, inquisitor, ...) | `plugins/ultramarines/agents/` | edit in this repo |
| External skills (agent-device, playwright-cli, ...) | `~/.agents/skills/<name>` (cloned upstream) | `scripts/update.sh` |

## MCP servers (adeptus-mechanicus)

| Server | Type | Env vars needed |
|--------|------|-----------------|
| `jira` | stdio | `ATLASSIAN_SITE_NAME`, `ATLASSIAN_USER_EMAIL`, `ATLASSIAN_API_TOKEN` |
| `notebooklm` | stdio | none (browser auth: `npx notebooklm-mcp@latest setup`) |
| `newrelic` | http | `NEW_RELIC_API_KEY` |

Tokens NEVER committed. See `.env.example`.

## Layout

```
warhammer-40k-AI/
├── .claude-plugin/marketplace.json
├── plugins/
│   ├── ultramarines/
│   │   ├── .claude-plugin/plugin.json
│   │   ├── agents/         # 6 themed + ticket-analyzer + mobile-issue-reproducer
│   │   ├── skills/         # ticket-* + clean-code-agent + karpathy-guidelines
│   │   ├── commands/       # /ticket-pipeline
│   │   ├── docs/           # security/ + design/ checklists referenced by skills
│   │   └── scripts/        # extract_design_context.py
│   └── adeptus-mechanicus/
│       ├── .claude-plugin/plugin.json
│       └── .mcp.json
├── scripts/
│   ├── install.sh
│   ├── update.sh
│   └── external-skills.json
├── .env.example
├── .gitignore
└── README.md
```

## Adding a new themed agent

1. Drop `<chapter-name>.md` in `plugins/ultramarines/agents/` with frontmatter `name`, `description`, `model`, optional `memory: project`.
2. Add lore mapping note here.
3. Optionally add to `/ticket-pipeline` if it's a pipeline step.

## Adding a new external skill

1. Add entry to `scripts/external-skills.json` (`name`, `repo`, `subdir` optional).
2. Run `./scripts/install.sh` again — idempotent, only clones missing.

---

For the Emperor.
