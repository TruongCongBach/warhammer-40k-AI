#!/usr/bin/env python3
"""Inspect HAR, Charles, zip, JSON, and text artifacts for ticket triage."""

from __future__ import annotations

import argparse
import json
import mimetypes
import os
import re
import sys
import tempfile
import zipfile
from collections import Counter
from pathlib import Path
from typing import Iterable
from urllib.parse import parse_qsl, urlsplit, urlunsplit


ERROR_WORDS = ("error", "exception", "fail", "timeout", "denied", "unauthorized")
HTTP_METHODS = {"GET", "POST", "PUT", "PATCH", "DELETE", "HEAD", "OPTIONS"}


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Summarize ticket artifacts such as HAR, zip, JSON, text logs, and Charles exports."
    )
    parser.add_argument("paths", nargs="+", help="Artifact paths to inspect")
    parser.add_argument("--slow-ms", type=int, default=1000, help="Threshold for slow requests")
    parser.add_argument("--top", type=int, default=5, help="Maximum rows per summary section")
    args = parser.parse_args()

    for raw_path in args.paths:
        path = Path(raw_path).expanduser()
        print(f"== {path} ==")
        if not path.exists():
            print("missing: file not found")
            print()
            continue
        summarize_path(path, slow_ms=args.slow_ms, top=args.top)
        print()
    return 0


def summarize_path(path: Path, slow_ms: int, top: int) -> None:
    kind = detect_kind(path)
    print(f"type: {kind}")

    if kind == "zip":
        summarize_zip(path, slow_ms=slow_ms, top=top)
        return
    if kind == "har":
        summarize_har_file(path, slow_ms=slow_ms, top=top)
        return
    if kind in {"json", "charles-json"}:
        summarize_json_file(path, slow_ms=slow_ms, top=top)
        return
    if kind in {"text", "xml", "charles-session", "charles-trace"}:
        summarize_text_file(path, top=top)
        return

    mime, _ = mimetypes.guess_type(path.name)
    print(f"note: unsupported or opaque artifact; mime={mime or 'unknown'}")


def detect_kind(path: Path) -> str:
    suffix = path.suffix.lower()
    if zipfile.is_zipfile(path):
        return "zip"
    if suffix == ".har":
        return "har"
    if suffix in {".json", ".har.json"}:
        return "json"
    if suffix in {".log", ".txt", ".out"}:
        return "text"
    if suffix == ".xml":
        return "xml"
    if suffix == ".chls":
        return "charles-session"
    if suffix == ".chlsj":
        return "charles-json"
    if suffix == ".trace":
        return "charles-trace"
    return "unknown"


def summarize_zip(path: Path, slow_ms: int, top: int) -> None:
    with tempfile.TemporaryDirectory(prefix="ticket-analysis-") as tmpdir:
        with zipfile.ZipFile(path) as archive:
            archive.extractall(tmpdir)
            names = archive.namelist()
        print(f"archive entries: {len(names)}")
        for name in names[:top]:
            print(f"- {name}")
        extracted_paths = [p for p in Path(tmpdir).rglob("*") if p.is_file()]
        if not extracted_paths:
            print("note: archive contained no files")
            return
        print("nested summary:")
        for nested in extracted_paths[:top]:
            print(f"-- {nested.relative_to(tmpdir)}")
            summarize_path(nested, slow_ms=slow_ms, top=top)


def summarize_har_file(path: Path, slow_ms: int, top: int) -> None:
    with path.open("r", encoding="utf-8", errors="replace") as handle:
        data = json.load(handle)
    summarize_har_data(data, slow_ms=slow_ms, top=top)


def summarize_json_file(path: Path, slow_ms: int, top: int) -> None:
    with path.open("r", encoding="utf-8", errors="replace") as handle:
        data = json.load(handle)

    if is_har_like(data):
        print("json shape: HAR-like")
        summarize_har_data(data, slow_ms=slow_ms, top=top)
        return

    flattened = json.dumps(data, ensure_ascii=False)[:4000]
    print("json shape: generic")
    print("error signatures:")
    for line in extract_error_snippets(flattened.splitlines(), top=top):
        print(f"- {line}")
    suspicious = find_suspicious_strings(flattened)
    if suspicious:
        print("suspicious fields:")
        for item in suspicious[:top]:
            print(f"- {item}")
    else:
        print("suspicious fields: none detected")


def summarize_text_file(path: Path, top: int) -> None:
    with path.open("r", encoding="utf-8", errors="replace") as handle:
        lines = handle.readlines()

    print(f"line count: {len(lines)}")
    print("error signatures:")
    snippets = extract_error_snippets(lines, top=top)
    if snippets:
        for line in snippets:
            print(f"- {line}")
    else:
        print("- none detected")

    urls = extract_urls(lines)
    if urls:
        print("request patterns:")
        for url, count in Counter(urls).most_common(top):
            print(f"- {url} x{count}")


def is_har_like(data: object) -> bool:
    return isinstance(data, dict) and isinstance(data.get("log"), dict) and isinstance(data["log"].get("entries"), list)


def summarize_har_data(data: dict, slow_ms: int, top: int) -> None:
    entries = data.get("log", {}).get("entries", [])
    print(f"request count: {len(entries)}")
    rows = []
    duplicates = Counter()
    suspicious = Counter()
    boundaries = Counter()

    for entry in entries:
        request = entry.get("request", {})
        response = entry.get("response", {})
        method = str(request.get("method", "UNKNOWN")).upper()
        url = str(request.get("url", ""))
        normalized_url = normalize_url(url)
        status = int(response.get("status", 0) or 0)
        time_ms = int(entry.get("time", 0) or 0)
        rows.append((method, normalized_url, status, time_ms))
        duplicates[(method, normalized_url)] += 1
        boundaries[infer_boundary(status, url)] += 1

        payload = request.get("postData", {}).get("text", "")
        for flag in suspicious_payload_flags(payload):
            suspicious[flag] += 1

    failed = [row for row in rows if row[2] >= 400 or row[2] == 0]
    slow = [row for row in rows if row[3] >= slow_ms]
    dupes = [(method, url, count) for (method, url), count in duplicates.items() if count > 1]

    print("failed requests:")
    if failed:
        for method, url, status, time_ms in failed[:top]:
            print(f"- {method} {url} -> {status} ({time_ms} ms)")
    else:
        print("- none")

    print("slow requests:")
    if slow:
        slow_sorted = sorted(slow, key=lambda item: item[3], reverse=True)
        for method, url, status, time_ms in slow_sorted[:top]:
            print(f"- {method} {url} -> {time_ms} ms (status {status})")
    else:
        print("- none")

    print("duplicate requests:")
    if dupes:
        dupes_sorted = sorted(dupes, key=lambda item: item[2], reverse=True)
        for method, url, count in dupes_sorted[:top]:
            print(f"- {method} {url} x{count}")
    else:
        print("- none")

    print("suspicious payloads:")
    if suspicious:
        for label, count in suspicious.most_common(top):
            print(f"- {label} x{count}")
    else:
        print("- none detected")

    print("likely system boundary:")
    for label, count in boundaries.most_common(top):
        print(f"- {label} x{count}")


def normalize_url(url: str) -> str:
    split = urlsplit(url)
    path = re.sub(r"/\d+\b", "/:id", split.path or "")
    query_items = sorted((key, "<value>") for key, _ in parse_qsl(split.query, keep_blank_values=True))
    query = "&".join(f"{key}={value}" for key, value in query_items)
    return urlunsplit((split.scheme, split.netloc, path, query, ""))


def infer_boundary(status: int, url: str) -> str:
    if status in {401, 403}:
        return "auth"
    if status >= 500:
        return "backend"
    if status >= 400:
        return "frontend-or-request-shape"
    if "staging" in url and "prod" in url:
        return "config"
    return "unknown"


def suspicious_payload_flags(payload: str) -> list[str]:
    if not payload:
        return []
    flags = []
    lowered = payload.lower()
    if '"id":null' in lowered or '"id": null' in lowered:
        flags.append("null id")
    if '""' in payload:
        flags.append("empty string value")
    if '"token":null' in lowered or '"token": null' in lowered:
        flags.append("null token")
    if "undefined" in lowered:
        flags.append("undefined value")
    return flags


def extract_error_snippets(lines: Iterable[str], top: int) -> list[str]:
    snippets = []
    for raw in lines:
        line = raw.strip()
        lowered = line.lower()
        if any(word in lowered for word in ERROR_WORDS):
            snippets.append(line[:240])
        if len(snippets) >= top:
            break
    return snippets


def extract_urls(lines: Iterable[str]) -> list[str]:
    pattern = re.compile(r"https?://[^\s\"'>]+")
    urls = []
    for raw in lines:
        for match in pattern.findall(raw):
            urls.append(normalize_url(match))
    return urls


def find_suspicious_strings(text: str) -> list[str]:
    checks = [
        ("null id", r'"id"\s*:\s*null'),
        ("null token", r'"token"\s*:\s*null'),
        ("empty array", r':\s*\[\s*\]'),
        ("undefined literal", r'undefined'),
    ]
    hits = []
    for label, pattern in checks:
        if re.search(pattern, text, flags=re.IGNORECASE):
            hits.append(label)
    return hits


if __name__ == "__main__":
    sys.exit(main())
