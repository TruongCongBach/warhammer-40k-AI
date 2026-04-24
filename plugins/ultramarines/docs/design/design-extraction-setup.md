# Design Extraction Setup

Use this setup when you want screenshots or design images to become structured text that the ticket workflow can reuse.

You do not need to install another skill for this. The existing `ticket-analysis`, `ticket-planner`, and `ticket-review` skills already know how to call the wrapper in this repo.

## Recommended Engine Order

1. **Primary**: Microsoft OmniParser for UI-aware screenshot parsing
2. **Fallback**: MarkItDown for OCR and Markdown extraction

The wrapper script in this repo uses the same order.

## What Another Machine Actually Needs

Required:

- this skills repo
- Python 3

Optional but recommended:

- OmniParser for better UI-aware parsing
- MarkItDown for OCR/Markdown fallback

## Wrapper Command

Run:

```bash
python3 scripts/extract_design_context.py path/to/design.png --include-raw
```

The script prefers:

1. `OMNIPARSER_URL`
2. `OMNIPARSER_CMD`
3. `markitdown`
4. `uvx markitdown`

## OmniParser Setup

Recommended source: `microsoft/OmniParser`

Official repo:

- `https://github.com/microsoft/OmniParser`

The official project does not provide a stable CLI contract for this repo to depend on directly, so this skills repo expects one of these integration points:

### Option A: Local API

Set:

```bash
export OMNIPARSER_URL="http://localhost:7860/process_image"
```

Use this when you run a local OmniParser-based API server.

### Option B: Local Command Wrapper

Set:

```bash
export OMNIPARSER_CMD="python /absolute/path/to/your_omniparser_wrapper.py --json"
```

Your wrapper should:

- accept the image path as the last argument
- print JSON to stdout
- include parsed elements, text, labels, or bounds when possible

## MarkItDown Setup

Recommended source: `microsoft/markitdown`

Official repo:

- `https://github.com/microsoft/markitdown`

Install locally:

```bash
pip install 'markitdown[all]'
```

Or use:

```bash
uvx markitdown path/to/file.png
```

## Practical Guidance

- Use OmniParser when you need better UI structure, interactable regions, and element hints.
- Use MarkItDown when you mostly need screen text, labels, and rough section order.
- Keep the original image in the workflow even after extraction. The Markdown note is supporting context, not the source of truth.

## Minimal Machine Setup

If you want the simplest reliable setup on another machine:

1. Install this skills repo
2. Install MarkItDown
3. Verify the wrapper script works

Example:

```bash
pip install 'markitdown[all]'
python3 scripts/extract_design_context.py path/to/image.png --include-raw
```

If you want the strongest UI parsing quality, add OmniParser after that.
