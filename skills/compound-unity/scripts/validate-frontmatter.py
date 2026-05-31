#!/usr/bin/env python3
"""Validate compound-unity docs/solutions/ frontmatter safety and schema basics.

Usage:
    python validate-frontmatter.py <doc-path>

Exit codes:
    0 - frontmatter passes all checks
    1 - validation failure (diagnostics on stderr)
    2 - usage error (bad arguments, missing file)

Scope: this script catches parser-safety issues and the schema basics that are
cheap to verify without a YAML dependency: required fields, enum values, date
format, track-specific required fields, category mapping, and array counts.

Checks (regex-based, no YAML parser dependency):
    1. File starts and ends frontmatter with `---` lines matched as full lines.
    2. No top-level scalar value contains ` #` unquoted.
    3. No top-level scalar value contains `: ` unquoted.
    4. No array-of-strings item starts with a reserved indicator unquoted.
    5. No array-of-strings item contains ` #` or `: ` unquoted.
    6. No top-level scalar value starts with a reserved indicator unquoted.
    7. No non-array scalar field uses flow-array syntax unquoted.
    8. Required fields and enum values match references/schema.yaml.
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
REQUIRED_FIELDS = {
    "title",
    "date",
    "category",
    "module",
    "problem_type",
    "component",
    "severity",
}
BUG_PROBLEM_TYPES = {
    "build_error",
    "test_failure",
    "runtime_error",
    "performance_issue",
    "database_issue",
    "security_issue",
    "ui_bug",
    "integration_issue",
    "logic_error",
}
KNOWLEDGE_PROBLEM_TYPES = {
    "developer_experience",
    "workflow_issue",
    "best_practice",
    "documentation_gap",
    "architecture_pattern",
    "design_pattern",
    "tooling_decision",
    "convention",
}
PROBLEM_TYPES = BUG_PROBLEM_TYPES | KNOWLEDGE_PROBLEM_TYPES
PROBLEM_CATEGORIES = {
    "build_error": "docs/solutions/build-errors",
    "test_failure": "docs/solutions/test-failures",
    "runtime_error": "docs/solutions/runtime-errors",
    "performance_issue": "docs/solutions/performance-issues",
    "database_issue": "docs/solutions/database-issues",
    "security_issue": "docs/solutions/security-issues",
    "ui_bug": "docs/solutions/ui-bugs",
    "integration_issue": "docs/solutions/integration-issues",
    "logic_error": "docs/solutions/logic-errors",
    "developer_experience": "docs/solutions/developer-experience",
    "workflow_issue": "docs/solutions/workflow-issues",
    "best_practice": "docs/solutions/best-practices",
    "documentation_gap": "docs/solutions/documentation-gaps",
    "architecture_pattern": "docs/solutions/architecture-patterns",
    "design_pattern": "docs/solutions/design-patterns",
    "tooling_decision": "docs/solutions/tooling-decisions",
    "convention": "docs/solutions/conventions",
}
COMPONENTS = {
    "editor_bridge",
    "bridge_tooling",
    "unity_mcp",
    "codex_config",
    "editor_workflow",
    "scene",
    "prefab",
    "script",
    "asmdef",
    "package",
    "project_settings",
    "input_system",
    "physics",
    "animation",
    "ui",
    "rendering",
    "tests_editmode",
    "tests_playmode",
    "scriptable_object",
    "asset_pipeline",
    "documentation",
    "development_workflow",
    "unity_editor",
    "navmesh",
    "vehicle",
    "interaction_system",
    "damage_system",
    "state_machine",
    "verification",
    "tooling",
}
SEVERITIES = {"critical", "high", "medium", "low"}
EDITOR_BRIDGES = {"unity_ai_assistant", "mcpforunity"}
ROOT_CAUSES = {
    "active_target_drift",
    "stale_bridge_tools",
    "stale_mcp_tools",
    "incomplete_editor_setup",
    "compile_error",
    "domain_reload_timing",
    "console_error",
    "missing_serialized_reference",
    "prefab_override_conflict",
    "scene_dirty_state",
    "guid_mismatch",
    "missing_meta_file",
    "asmdef_reference_missing",
    "package_dependency_missing",
    "manifest_mismatch",
    "editor_runtime_boundary",
    "fixed_update_timing",
    "animation_event_mismatch",
    "animator_parameter_mismatch",
    "input_action_miswired",
    "asset_load_path_wrong",
    "scriptable_object_reference_missing",
    "missing_scene_wiring",
    "insufficient_verification",
    "architecture_coupling",
    "missing_workflow_step",
    "inadequate_documentation",
    "missing_tooling",
    "incomplete_setup",
    "wrong_api",
    "logic_error",
}
RESOLUTION_TYPES = {
    "bridge_retarget",
    "unity_mcp_retarget",
    "editor_setup_change",
    "code_fix",
    "scene_wiring_change",
    "prefab_wiring_change",
    "serialization_fix",
    "meta_guid_restore",
    "asmdef_reference_change",
    "package_manifest_change",
    "config_change",
    "test_fix",
    "playmode_fix",
    "editmode_fix",
    "dependency_update",
    "environment_setup",
    "workflow_improvement",
    "documentation_update",
    "tooling_addition",
    "architecture_refactor",
    "verification_update",
    "workaround",
}


def is_quoted(value: str) -> bool:
    return bool(value) and value[0] in "\"'"


def unquote(value: str) -> str:
    value = value.strip()
    if len(value) >= 2 and value[0] == value[-1] and value[0] in "\"'":
        return value[1:-1]
    return value


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


def check_enum(field: str, value: str, allowed: set[str], issues: list[str]) -> None:
    if value and value not in allowed:
        issues.append(
            f"'{field}' has invalid value '{value}'. Allowed: {', '.join(sorted(allowed))}."
        )


def validate_schema_fields(scalars: dict[str, str], arrays: dict[str, list[str]], issues: list[str]) -> None:
    for field in sorted(REQUIRED_FIELDS):
        if field not in scalars or not scalars[field]:
            issues.append(f"missing required field '{field}'")

    if "date" in scalars and not re.fullmatch(r"\d{4}-\d{2}-\d{2}", scalars["date"]):
        issues.append("'date' must match YYYY-MM-DD")

    problem_type = scalars.get("problem_type", "")
    check_enum("problem_type", problem_type, PROBLEM_TYPES, issues)
    check_enum("component", scalars.get("component", ""), COMPONENTS, issues)
    check_enum("severity", scalars.get("severity", ""), SEVERITIES, issues)
    if "editor_bridge" in scalars:
        check_enum("editor_bridge", scalars["editor_bridge"], EDITOR_BRIDGES, issues)

    expected_category = PROBLEM_CATEGORIES.get(problem_type)
    category = scalars.get("category", "").rstrip("/")
    if expected_category and category != expected_category:
        issues.append(
            f"'category' must be '{expected_category}' for problem_type '{problem_type}'"
        )

    if problem_type in BUG_PROBLEM_TYPES:
        for field in ("symptoms", "root_cause", "resolution_type"):
            has_field = field in arrays if field == "symptoms" else field in scalars
            if not has_field:
                issues.append(f"bug-track problem_type requires '{field}'")

    if "root_cause" in scalars:
        check_enum("root_cause", scalars["root_cause"], ROOT_CAUSES, issues)
    if "resolution_type" in scalars:
        check_enum("resolution_type", scalars["resolution_type"], RESOLUTION_TYPES, issues)

    array_limits = {
        "symptoms": (1 if problem_type in BUG_PROBLEM_TYPES else 0, 6),
        "applies_when": (0, 6),
        "tags": (0, 10),
        "evidence": (0, 8),
    }
    for field, (minimum, maximum) in array_limits.items():
        if field not in arrays:
            continue
        count = len(arrays[field])
        if count < minimum:
            issues.append(f"'{field}' must contain at least {minimum} item(s)")
        if count > maximum:
            issues.append(f"'{field}' must contain at most {maximum} item(s)")


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
    scalars: dict[str, str] = {}
    arrays: dict[str, list[str]] = {}
    current_array_key: str | None = None

    for lineno, line in enumerate(fm_text.split("\n"), start=2):
        stripped = line.lstrip()
        if not stripped or stripped.startswith("#"):
            continue

        if stripped.startswith("- "):
            item = stripped[2:].strip()
            validate_array_item(item, lineno, issues)
            if current_array_key:
                arrays.setdefault(current_array_key, []).append(unquote(item))
            continue

        if ":" not in line:
            continue
        if line.startswith((" ", "\t")):
            continue

        key, _, val = line.partition(":")
        key_name = key.strip()
        val_stripped = val.strip()
        current_array_key = None
        if not val_stripped:
            if key_name in FLOW_ARRAY_FIELDS:
                current_array_key = key_name
                arrays.setdefault(key_name, [])
            continue
        if val_stripped.startswith("[") and val_stripped.endswith("]"):
            if key_name not in FLOW_ARRAY_FIELDS:
                issues.append(
                    f"line {lineno}: '{key_name}' value starts with '[' - quote it "
                    "or use an array field. YAML parses unquoted brackets as a flow array."
                )
                continue
            items = split_flow_items(val_stripped)
            arrays[key_name] = [unquote(item) for item in items]
            for item in items:
                validate_array_item(item, lineno, issues, f"flow array item for '{key_name}'")
            continue

        if val_stripped[0] in '"\'':
            scalars[key_name] = unquote(val_stripped)
            continue
        if val_stripped[0] in RESERVED_ARRAY_ITEM_STARTS:
            issues.append(
                f"line {lineno}: '{key_name}' value starts with '{val_stripped[0]}' - quote it. "
                "YAML may parse the value as a non-string value or reject it."
            )
        scalars[key_name] = unquote(val_stripped)

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

    validate_schema_fields(scalars, arrays, issues)

    if issues:
        sys.stderr.write(f"FAIL: {doc_path}\n")
        for issue in issues:
            sys.stderr.write(f"  {issue}\n")
        return 1

    print(f"OK: {doc_path}")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
