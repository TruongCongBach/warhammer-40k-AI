---
name: maestro
description: Author and run Maestro mobile UI tests (iOS, Android, React Native, Flutter). Use when user asks to write a Maestro flow, debug a flaky E2E, run `maestro test`/`studio`/`cloud`/`record`/`hierarchy`, fix `testID`/selectors, handle OTP/permission dialogs, set up CI for mobile tests, or mentions `.maestro/`, `runFlow`, `clearState`, `launchApp`, GraalJS scripting, or `maestro mcp`. Covers selector strategy, adaptive auth flows, platform gotchas (iOS Keychain, XCTest cold-boot), CI sharding/tags, and the write-run-fix loop.
allowed-tools: Bash(maestro:*), Bash(adb:*), Bash(xcrun:*), Read, Write, Edit, Glob, Grep
---

# Maestro — Mobile E2E Authoring

Maestro = YAML-flow-driven mobile UI test runner. Single binary, declarative, fast feedback. This skill teaches **authoring durable flows**; `maestro mcp` and `maestro studio` are the runtime companions.

Companion skills in this plugin:
- `agent-device` — ad-hoc imperative driving for **bug repro / exploration**
- `dogfood` — exploratory QA report
- `maestro` (this) — **regression-grade flows committed to repo**

Decision: repro one-off bug → `agent-device`. Lock regression → write Maestro flow.

## Quick start

```bash
# Run one flow on connected device/simulator
maestro test .maestro/flows/login-success.yaml

# Run whole suite, JUnit report, retry flakes, parallel shards
maestro test --include-tags=ci --shards=2 --retries=1 --format=junit --output=report.xml .maestro/flows

# Live record + autocomplete authoring
maestro studio

# Cloud (only path for iOS in CI)
maestro cloud --apiKey=$MAESTRO_API_KEY app.app .maestro/flows --include-tags=smoke

# Print live view hierarchy (find selectors)
maestro hierarchy

# MCP server for LLM agents (write-run-fix loop)
maestro mcp
```

Recommended layout:

```
.maestro/
├── flows/                    # one feature per file
│   ├── login-success.yaml
│   ├── login-otp.yaml
│   └── checkout-happy-path.yaml
├── subflows/                 # reusable bits
│   ├── auth.yaml
│   └── dismiss-permissions.yaml
├── scripts/                  # GraalJS helpers
│   ├── fetch-otp.js
│   └── split-otp.js
└── config.yaml               # shared appId, tags, env
```

Naming: `{feature}-{action}.yaml`. Tag every flow with one of `ci`, `smoke`, `wip`, `nightly`.

## Core flow skeleton

```yaml
appId: com.example.app
tags:
  - ci
  - smoke
---
- launchApp:
    clearState: true
- runFlow:
    file: ../subflows/auth.yaml
    when:
      visible: "Sign in"
- assertVisible: "Home"
- tapOn:
    id: "checkout-button"
- assertVisible:
    id: "order-confirmation"
    timeout: 5000
- takeScreenshot: artifacts/checkout-confirmed
```

Full annotated template: `assets/flow-template.yaml`.

## Selector strategy (decision matrix)

| Priority | Selector | When |
|----------|----------|------|
| 1 | `id: "testID"` | First choice always. Stable, fast, locale-proof. |
| 2 | `text: "..."` | When testID impossible; pin via `containsDescendants`/`childOf` to scope. |
| 3 | `text` + relative (`below`, `above`, `leftOf`, `rightOf`, `childOf`) | Disambiguating list rows or repeated labels. |
| 4 | State props (`enabled`, `checked`, `focused`, `selected`) | Asserting toggle/radio state. |
| ❌ | `index: N` | **Banned.** Brittle to layout change. Refactor to scoped relative selector. |

State assertion example:
```yaml
- assertVisible:
    id: "notif-toggle"
    checked: true
```

Scoped tap (avoid `index`):
```yaml
- tapOn:
    text: "Delete"
    childOf:
      id: "cart-row-${ITEM_ID}"
```

Auth-loaded pre-flight (zero-size testID at top of authed screens lets flows branch reliably):
```yaml
- runFlow:
    when:
      visible:
        id: "auth-loaded"
    file: ../subflows/post-auth.yaml
```

## Common gotchas (full list: `references/gotchas.md`)

| Symptom | Cause | Fix |
|---------|-------|-----|
| `clearState: true` but user still logged in (iOS) | iOS Keychain survives app data wipe | Add explicit logout subflow or use `clearKeychain: true` |
| `kAXErrorInvalidUIElement` cold-boot iOS | XCTest race on first launch | Add `- swipe: { from: { x: 50%, y: 50% }, to: { x: 50%, y: 40% } }` after `launchApp` |
| `evalScript` `fetch is not defined` | GraalJS, not Node | Use `http.get(url)`; no `fetch`, no `async/await` |
| Deep link opens wrong app | Used bundle ID where scheme expected | `openLink: myapp://path` (URL scheme, not appId) |
| Tab bar selector finds wrong item post-login | Pre/post auth tabs share text | Add scoping: `childOf: { id: "authed-tabbar" }` |
| Permission dialog blocks flow | OS-level overlay not in app hierarchy | `tapOn: { text: "Allow", optional: true }` and add platform-specific labels (see `references/platforms.md`) |
| Optimistic UI assertion flakes | Server roundtrip ~5s, default timeout 1.5s | `timeout: 5000` for network-bound asserts; `3000` for animations |

## Per-flow checklist

Before committing a flow:

- [ ] `appId` set, tags include `ci` or `smoke`
- [ ] Cold-boot resilient (`launchApp: { clearState: true }`)
- [ ] All taps use `id:` or scoped `text` — no `index:`
- [ ] Auth handled via `runFlow` + `when: visible:` (idempotent)
- [ ] Permission dialogs `optional: true`
- [ ] Optimistic asserts have explicit `timeout`
- [ ] `takeScreenshot` at every key checkpoint
- [ ] Runs locally clean 3× in a row before push

## CI in one paragraph

GitHub Actions: `mobile-dev-inc/action-maestro-cloud@v2` for cloud, or self-hosted macOS runner for `maestro test`. Shard with `--shards=N`, retry flakes with `--retries=1`, filter with `--include-tags=ci`. Android in CI: Docker emulator OK. **iOS in CI: Maestro Cloud only** (no GitHub-hosted iOS simulator support for Maestro). Full template: `assets/github-actions-maestro-cloud.yml`. Detail: `references/ci.md`.

## When to reach for what

- New feature → write flow first in `studio`, then commit YAML.
- Flake hunt → `maestro test --debug` + `references/gotchas.md`.
- Selector unclear → `maestro hierarchy` while screen open.
- Auth/OTP → GraalJS script + Mailpit/mock; see `references/graaljs.md` + `assets/fetch-otp.js`.
- LLM-driven authoring → `maestro mcp` (write-run-fix loop).
- Platform-specific dialog text → `references/platforms.md`.

## References (load on demand)

- `references/selectors.md` — full selector grammar, relative selectors, anti-patterns
- `references/ci.md` — GitHub Actions / GitLab CI / sharding / artifacts
- `references/platforms.md` — iOS vs Android vs RN vs Flutter specifics
- `references/graaljs.md` — `evalScript` rules, OTP fetch, mock API
- `references/gotchas.md` — full symptom→cause→fix table

## Assets

- `assets/flow-template.yaml` — annotated skeleton
- `assets/subflow-auth.yaml` — adaptive login subflow
- `assets/fetch-otp.js` — GraalJS Mailpit fetch
- `assets/split-otp.js` — extract code from email body
- `assets/github-actions-maestro-cloud.yml` — CI template
