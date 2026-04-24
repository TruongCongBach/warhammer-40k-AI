#!/usr/bin/env python3
"""Review current git changes and recommend a conservative scoped commit set."""

from __future__ import annotations

import argparse
import re
import subprocess
import sys
from pathlib import Path


SUSPICIOUS_NAMES = {
    "package-lock.json",
    "yarn.lock",
    "pnpm-lock.yaml",
    "Podfile.lock",
}
SUSPICIOUS_PARTS = {
    ".idea",
    ".vscode",
    "__pycache__",
    "dist",
    "build",
    ".next",
    "Pods",
}
SUSPICIOUS_SUFFIXES = {
    ".log",
    ".tmp",
    ".zip",
    ".har",
    ".png",
    ".jpg",
    ".jpeg",
}
STOPWORDS = {
    "the",
    "and",
    "for",
    "with",
    "from",
    "that",
    "this",
    "into",
    "after",
    "before",
    "issue",
    "ticket",
    "screen",
    "state",
}
IGNORED_PARTS = {"__pycache__"}
IGNORED_SUFFIXES = {".pyc", ".pyo"}
IGNORED_NAMES = {".DS_Store"}


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Inspect git changes and recommend files for a conservative issue-scoped commit."
    )
    parser.add_argument("--ticket-id", default="", help="Jira ticket ID, for example ML-39")
    parser.add_argument("--summary", default="", help="Issue summary or short commit summary")
    parser.add_argument(
        "--keywords",
        nargs="*",
        default=[],
        help="Extra keywords to help score relevance",
    )
    parser.add_argument(
        "--stage",
        action="store_true",
        help="Stage recommended files with git add -- <paths>",
    )
    args = parser.parse_args()

    changes = collect_changes()
    if not changes:
        print("No changed files detected.")
        return 0

    tokens = build_tokens(args.ticket_id, args.summary, args.keywords)
    recommended: list[dict] = []
    needs_review: list[dict] = []

    for change in changes:
        score, reasons = score_change(change["path"], tokens)
        suspicious_reasons = suspicious_flags(change["path"])
        if suspicious_reasons:
            reasons.extend(suspicious_reasons)

        item = {
            "status": change["status"],
            "path": change["path"],
            "score": score,
            "reasons": reasons,
        }

        if score >= 3 and not suspicious_reasons:
            recommended.append(item)
        else:
            needs_review.append(item)

    print("Changed files detected:")
    for change in changes:
        print(f"- {change['status']} {change['path']}")

    print("\nFiles recommended for commit:")
    if recommended:
        for item in recommended:
            reason_text = "; ".join(item["reasons"]) if item["reasons"] else "path matched issue scope"
            print(f"- {item['path']} ({reason_text})")
    else:
        print("- none")

    print("\nFiles excluded or needing review:")
    if needs_review:
        for item in needs_review:
            reason_text = "; ".join(item["reasons"]) if item["reasons"] else "low confidence relevance"
            print(f"- {item['path']} ({reason_text})")
    else:
        print("- none")

    if recommended:
        add_command = "git add -- " + " ".join(shell_quote(item["path"]) for item in recommended)
        print("\nSuggested staging command:")
        print(add_command)
    else:
        print("\nSuggested staging command:")
        print("# no safe files to stage automatically")

    final_recommendation = (
        "safe to commit" if recommended and not needs_review else "review needed"
    )
    print(f"\nFinal recommendation: {final_recommendation}")

    if args.stage:
        if not recommended or needs_review:
            raise SystemExit("Refusing to stage automatically because review is still needed.")
        run_git(["add", "--", *[item["path"] for item in recommended]])
        print("Staged recommended files.")

    return 0


def collect_changes() -> list[dict]:
    output = run_git(["status", "--short"])
    changes = []
    for raw_line in output.splitlines():
        if not raw_line.strip():
            continue
        status = raw_line[:2].strip() or "??"
        path = raw_line[3:].strip()
        if " -> " in path:
            path = path.split(" -> ", 1)[1]
        path_obj = Path(path)
        if status == "??" and path_obj.is_dir():
            for nested in sorted(item for item in path_obj.rglob("*") if item.is_file()):
                if should_skip(nested):
                    continue
                changes.append({"status": status, "path": str(nested)})
            continue
        if should_skip(path_obj):
            continue
        changes.append({"status": status, "path": path})
    return changes


def build_tokens(ticket_id: str, summary: str, extra_keywords: list[str]) -> set[str]:
    text = " ".join(part for part in [ticket_id, summary, " ".join(extra_keywords)] if part)
    base_tokens = {
        token.lower()
        for token in re.findall(r"[a-zA-Z][a-zA-Z0-9_-]+", text)
        if len(token) > 2
    }
    return {token for token in base_tokens if token not in STOPWORDS}


def score_change(path: str, tokens: set[str]) -> tuple[int, list[str]]:
    lowered = path.lower()
    score = 0
    reasons: list[str] = []

    for token in sorted(tokens):
        if token in lowered:
            score += 2
            reasons.append(f"matched token '{token}'")

    if any(part in lowered for part in ("screen", "screens", "component", "components", "page", "app/")):
        score += 1
        reasons.append("changed path looks product-facing")
    if any(part in lowered for part in ("hook", "store", "service", "api", "navigation")):
        score += 1
        reasons.append("changed path looks issue-relevant infrastructure")

    return score, reasons


def suspicious_flags(path: str) -> list[str]:
    path_obj = Path(path)
    flags = []
    if path_obj.name in SUSPICIOUS_NAMES:
        flags.append("suspicious lockfile or package manifest companion")
    if any(part in SUSPICIOUS_PARTS for part in path_obj.parts):
        flags.append("suspicious generated, workspace, or build path")
    if path_obj.suffix.lower() in SUSPICIOUS_SUFFIXES:
        flags.append("suspicious artifact or binary-like file")
    return flags


def should_skip(path_obj: Path) -> bool:
    if any(part in IGNORED_PARTS for part in path_obj.parts):
        return True
    if path_obj.suffix.lower() in IGNORED_SUFFIXES:
        return True
    if path_obj.name in IGNORED_NAMES:
        return True
    return False


def run_git(args: list[str]) -> str:
    result = subprocess.run(
        ["git", *args],
        check=True,
        capture_output=True,
        text=True,
    )
    return result.stdout


def shell_quote(text: str) -> str:
    if re.fullmatch(r"[-_./a-zA-Z0-9]+", text):
        return text
    return "'" + text.replace("'", "'\"'\"'") + "'"


if __name__ == "__main__":
    sys.exit(main())
