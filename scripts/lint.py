#!/usr/bin/env python3
from __future__ import annotations

import re
import sys
from collections import defaultdict
from pathlib import Path

LIST_FILE = Path(__file__).resolve().parent.parent / "apps-direct.list"

RULE_RE = re.compile(
    r"^(PROCESS-NAME),"
    r"([^\s,]+),"
    r"(DIRECT|REJECT|PROXY)$"
)

NAME_MAX_LEN = 255


def validate_name(name: str) -> str | None:
    if not name:
        return "empty process name"
    if len(name) > NAME_MAX_LEN:
        return f"process name too long (>{NAME_MAX_LEN} chars)"
    if any(c in name for c in "\t\n\r"):
        return "contains whitespace or control character"
    return None


def main() -> int:
    if not LIST_FILE.exists():
        print(f"❌ Rule file not found: {LIST_FILE}", file=sys.stderr)
        return 1

    text = LIST_FILE.read_text(encoding="utf-8")
    lines = text.splitlines()

    errors: list[str] = []
    warnings: list[str] = []
    seen: dict[tuple[str, str], int] = {}
    rule_count = 0
    category_counts: dict[str, int] = defaultdict(int)
    current_category = "(uncategorized)"

    for lineno, raw in enumerate(lines, 1):
        line = raw.rstrip()
        stripped = line.strip()

        if not stripped:
            continue

        if stripped.startswith("#"):
            cat_match = re.match(r"^#\s*===\s*(.+?)\s*===\s*$", stripped)
            if cat_match:
                current_category = cat_match.group(1)
            continue

        if line != line.rstrip():
            warnings.append(f"line {lineno}: trailing whitespace")

        match = RULE_RE.match(stripped)
        if not match:
            errors.append(f"line {lineno}: malformed rule: {stripped!r}")
            continue

        rule_type, name, target = match.groups()

        name_error = validate_name(name)
        if name_error:
            errors.append(f"line {lineno}: {name_error}: {name!r}")
            continue

        key = (rule_type, name)
        if key in seen:
            errors.append(
                f"line {lineno}: duplicate {rule_type},{name} "
                f"(first at line {seen[key]})"
            )
            continue
        seen[key] = lineno

        rule_count += 1
        category_counts[current_category] += 1

    print(f"✓ Validated {LIST_FILE.name}")
    print(f"  Total rules: {rule_count}")
    print(f"  Categories ({len(category_counts)}):")
    for cat, n in sorted(category_counts.items(), key=lambda kv: (-kv[1], kv[0])):
        print(f"    - {cat}: {n}")

    if warnings:
        print(f"\n⚠ {len(warnings)} warning(s):")
        for w in warnings:
            print(f"  {w}")

    if errors:
        print(f"\n❌ {len(errors)} error(s):", file=sys.stderr)
        for e in errors:
            print(f"  {e}", file=sys.stderr)
        return 1

    print("\n✓ All checks passed")
    return 0


if __name__ == "__main__":
    sys.exit(main())
