# Design Context Template

Use this template for the normalized Markdown note produced from a screenshot or design image.

```markdown
# Design Context

## Extraction Summary
- Source image: `...`
- Engine used: omniparser | markitdown
- Extraction note: ...

## Visible Text
- ...

## Detected Elements
- button | "Continue" | confidence 0.94 | bounds 120,540,340,604

## Likely Layout Structure
- Header near ...
- Primary CTA near ...

## Likely Interaction Points
- button: Continue [120,540,340,604]

## Assumptions And Limits
- ...
```

## Rules

- Keep extracted design context clearly separate from confirmed design spec.
- Prefer parser-derived evidence over free-form interpretation.
- If the parser is weak or unavailable, keep the note short and explicit about its limits.
- Preserve the original image path in the note for traceability.
