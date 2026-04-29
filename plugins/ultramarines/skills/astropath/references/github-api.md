# GitHub research patterns (`gh` CLI)

`gh` is preinstalled on most dev machines. Use it to fetch repo state authoritatively without scraping HTML.

## Auth check (do first)

```bash
gh auth status
```

If unauthenticated, public-only queries still work (rate-limited). Authenticated = 5000 req/h, public-only = 60 req/h.

## Repo metadata

```bash
# Basic
gh repo view facebook/react

# Specific fields, JSON
gh repo view facebook/react --json name,description,defaultBranchRef,licenseInfo,homepageUrl,stargazerCount

# README rendered
gh api repos/facebook/react/readme --jq '.content' | base64 -d
```

## Releases / versions

```bash
# Latest 10 releases (most recent first)
gh release list -R facebook/react -L 10

# Specific release notes
gh release view v18.3.0 -R facebook/react

# Latest tag (semver)
gh api repos/facebook/react/releases/latest --jq '.tag_name'

# All tags
gh api repos/facebook/react/tags --jq '.[].name' | head -20
```

## Issues / PRs

```bash
# View specific issue
gh issue view 12345 -R facebook/react

# Last 10 open issues
gh issue list -R facebook/react -L 10 --state open

# Search across repo
gh search issues "useEffect cleanup async" -R facebook/react --state closed --limit 5

# PR that closed an issue
gh issue view 12345 -R facebook/react --json closedByPullRequestsReferences

# Check if issue is fix-merged
gh pr view <num> -R facebook/react --json mergedAt,state
```

Use this when ticket says "user reports X bug" and you want to know if it's a known issue or already fixed upstream.

## File contents at specific ref

```bash
# File at HEAD
gh api repos/facebook/react/contents/packages/react/package.json --jq '.content' | base64 -d

# File at specific commit / tag / branch
gh api "repos/facebook/react/contents/packages/react/package.json?ref=v18.3.0" --jq '.content' | base64 -d
```

## Compare versions / changelog excerpt

```bash
# Diff URL between two tags (HTML)
echo "https://github.com/facebook/react/compare/v18.3.0...v18.3.1"

# Programmatic compare (commit list)
gh api repos/facebook/react/compare/v18.3.0...v18.3.1 --jq '.commits[].commit.message' | head -20

# Changelog file
gh api repos/facebook/react/contents/CHANGELOG.md --jq '.content' | base64 -d | head -100
```

## Search across many repos

```bash
# Find all repos using a specific dep version
gh search code '"react": "18.0.0"' --extension json --filename package.json --limit 20

# Find migration guides
gh search code "useDeferredValue" --language tsx --owner facebook --limit 10
```

## Rate-limit awareness

```bash
gh api rate_limit --jq '.rate'
```

If `remaining` < 100, slow down or fall back to a different tier.

## When to use which

| Goal | Command |
|------|---------|
| "Is package X up to date?" | `gh release list -R <repo> -L 1` + `npm view X version` |
| "Did upstream fix this bug?" | `gh search issues "<symptom>" -R <repo>` |
| "What changed in v5?" | `gh release view v5.0.0 -R <repo>` |
| "What's the typescript signature of foo?" | `gh api repos/<repo>/contents/<path>?ref=<tag>` |
| "Are there any known security advisories?" | `gh api repos/<owner>/<name>/security-advisories` (if accessible) |
| "Who maintains this?" | `gh repo view <repo> --json owner,homepageUrl` |

## Cite format

```
[via skill: astropath, source: github]
- repo: facebook/react
- ref: v18.3.0 (release)
- url: https://github.com/facebook/react/releases/tag/v18.3.0
- accessed: 2026-04-29
- excerpt: "..."
- confidence: high (official release notes)
```
