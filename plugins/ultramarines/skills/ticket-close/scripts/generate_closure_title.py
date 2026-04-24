#!/usr/bin/env python3
"""Generate a standard ticket closure title string."""

from __future__ import annotations

import argparse
import re
import sys


TYPE_MAP = {
    "bug": "fix",
    "defect": "fix",
    "incident": "hotfix",
    "production bug": "hotfix",
    "feature": "feat",
    "story": "feat",
    "task": "chore",
    "maintenance": "chore",
    "internal cleanup": "chore",
    "refactor": "refactor",
    "tech debt": "refactor",
}


def main() -> int:
    parser = argparse.ArgumentParser(description="Generate 'type: TICKET-ID | summary'")
    parser.add_argument("--ticket-id", required=True, help="Jira ticket ID, for example ML-39")
    parser.add_argument("--summary", required=True, help="Short action-oriented summary")
    parser.add_argument("--issue-type", default="", help="Issue category from Jira, for example bug or feature")
    parser.add_argument("--type", dest="forced_type", default="", help="Explicit override for output type")
    args = parser.parse_args()

    output_type = infer_type(args.issue_type, args.forced_type)
    summary = normalize_summary(args.summary)
    print(f"{output_type}: {args.ticket_id} | {summary}")
    return 0


def infer_type(issue_type: str, forced_type: str) -> str:
    if forced_type:
        return forced_type.strip().lower()
    lowered = issue_type.strip().lower()
    if lowered in TYPE_MAP:
        return TYPE_MAP[lowered]
    if "bug" in lowered:
        return "fix"
    if "feature" in lowered:
        return "feat"
    return "fix"


def normalize_summary(summary: str) -> str:
    compact = " ".join(summary.strip().split())
    compact = re.sub(r"\s*\|\s*", " ", compact)
    if not compact:
        raise SystemExit("summary must not be empty")
    return compact[0].lower() + compact[1:] if len(compact) > 1 else compact.lower()


if __name__ == "__main__":
    sys.exit(main())
