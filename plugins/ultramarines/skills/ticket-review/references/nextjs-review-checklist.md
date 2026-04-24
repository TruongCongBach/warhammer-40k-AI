# Next.js Review Checklist

## Purpose

Use this checklist when reviewing a Next.js implementation.

## Checklist

- Route behavior matches the ticket scope.
- Server component and client component boundaries look appropriate.
- Loading and error states are present where user-visible latency exists.
- Search params, route params, and dynamic segments are handled correctly.
- Mutations and follow-up refresh or revalidation behavior are coherent.
- Auth or permission gating matches the expected user flow.
- Cache, stale-data, or revalidation risks are accounted for.
- Hardcoded values are not replacing shared config or tokens without reason.
- SEO or metadata changes are considered if the ticket affects discoverability or shareability.
- Tests cover critical rendering and interaction paths when risk warrants it.

## Common Review Targets

- `app/` or `pages/`
- route segments and layouts
- client components
- server actions or API routes
- shared components
- data services and validators
- middleware or auth guards
