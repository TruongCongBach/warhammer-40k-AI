# Context7 MCP — version-pinned library docs

[Context7](https://github.com/upstash/context7) is an MCP server that fetches up-to-date, version-pinned library documentation by library ID. Use when Tier 1 (vendor docs) URL pattern is non-obvious or when you need a snapshot at a specific version.

## Install

```bash
# As MCP server in your Claude Code project
claude mcp add context7 -- npx -y @upstash/context7-mcp
```

Or add to project `.mcp.json`:

```json
{
  "mcpServers": {
    "context7": {
      "type": "stdio",
      "command": "npx",
      "args": ["-y", "@upstash/context7-mcp"]
    }
  }
}
```

Optional: set `CONTEXT7_API_KEY` for higher rate limits (free tier exists).

## Detection

Before using context7 in this skill, check it's available:

- If MCP tool surfaces include `mcp__context7__*` → installed, use directly.
- Otherwise → fall back to Tier 1-3 (vendor docs / GitHub / npm).

Do NOT pretend context7 results when it's not installed — that violates the skill's anti-hallucination rule.

## Usage pattern

Context7 typically exposes:

1. **Resolve library ID** — convert human name to context7 ID:
   ```
   resolve-library-id "react"          → /facebook/react
   resolve-library-id "tanstack query" → /tanstack/query
   ```

2. **Fetch docs** — pull doc content for a library + topic:
   ```
   get-library-docs /facebook/react --topic "useEffect" --tokens 5000
   ```

   The returned content is doc snippets ranked by relevance to the topic.

## When context7 beats Tier 1

- Library has many doc pages and you need only the relevant snippet (token-efficient).
- Vendor docs URL keeps changing or has bad search.
- You want a stable version snapshot rather than "latest" drift.
- Library is popular but its doc site is hard to scrape (JS-rendered, paywalled).

## When NOT to use context7

- Library is small/niche → context7 may not have it; fall back to GitHub.
- Vendor doc URL is known and stable → WebFetch is faster.
- You need the very latest unreleased behavior → context7 may lag the actual repo.

## Cite format

When citing a context7 result:

```
[via skill: astropath, source: context7]
- library: /facebook/react
- topic: useEffect
- accessed: 2026-04-29
- excerpt: "useEffect runs after the browser has painted..."
- confidence: medium (context7 snapshot — verify against react.dev for current)
```

Confidence is `medium` not `high` because context7 is a snapshot service. For production decisions, cross-check with vendor docs (Tier 1).

## Limits

- Coverage skews to popular libraries (React, Vue, Next.js, etc). Niche libs may not be indexed.
- Free tier rate-limits — if hitting limits, fall back to WebFetch on vendor docs.
- Snapshot freshness varies. Check the doc URL the snippet came from for recent commits.
