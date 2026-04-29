# CI integration

## GitHub Actions — Maestro Cloud (recommended for iOS)

```yaml
name: maestro-cloud
on: [pull_request, push]
jobs:
  maestro:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - uses: mobile-dev-inc/action-maestro-cloud@v2
        with:
          api-key: ${{ secrets.MAESTRO_CLOUD_API_KEY }}
          app-file: build/app.apk          # or .app.zip for iOS
          workspace: .maestro/flows
          include-tags: ci
          env: |
            BASE_URL=https://staging.example.com
```

Multi-platform matrix:

```yaml
strategy:
  matrix:
    include:
      - app: build/app.apk
        platform: android
      - app: build/app.app.zip
        platform: ios
```

## GitHub Actions — self-hosted macOS (Android only or local sim)

```yaml
runs-on: [self-hosted, macos]
steps:
  - run: curl -Ls "https://get.maestro.mobile.dev" | bash
  - run: maestro test --shards=2 --retries=1 --format=junit --output=maestro-report.xml --include-tags=ci .maestro/flows
  - uses: actions/upload-artifact@v4
    if: always()
    with:
      name: maestro-artifacts
      path: |
        maestro-report.xml
        ~/.maestro/tests/**/screenshots
```

## GitLab CI

```yaml
maestro:
  image: mobiledevinc/maestro:latest
  script:
    - maestro test --include-tags=ci --format=junit --output=report.xml .maestro/flows
  artifacts:
    when: always
    reports:
      junit: report.xml
    paths:
      - ~/.maestro/tests/
```

## Sharding + retries

```bash
# Split suite across 4 parallel runners
maestro test --shards=4 --shard-index=$CI_NODE_INDEX .maestro/flows

# Auto-retry once on flake
maestro test --retries=1 .maestro/flows
```

## Tag strategy

| Tag | Run when | Block merge? |
|-----|----------|--------------|
| `smoke` | every PR | yes |
| `ci` | every PR | yes |
| `nightly` | scheduled | no, alert only |
| `wip` | never in CI | — |

```bash
maestro test --include-tags=ci --exclude-tags=wip .maestro/flows
```

## Reporting

- `--format=junit --output=report.xml` — JUnit XML, auto-rendered by GitHub/GitLab
- `--format=html --output=report.html` — Static HTML report
- Artifacts: screenshots + recordings in `~/.maestro/tests/{flowName}/{timestamp}/`

## iOS in CI — important

GitHub-hosted runners do **not** support Maestro on iOS simulators reliably (XCTest harness install fails). Options:

1. **Maestro Cloud** (paid, recommended) — `mobile-dev-inc/action-maestro-cloud@v2`
2. **Self-hosted macOS runner** — works but slow, brittle
3. **AWS Device Farm via Maestro adapter** — niche

Android in CI: works fine in Docker via `mobiledevinc/maestro:latest` or self-hosted Linux with emulator.
