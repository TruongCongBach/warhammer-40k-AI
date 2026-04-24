# Next.js Planning Checklist

## Purpose

Use this checklist when the ticket affects a Next.js app.

## Checklist

- Route or page entry point is identified.
- Server component versus client component boundary is considered.
- Data fetching location is appropriate for the planned change.
- Loading and error states are considered.
- Mutation flow and cache revalidation behavior are considered.
- Auth, session, and permission boundaries are considered.
- Search params, route params, or dynamic segments are considered.
- SEO or metadata impact is considered if relevant.
- Environment-specific behavior is considered.
- Feature flags or configuration dependencies are considered.
- Analytics or observability impact is considered if relevant.

## Likely Affected Areas

- `app/` or `pages/`
- route segments and layouts
- server actions or API routes
- client components
- shared UI components
- data services, fetchers, mappers, validators
- caching and revalidation helpers
- middleware or auth guards
