#!/usr/bin/env python3
"""Validate compound-unity docs/solutions/ frontmatter parser-safety issues.

Usage:
    python validate-frontmatter.py <doc-path>

Exit codes:
    0 - frontmatter passes all checks
    1 - validation failure (diagnostics on stderr)
    2 - usage error (bad arguments, missing file)

Scope: this script catches parser-safety issues: frontmatter that strict YAML
parsers will silently misread. It does NOT validate against the schema's
required-field or enum-value rules; that is a separate concern. The intent is
to prevent silent data loss where YAML quoting rules truncate or reframe scalar
values without raising.

Checks (regex-based, no YAML parser dependency):
    1. File starts and ends frontmatter with `---` lines matched as full lines.
    2. No top-level scalar value contains ` #` unquoted.
    3. No top-level scalar value contains `: ` unquoted.
    4. No array-of-strings item starts with a reserved indicator unquoted.
    5. No array-of-strings item contains ` #` or `: ` unquoted.
    6. No top-level scalar value starts with a reserved indicator unquoted.
    7. No non-array scalar field uses flow-array syntax unquoted.
"""
import os
import re
import sys

RESERVED_ARRAY_ITEM_STARTS = set("-?:,[]{}#&*!|>'\"%@`")
FLOW_ARRAY_FIELDS = {
    "symptoms",
    "applies_when",
    "tags",
    "related_components",
    "evidence",
}


def is_quoted(value: str) -> bool:
    return bool(value) and value[0] in "\"'"


def split_flow_items(value: str) -> list[str]:
    inner = value.strip()[1:-1]
    items: list[str] = []
    current: list[str] = []
    quote: str | None = None
    escape = False

    for char in inner:
        if escape:
            current.append(char)
            escape = False
            continue
        if char == "\\" and quote == '"':
            current.append(char)
            escape = True
            continue
        if quote:
            current.append(char)
            if char == quote:
                quote = None
            continue
        if char in "\"'":
            current.append(char)
            quote = char
            continue
        if char == ",":
            items.append("".join(current).strip())
            current = []
            continue
        current.append(char)

    items.append("".join(current).strip())
    return [item for item in items if item]


def validate_array_item(item: str, lineno: int, issues: list[str], context: str = "array item") -> None:
    if not item or is_quoted(item):
        return
    if item[0] in RESERVED_ARRAY_ITEM_STARTS:
        issues.append(
            f"line {lineno}: {context} starts with '{item[0]}' - quote it. "
            "YAML may parse the item as a non-string value or nested structure."
        )
    if re.search(r"\s#", item):
        issues.append(
            f"line {lineno}: {context} contains ' #' - quote it. "
            "YAML treats space-then-# as a comment delimiter and silently "
            "drops the rest of the value."
        )
    if re.search(r":\s", item):
        issues.append(
            f"line {lineno}: {context} contains ': ' - quote it. "
            "Strict YAML parsers may treat this as a nested mapping."
        )


def usage_fail(msg: str) -> "NoReturn":
    sys.stderr.write(f"validate-frontmatter: {msg}\n")
    sys.exit(2)


def main(argv: list[str]) -> int:
    if len(argv) != 2:
        usage_fail(f"usage: {os.path.basename(argv[0])} <doc-path>")

    doc_path = argv[1]
    if not os.path.isfile(doc_path):
        usage_fail(f"file not found: {doc_path}")

    with open(doc_path, encoding="utf-8-sig") as f:
        text = f.read()

    issues: list[str] = []

    lines = text.split("\n")
    if not lines or lines[0].rstrip() != "---":
        sys.stderr.write(
            f"FAIL: {doc_path}\n"
            f"  file does not start with '---' frontmatter delimiter line\n"
        )
        return 1

    end_idx: int | None = None
    for i in range(1, len(lines)):
        if lines[i].rstrip() == "---":
            end_idx = i
            break

    if end_idx is None:
        sys.stderr.write(
            f"FAIL: {doc_path}\n"
            f"  frontmatter not closed (no '---' line after the opening delimiter)\n"
        )
        return 1

    fm_text = "\n".join(lines[1:end_idx])

    for lineno, line in enumerate(fm_text.split("\n"), start=2):
        stripped = line.lstrip()
        if not stripped or stripped.startswith("#"):
            continue

        if stripped.startswith("- "):
            item = stripped[2:].strip()
            validate_array_item(item, lineno, issues)
            continue

        if ":" not in line:
            continue
        if line.startswith((" ", "\t")):
            continue

        key, _, val = line.partition(":")
        key_name = key.strip()
        val_stripped = val.strip()
        if not val_stripped:
            continue
        if val_stripped.startswith("[") and val_stripped.endswith("]"):
            if key_name not in FLOW_ARRAY_FIELDS:
                issues.append(
                    f"line {lineno}: '{key_name}' value starts with '[' - quote it "
                    "or use an array field. YAML parses unquoted brackets as a flow array."
                )
                continue
            for item in split_flow_items(val_stripped):
                validate_array_item(item, lineno, issues, f"flow array item for '{key_name}'")
            continue

        if val_stripped[0] in '"\'':
            continue
        if val_stripped[0] in RESERVED_ARRAY_ITEM_STARTS:
            issues.append(
                f"line {lineno}: '{key_name}' value starts with '{val_stripped[0]}' - quote it. "
                "YAML may parse the value as a non-string value or reject it."
            )

        if re.search(r"\s#", val_stripped):
            issues.append(
                f"line {lineno}: '{key_name}' value contains ' #' - quote it. "
                "YAML treats space-then-# as a comment delimiter and silently "
                "drops the rest of the value."
            )
        if re.search(r":\s", val_stripped):
            issues.append(
                f"line {lineno}: '{key_name}' value contains ': ' - quote it. "
                "Strict YAML parsers may treat this as a nested mapping."
            )

    if issues:
        sys.stderr.write(f"FAIL: {doc_path}\n")
        for issue in issues:
            sys.stderr.write(f"  {issue}\n")
        return 1

    print(f"OK: {doc_path}")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
