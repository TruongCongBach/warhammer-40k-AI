# Network / Log Analysis Template

## Purpose

Use this template when HAR, Charles, zip archives, JSON payloads, or text logs are provided.

## First Pass

- identify file type
- note source system if known
- unzip archives when needed
- normalize HAR or JSON before interpretation
- summarize patterns rather than quoting whole files

## What to Look For

- failed requests: `status >= 400`
- slow requests above a chosen threshold
- duplicate requests to the same normalized endpoint
- suspicious payloads: null IDs, empty required fields, malformed filters, unexpected flags
- auth problems: `401`, `403`, expired tokens, missing headers
- caching or concurrency issues: repeated retries, stale responses, race indicators
- environment or routing issues: wrong host, wrong versioned path, mixed staging and production calls
- backend fault signals: `500`, `502`, `503`, structured error payloads

## Template

```markdown
Network/log findings
- Artifacts reviewed: ...
- File type summary: ...
- Failed requests:
  - METHOD URL -> STATUS (brief note)
- Slow requests:
  - METHOD URL -> TIME ms
- Duplicate patterns:
  - METHOD URL xCOUNT
- Suspicious payloads:
  - ...
- Error signatures:
  - ...
- Most likely system boundary:
  - frontend | backend | auth | network | config | third-party | unknown
```

## Script Usage

Run:

```bash
python3 scripts/inspect_ticket_artifacts.py path/to/file.har
python3 scripts/inspect_ticket_artifacts.py archive.zip --slow-ms 1500 --top 10
```

Treat the script output as a structured clue set. Refine the final analysis manually.
