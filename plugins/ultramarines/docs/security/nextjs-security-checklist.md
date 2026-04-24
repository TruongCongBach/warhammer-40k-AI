# Next.js Security Checklist

Use this checklist when a Next.js ticket may affect security-sensitive behavior.

## Focus Areas

- Server vs client boundaries: data fetching location, secrets exposure, server action inputs, client bundle leakage
- Auth and session handling: cookies, headers, middleware, redirects, stale session assumptions
- Authorization: route guards, server-side enforcement, API route ownership checks, tenant boundaries
- Caching and revalidation: sensitive data cached too broadly, shared cache keys, stale protected content
- Request validation: query params, form inputs, file uploads, server action payloads, API body validation
- Redirects and external navigation: open redirects, return URLs, callback validation
- Logging and observability: secrets in logs, verbose error responses, personally identifiable data in traces
- Headers and browser policy: CSP, cookie flags, CORS implications, iframe/embed exposure
- Public vs private environment variables: leaking server-only config into the client bundle

## Questions To Ask

- Is the sensitive logic enforced on the server, not just hidden in the UI?
- Could a cache or revalidation path expose data across users or tenants?
- Are redirects and callback URLs validated tightly enough?
- Are secrets or internal headers leaking into the client or logs?
- Do server actions and APIs validate untrusted input before use?
