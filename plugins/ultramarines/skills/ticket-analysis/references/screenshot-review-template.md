# Screenshot Review Template

## Purpose

Use this template when a screenshot or design image accompanies the ticket.

When the image is central to the ticket, prefer generating a normalized design note first:

```bash
python3 ../../scripts/extract_design_context.py path/to/image.png --include-raw
```

Then use that Markdown note alongside the original image.

## What to Inspect

- visible screen or route
- platform clues: iOS, Android, mobile web, desktop web
- loading, empty, success, or error state
- layout integrity: overlap, clipping, truncation, overflow
- spacing and alignment issues that are clearly visible
- missing or unexpected UI elements
- copy mismatches or inconsistent labels
- disabled, hidden, or incorrect CTA states
- visual signs of stale state, incorrect data, or wrong navigation context

## Template

```markdown
Design/UI findings
- Image type: screenshot | design image | unknown
- Design context note: path/to/design-context.md | inline summary
- Visible context: ...
- Observed issue: ...
- Likely impacted component or screen: ...
- Confidence: high | medium | low
- Assumptions:
  - ...
- What cannot be confirmed from the image alone:
  - ...
```

## Rules

- Describe only what is visible.
- Infer state cautiously and label it as an assumption.
- Do not claim exact pixel values, spacing tokens, or design-system specs unless another source confirms them.
- If the image conflicts with the ticket text, note the conflict explicitly.
