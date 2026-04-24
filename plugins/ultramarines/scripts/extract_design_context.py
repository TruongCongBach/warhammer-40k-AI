#!/usr/bin/env python3
"""Extract design context from screenshots using OmniParser when available, with MarkItDown fallback."""

from __future__ import annotations

import argparse
import json
import mimetypes
import os
import re
import shlex
import shutil
import subprocess
import sys
import urllib.error
import urllib.request
from dataclasses import dataclass
from pathlib import Path
from uuid import uuid4


DEFAULT_TIMEOUT = 120


@dataclass
class EngineResult:
    engine: str
    source: str
    raw_text: str
    raw_data: object | None = None


def main() -> int:
    parser = argparse.ArgumentParser(
        description=(
            "Extract a Markdown design-context note from a screenshot or design image. "
            "Prefers OmniParser via OMNIPARSER_URL or OMNIPARSER_CMD, then falls back to MarkItDown."
        )
    )
    parser.add_argument("image", help="Path to the screenshot or design image")
    parser.add_argument(
        "--engine",
        choices=("auto", "omniparser", "markitdown"),
        default="auto",
        help="Force a specific extraction engine",
    )
    parser.add_argument(
        "-o",
        "--output",
        help="Optional output Markdown path. Defaults to stdout.",
    )
    parser.add_argument(
        "--max-elements",
        type=int,
        default=20,
        help="Maximum number of parsed UI elements to include",
    )
    parser.add_argument(
        "--raw-limit",
        type=int,
        default=1600,
        help="Maximum raw-output characters to embed",
    )
    parser.add_argument(
        "--include-raw",
        action="store_true",
        help="Include a truncated raw parser section in the Markdown output",
    )
    parser.add_argument(
        "--endpoint",
        help="Override OMNIPARSER_URL for HTTP-based OmniParser integration",
    )
    parser.add_argument(
        "--endpoint-field",
        default="file",
        help="Multipart field name for the image when using OMNIPARSER_URL",
    )
    parser.add_argument(
        "--omniparser-cmd",
        help=(
            "Override OMNIPARSER_CMD for command-based OmniParser integration. "
            "The image path is appended as the last argument."
        ),
    )
    parser.add_argument(
        "--timeout",
        type=int,
        default=DEFAULT_TIMEOUT,
        help="Timeout in seconds for parser execution",
    )
    args = parser.parse_args()

    image_path = Path(args.image).expanduser()
    if not image_path.exists():
        print(f"missing image: {image_path}", file=sys.stderr)
        return 2

    try:
        result = extract_design_context(
            image_path=image_path,
            requested_engine=args.engine,
            endpoint=args.endpoint or os.getenv("OMNIPARSER_URL"),
            endpoint_field=args.endpoint_field,
            omniparser_cmd=args.omniparser_cmd or os.getenv("OMNIPARSER_CMD"),
            timeout=args.timeout,
        )
    except RuntimeError as exc:
        print(render_missing_engine_note(image_path, str(exc)), file=sys.stderr)
        return 3

    markdown = normalize_result(
        image_path=image_path,
        result=result,
        max_elements=args.max_elements,
        raw_limit=args.raw_limit,
        include_raw=args.include_raw,
    )

    if args.output:
        output_path = Path(args.output).expanduser()
        output_path.write_text(markdown, encoding="utf-8")
    else:
        print(markdown)
    return 0


def extract_design_context(
    *,
    image_path: Path,
    requested_engine: str,
    endpoint: str | None,
    endpoint_field: str,
    omniparser_cmd: str | None,
    timeout: int,
) -> EngineResult:
    if requested_engine in {"auto", "omniparser"}:
        if endpoint:
            return run_omniparser_http(
                image_path=image_path,
                endpoint=endpoint,
                endpoint_field=endpoint_field,
                timeout=timeout,
            )
        if omniparser_cmd:
            return run_omniparser_cmd(
                image_path=image_path,
                omniparser_cmd=omniparser_cmd,
                timeout=timeout,
            )
        if requested_engine == "omniparser":
            raise RuntimeError(
                "OmniParser requested but neither OMNIPARSER_URL nor OMNIPARSER_CMD is configured."
            )

    if requested_engine in {"auto", "markitdown"}:
        return run_markitdown(image_path=image_path, timeout=timeout)

    raise RuntimeError("No supported extraction engine is configured.")


def run_omniparser_http(
    *,
    image_path: Path,
    endpoint: str,
    endpoint_field: str,
    timeout: int,
) -> EngineResult:
    mime_type = mimetypes.guess_type(image_path.name)[0] or "application/octet-stream"
    boundary = f"----skills-{uuid4().hex}"
    image_bytes = image_path.read_bytes()

    body = bytearray()
    body.extend(f"--{boundary}\r\n".encode("utf-8"))
    body.extend(
        (
            f'Content-Disposition: form-data; name="{endpoint_field}"; '
            f'filename="{image_path.name}"\r\n'
        ).encode("utf-8")
    )
    body.extend(f"Content-Type: {mime_type}\r\n\r\n".encode("utf-8"))
    body.extend(image_bytes)
    body.extend(f"\r\n--{boundary}--\r\n".encode("utf-8"))

    request = urllib.request.Request(
        endpoint,
        data=bytes(body),
        headers={"Content-Type": f"multipart/form-data; boundary={boundary}"},
        method="POST",
    )

    try:
        with urllib.request.urlopen(request, timeout=timeout) as response:
            raw_bytes = response.read()
    except urllib.error.URLError as exc:
        raise RuntimeError(f"OmniParser HTTP request failed: {exc}") from exc

    raw_text = raw_bytes.decode("utf-8", errors="replace")
    raw_data = parse_json_loose(raw_text)
    if raw_data is None:
        raise RuntimeError("OmniParser HTTP response was not valid JSON.")

    return EngineResult(
        engine="omniparser",
        source=f"omniparser-http:{endpoint}",
        raw_text=raw_text,
        raw_data=raw_data,
    )


def run_omniparser_cmd(
    *,
    image_path: Path,
    omniparser_cmd: str,
    timeout: int,
) -> EngineResult:
    command = shlex.split(omniparser_cmd) + [str(image_path)]
    completed = subprocess.run(
        command,
        capture_output=True,
        text=True,
        timeout=timeout,
        check=False,
    )
    if completed.returncode != 0:
        stderr = completed.stderr.strip() or "unknown error"
        raise RuntimeError(f"OmniParser command failed: {stderr}")

    raw_text = completed.stdout.strip()
    raw_data = parse_json_loose(raw_text)
    return EngineResult(
        engine="omniparser",
        source=f"omniparser-cmd:{' '.join(command[:-1])}",
        raw_text=raw_text,
        raw_data=raw_data,
    )


def run_markitdown(*, image_path: Path, timeout: int) -> EngineResult:
    command = detect_markitdown_command()
    if not command:
        raise RuntimeError(
            "No extraction engine found. Configure OMNIPARSER_URL or OMNIPARSER_CMD, "
            "or install MarkItDown."
        )

    completed = subprocess.run(
        command + [str(image_path)],
        capture_output=True,
        text=True,
        timeout=timeout,
        check=False,
    )
    if completed.returncode != 0:
        stderr = completed.stderr.strip() or "unknown error"
        raise RuntimeError(f"MarkItDown failed: {stderr}")

    return EngineResult(
        engine="markitdown",
        source=" ".join(command),
        raw_text=completed.stdout.strip(),
        raw_data=None,
    )


def detect_markitdown_command() -> list[str] | None:
    if shutil.which("markitdown"):
        return ["markitdown"]
    if shutil.which("uvx"):
        return ["uvx", "markitdown"]
    return None


def normalize_result(
    *,
    image_path: Path,
    result: EngineResult,
    max_elements: int,
    raw_limit: int,
    include_raw: bool,
) -> str:
    if result.engine == "omniparser" and result.raw_data is not None:
        return normalize_omniparser_markdown(
            image_path=image_path,
            result=result,
            max_elements=max_elements,
            raw_limit=raw_limit,
            include_raw=include_raw,
        )

    if result.engine == "omniparser":
        return normalize_omniparser_text_markdown(
            image_path=image_path,
            result=result,
            raw_limit=raw_limit,
            include_raw=include_raw,
        )

    return normalize_markitdown_markdown(
        image_path=image_path,
        result=result,
        raw_limit=raw_limit,
        include_raw=include_raw,
    )


def normalize_omniparser_markdown(
    *,
    image_path: Path,
    result: EngineResult,
    max_elements: int,
    raw_limit: int,
    include_raw: bool,
) -> str:
    elements = extract_elements(result.raw_data)
    visible_text = extract_visible_text(result.raw_data, limit=max_elements)
    structure = infer_layout_structure(elements, limit=8)
    interaction_cues = infer_interaction_cues(elements, limit=8)
    parser_notes = [
        "Primary engine: OmniParser",
        f"Source: `{result.source}`",
        "Use this as structured screenshot evidence, not as an exact design spec.",
        "Bounds, hierarchy, and control roles are parser-derived and may need manual confirmation.",
    ]

    lines: list[str] = [
        "# Design Context",
        "",
        "## Extraction Summary",
        f"- Source image: `{image_path}`",
        *[f"- {note}" for note in parser_notes],
        f"- Parsed element count: {len(elements)}",
        "",
        "## Visible Text",
    ]

    if visible_text:
        lines.extend(f"- {item}" for item in visible_text)
    else:
        lines.append("- No reliable visible text extracted.")

    lines.extend(["", "## Detected Elements"])
    if elements:
        for element in elements[:max_elements]:
            lines.append(f"- {format_element(element)}")
    else:
        lines.append("- No structured elements were extracted.")

    lines.extend(["", "## Likely Layout Structure"])
    if structure:
        lines.extend(f"- {item}" for item in structure)
    else:
        lines.append("- Layout grouping was not reliable enough to summarize.")

    lines.extend(["", "## Likely Interaction Points"])
    if interaction_cues:
        lines.extend(f"- {item}" for item in interaction_cues)
    else:
        lines.append("- No clear interaction cues were extracted.")

    lines.extend(
        [
            "",
            "## Assumptions And Limits",
            "- This output improves screenshot readability for the agent, but it is still not a Figma spec.",
            "- Exact spacing tokens, font specs, color tokens, and interaction timing cannot be confirmed from parser output alone.",
            "- If the ticket depends on precise UI implementation, keep the original image alongside this note.",
        ]
    )

    if include_raw:
        raw_excerpt = truncate_text(result.raw_text, raw_limit)
        lines.extend(["", "## Raw Parser Output", "```text", raw_excerpt, "```"])

    return "\n".join(lines).strip() + "\n"


def normalize_markitdown_markdown(
    *,
    image_path: Path,
    result: EngineResult,
    raw_limit: int,
    include_raw: bool,
) -> str:
    visible_text = extract_markitdown_lines(result.raw_text, limit=20)
    headings = [line for line in visible_text if len(line.split()) <= 8][:6]

    lines: list[str] = [
        "# Design Context",
        "",
        "## Extraction Summary",
        f"- Source image: `{image_path}`",
        "- Primary engine unavailable. Falling back to MarkItDown OCR.",
        f"- Source: `{result.source}`",
        "- This is text-first extraction. It helps with labels and content, but is weaker on true UI hierarchy.",
        "",
        "## Visible Text",
    ]

    if visible_text:
        lines.extend(f"- {item}" for item in visible_text)
    else:
        lines.append("- No reliable text was extracted.")

    lines.extend(["", "## Likely Layout Structure"])
    if headings:
        lines.extend(f"- Likely text block or heading: {item}" for item in headings)
    else:
        lines.append("- OCR output did not expose a strong layout structure.")

    lines.extend(
        [
            "",
            "## Assumptions And Limits",
            "- This fallback is useful for screen copy, labels, and rough section order.",
            "- It cannot reliably infer exact component boundaries, visual hierarchy, or spacing.",
            "- Keep the original image in the review flow for visual confirmation.",
        ]
    )

    if include_raw:
        raw_excerpt = truncate_text(result.raw_text, raw_limit)
        lines.extend(["", "## Raw OCR Markdown", "```md", raw_excerpt, "```"])

    return "\n".join(lines).strip() + "\n"


def normalize_omniparser_text_markdown(
    *,
    image_path: Path,
    result: EngineResult,
    raw_limit: int,
    include_raw: bool,
) -> str:
    visible_text = extract_markitdown_lines(result.raw_text, limit=20)
    lines: list[str] = [
        "# Design Context",
        "",
        "## Extraction Summary",
        f"- Source image: `{image_path}`",
        "- OmniParser was used, but the output was text-only rather than structured JSON.",
        f"- Source: `{result.source}`",
        "- Treat this as parser-assisted notes, not as a stable UI structure export.",
        "",
        "## Visible Text",
    ]
    if visible_text:
        lines.extend(f"- {item}" for item in visible_text)
    else:
        lines.append("- No reliable text was extracted.")

    lines.extend(
        [
            "",
            "## Assumptions And Limits",
            "- Because the output was not structured JSON, element hierarchy and bounds could not be normalized.",
            "- Keep the original image in the workflow for layout verification.",
        ]
    )
    if include_raw:
        raw_excerpt = truncate_text(result.raw_text, raw_limit)
        lines.extend(["", "## Raw Parser Output", "```text", raw_excerpt, "```"])

    return "\n".join(lines).strip() + "\n"


def extract_elements(data: object) -> list[dict[str, str]]:
    elements: list[dict[str, str]] = []

    def walk(node: object) -> None:
        if isinstance(node, dict):
            record = coerce_element(node)
            if record:
                elements.append(record)
            for value in node.values():
                walk(value)
        elif isinstance(node, list):
            for item in node:
                walk(item)

    walk(data)

    unique: list[dict[str, str]] = []
    seen: set[tuple[str, str, str]] = set()
    for element in elements:
        key = (element.get("kind", ""), element.get("text", ""), element.get("bounds", ""))
        if key in seen:
            continue
        seen.add(key)
        unique.append(element)
    return unique


def coerce_element(node: dict[str, object]) -> dict[str, str] | None:
    kind = first_string(
        node,
        "type",
        "role",
        "kind",
        "class",
        "category",
        "element_type",
        "elementType",
    )
    text = first_string(
        node,
        "text",
        "label",
        "content",
        "description",
        "name",
        "caption",
        "value",
        "title",
    )
    bounds = format_bounds(node.get("bbox") or node.get("bounds") or node.get("box") or node.get("rect"))
    confidence = first_number(node, "score", "confidence", "prob", "probability")

    if not any((kind, text, bounds)):
        return None

    record: dict[str, str] = {}
    if kind:
        record["kind"] = simplify_whitespace(kind)
    if text:
        record["text"] = simplify_whitespace(text)
    if bounds:
        record["bounds"] = bounds
    if confidence is not None:
        record["confidence"] = f"{confidence:.2f}"
    return record


def infer_layout_structure(elements: list[dict[str, str]], limit: int) -> list[str]:
    scored: list[tuple[float, float, str]] = []
    for element in elements:
        bounds = parse_bounds(element.get("bounds", ""))
        if not bounds:
            continue
        x1, y1, x2, y2 = bounds
        label = element.get("text") or element.get("kind") or "unlabeled element"
        scored.append((y1, x1, f"{label} near ({int(x1)},{int(y1)}) to ({int(x2)},{int(y2)})"))

    scored.sort()
    return [item for _, _, item in scored[:limit]]


def infer_interaction_cues(elements: list[dict[str, str]], limit: int) -> list[str]:
    cues = []
    interactive_tokens = ("button", "link", "tab", "input", "field", "checkbox", "radio", "icon")
    for element in elements:
        kind = element.get("kind", "").lower()
        text = element.get("text", "")
        if any(token in kind for token in interactive_tokens):
            cue = text or kind
            suffix = f" [{element['bounds']}]" if element.get("bounds") else ""
            cues.append(f"{kind}: {cue}{suffix}")
    return cues[:limit]


def extract_visible_text(data: object, limit: int) -> list[str]:
    fragments: list[str] = []

    def walk(node: object) -> None:
        if isinstance(node, dict):
            for key, value in node.items():
                if key.lower() in {"text", "label", "content", "description", "name", "title", "caption"}:
                    if isinstance(value, str):
                        fragments.append(value)
                walk(value)
        elif isinstance(node, list):
            for item in node:
                walk(item)

    walk(data)

    unique: list[str] = []
    seen: set[str] = set()
    for fragment in fragments:
        cleaned = simplify_whitespace(fragment)
        if not cleaned or len(cleaned) < 2:
            continue
        key = cleaned.casefold()
        if key in seen:
            continue
        seen.add(key)
        unique.append(cleaned)
    return unique[:limit]


def extract_markitdown_lines(text: str, limit: int) -> list[str]:
    lines = []
    seen: set[str] = set()
    for raw in text.splitlines():
        cleaned = simplify_whitespace(strip_markdown(raw))
        if not cleaned or len(cleaned) < 2:
            continue
        if cleaned.casefold() in seen:
            continue
        seen.add(cleaned.casefold())
        lines.append(cleaned)
        if len(lines) >= limit:
            break
    return lines


def strip_markdown(line: str) -> str:
    return re.sub(r"^[#>*\-\d\.\)\s`]+", "", line).strip()


def format_element(element: dict[str, str]) -> str:
    parts = []
    if element.get("kind"):
        parts.append(element["kind"])
    if element.get("text"):
        parts.append(f'"{element["text"]}"')
    if element.get("confidence"):
        parts.append(f"confidence {element['confidence']}")
    if element.get("bounds"):
        parts.append(f"bounds {element['bounds']}")
    return " | ".join(parts) if parts else "unlabeled element"


def first_string(node: dict[str, object], *keys: str) -> str | None:
    for key in keys:
        value = node.get(key)
        if isinstance(value, str) and value.strip():
            return value
    return None


def first_number(node: dict[str, object], *keys: str) -> float | None:
    for key in keys:
        value = node.get(key)
        if isinstance(value, (int, float)):
            return float(value)
    return None


def format_bounds(value: object) -> str | None:
    if isinstance(value, (list, tuple)) and len(value) >= 4:
        try:
            x1, y1, x2, y2 = [float(item) for item in value[:4]]
        except (TypeError, ValueError):
            return None
        return f"{x1:.0f},{y1:.0f},{x2:.0f},{y2:.0f}"
    if isinstance(value, dict):
        keys = [value.get(key) for key in ("x1", "y1", "x2", "y2")]
        if all(isinstance(item, (int, float)) for item in keys):
            x1, y1, x2, y2 = [float(item) for item in keys]
            return f"{x1:.0f},{y1:.0f},{x2:.0f},{y2:.0f}"
    if isinstance(value, str) and value.strip():
        return value.strip()
    return None


def parse_bounds(bounds: str) -> tuple[float, float, float, float] | None:
    match = re.fullmatch(r"\s*(-?\d+(?:\.\d+)?),(-?\d+(?:\.\d+)?),(-?\d+(?:\.\d+)?),(-?\d+(?:\.\d+)?)\s*", bounds)
    if not match:
        return None
    return tuple(float(group) for group in match.groups())  # type: ignore[return-value]


def parse_json_loose(raw_text: str) -> object | None:
    raw_text = raw_text.strip()
    if not raw_text:
        return None
    try:
        return json.loads(raw_text)
    except json.JSONDecodeError:
        pass

    fenced_match = re.search(r"```json\s*(.*?)```", raw_text, re.DOTALL | re.IGNORECASE)
    if fenced_match:
        candidate = fenced_match.group(1).strip()
        try:
            return json.loads(candidate)
        except json.JSONDecodeError:
            return None

    start = raw_text.find("{")
    end = raw_text.rfind("}")
    if start != -1 and end != -1 and end > start:
        candidate = raw_text[start : end + 1]
        try:
            return json.loads(candidate)
        except json.JSONDecodeError:
            return None
    return None


def truncate_text(text: str, raw_limit: int) -> str:
    if len(text) <= raw_limit:
        return text
    return text[: raw_limit - 13].rstrip() + "\n...[truncated]"


def simplify_whitespace(value: str) -> str:
    return re.sub(r"\s+", " ", value).strip()


def render_missing_engine_note(image_path: Path, detail: str) -> str:
    return "\n".join(
        [
            "# Design Context",
            "",
            "## Extraction Summary",
            f"- Source image: `{image_path}`",
            "- No supported parser was available in this environment.",
            f"- Detail: {detail}",
            "",
            "## Setup Guidance",
            "- Recommended primary engine: Microsoft OmniParser.",
            "- Configure `OMNIPARSER_URL` to a local OmniParser-style API endpoint, or `OMNIPARSER_CMD` to a local wrapper command that prints JSON to stdout.",
            "- Recommended fallback engine: install MarkItDown with `pip install 'markitdown[all]'`, or ensure `uvx markitdown` works on this machine.",
            "- After setup, rerun `python3 scripts/extract_design_context.py path/to/image.png --include-raw`.",
        ]
    )


if __name__ == "__main__":
    raise SystemExit(main())
