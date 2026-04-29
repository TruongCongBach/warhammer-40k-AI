# Source ladder — full reference

## Tier 1 — Official vendor docs (always preferred)

| Domain | Use for |
|--------|---------|
| `react.dev` | React core, hooks, server components |
| `tanstack.com/query/latest/docs` | TanStack Query v5 |
| `tanstack.com/router/latest/docs` | TanStack Router |
| `docs.expo.dev` | Expo SDK |
| `reactnative.dev/docs` | React Native core |
| `developer.apple.com/documentation` | iOS, Swift, UIKit |
| `developer.android.com/reference` | Android SDK |
| `nodejs.org/docs/latest/api` | Node.js |
| `docs.python.org/3/` | Python stdlib |
| `developer.mozilla.org` | Web platform (HTML/CSS/JS standards) |
| `docs.stripe.com` | Stripe API |
| `docs.aws.amazon.com` | AWS services |
| `cloud.google.com/docs` | GCP |

URL pattern: usually `<vendor>.com/docs/<version>/<topic>` or `<vendor>.dev/reference/<topic>`. WebFetch directly.

### Version pinning

Vendor docs often default to "latest". For older-version research, look for version dropdown or pinned URL:
- React: `https://18.react.dev/...` for v18-pinned
- React Native: `https://reactnative.dev/docs/0.77/<topic>`
- Stripe API: header `Stripe-Version: 2024-04-10`
- Always note the version in citation.

## Tier 2 — Official GitHub repo

```bash
# Repo info
gh repo view <owner>/<name>

# README content
gh api repos/<owner>/<name>/readme --jq '.content' | base64 -d

# Latest releases (newest first)
gh release list -R <owner>/<name> -L 5

# Specific release notes
gh release view v5.0.0 -R tanstack/query

# CHANGELOG file
gh api repos/<owner>/<name>/contents/CHANGELOG.md --jq '.content' | base64 -d | head -200

# Default branch
gh repo view <owner>/<name> --json defaultBranchRef --jq '.defaultBranchRef.name'
```

### When repo > vendor docs

- Library has no separate docs site
- You need actual source (e.g., type signature, default config)
- You need to verify a behavior changed in a specific commit

## Tier 3 — Package registries

```bash
# Current published version
npm view react version

# All dist-tags (latest, next, beta, rc)
npm view react dist-tags

# Repo URL from package.json
npm view react repository.url

# Deprecation status
npm view some-old-pkg deprecated

# Full metadata
npm view react

# Python equivalent
pip index versions <pkg>
curl -s https://pypi.org/pypi/<pkg>/json | jq '.info.version'
```

## Tier 4 — Context7 MCP

See `context7.md`. Best for popular libraries when version-pinned doc is needed and Tier 1 URL is non-obvious.

## Tier 5 — GitHub search

```bash
# Hunt known bug
gh search issues "ENOSPC simulator" -R facebook/react-native --state closed --limit 5

# Find PR that introduced a change
gh search prs "remove findDOMNode" -R facebook/react

# Cross-repo search
gh search code "FlatList scrollToIndex" --owner facebook --limit 10
```

## Tier 6 — WebSearch

Open query. Use only when previous tiers fail or you don't yet know the URL pattern.

Best practices:
- Scope by domain: `react useEffect cleanup site:react.dev`
- Date-bound: `Stripe webhook 2024 invoice.paid` to filter old answers
- Quote exact error: `"Module not found: Can't resolve 'crypto'" webpack 5`

## Tier 7 — Stack Overflow / blogs (last resort)

Never sole source for:
- Production architectural decision
- Security-sensitive behavior
- Migration path for breaking change
- Anything where being wrong has cost

OK as supporting evidence after Tier 1 confirmation.

## Verification heuristics

For high-stakes claims (breaking change, deprecation, security boundary):

1. **Two-source rule** — confirm same fact in 2 independent sources (e.g., vendor docs + CHANGELOG entry).
2. **Date check** — source dated within last 12 months for fast-moving libs (React, RN, Next.js).
3. **Version match** — source explicitly mentions the version under question.
4. **Author signal** — official maintainer / org account > random blog post.

If any check fails → label confidence `low` and tell caller "user verify before acting".

## Per-domain quirks

| Domain | Watch out for |
|--------|---------------|
| MDN | Community wiki — recent edits may be unreviewed; check edit history for new claims |
| Stack Overflow | Accepted answer can be 10y old and wrong now. Look at vote dates + comments |
| Medium / dev.to | Often misleading; never sole source. Useful for "why did X exist" archaeology only |
| Vendor blog (react.dev/blog) | Authoritative — same weight as docs |
| GitHub Discussions | Maintainer comment > random user. Check OP role |
| Reddit r/<lang> | Anecdotal. Useful for community sentiment, not facts |
