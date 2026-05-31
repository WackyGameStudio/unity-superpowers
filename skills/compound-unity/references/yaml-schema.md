# YAML Frontmatter Schema

`schema.yaml` in this directory is the canonical contract for `docs/solutions/` frontmatter written by `compound-unity`.

Use this file as the quick reference for:

- required fields
- preserved `ce-compound` `problem_type` values
- Unity `component` values
- validation expectations
- category mapping
- track classification
- YAML safety rules

## Tracks

`problem_type` determines which track applies. Preserve the original `ce-compound` taxonomy. Put Unity specificity in `component`, `tags`, `root_cause`, `resolution_type`, and evidence fields.

| Track | problem_types | Description |
|-------|---------------|-------------|
| Bug | `build_error`, `test_failure`, `runtime_error`, `performance_issue`, `database_issue`, `security_issue`, `ui_bug`, `integration_issue`, `logic_error` | Defects, failures, and errors that were diagnosed and fixed. |
| Knowledge | `developer_experience`, `workflow_issue`, `best_practice`, `documentation_gap`, `architecture_pattern`, `design_pattern`, `tooling_decision`, `convention` | Practices, patterns, conventions, decisions, workflow improvements, and documentation. |

## Required Fields

- `title`: Clear title for the documented Unity learning.
- `date`: ISO date in `YYYY-MM-DD`.
- `category`: `docs/solutions` subdirectory selected from the category mapping.
- `module`: Unity project area, package, scene, prefab, subsystem, or workflow affected.
- `problem_type`: One of the preserved values in the Tracks table above.
- `component`: One of `editor_bridge`, `bridge_tooling`, `unity_mcp` (legacy alias), `codex_config`, `editor_workflow`, `scene`, `prefab`, `script`, `asmdef`, `package`, `project_settings`, `input_system`, `physics`, `animation`, `ui`, `rendering`, `tests_editmode`, `tests_playmode`, `scriptable_object`, `asset_pipeline`, `documentation`, `development_workflow`, `unity_editor`, `navmesh`, `vehicle`, `interaction_system`, `damage_system`, `state_machine`, `verification`, `tooling`.
- `severity`: One of `critical`, `high`, `medium`, `low`.

## Bug Track Fields

Required:

- `symptoms`: YAML array with 1-6 observable symptoms such as console errors, failed tests, broken scene/prefab behavior, or runtime issues.
- `root_cause`: Use the narrowest value from `schema.yaml`. Values may be Unity-specific, for example `active_target_drift`, `stale_bridge_tools`, `missing_serialized_reference`, `prefab_override_conflict`, `guid_mismatch`, `asmdef_reference_missing`, `package_dependency_missing`, `fixed_update_timing`, `animation_event_mismatch`, `input_action_miswired`, `scriptable_object_reference_missing`, `missing_scene_wiring`, or `insufficient_verification`.
- `resolution_type`: Use the narrowest value from `schema.yaml`. Values may be Unity-specific, for example `bridge_retarget`, `scene_wiring_change`, `prefab_wiring_change`, `serialization_fix`, `meta_guid_restore`, `asmdef_reference_change`, `package_manifest_change`, `playmode_fix`, `editmode_fix`, `architecture_refactor`, `verification_update`, or `workaround`.

## Knowledge Track Fields

No additional required fields beyond the shared required fields.

Optional:

- `applies_when`: Conditions or situations where this guidance applies.
- `symptoms`: Observable gaps or friction that prompted this guidance.
- `root_cause`: Underlying cause, if there is a specific one.
- `resolution_type`: Type of change, if applicable.

## Optional Fields

- `related_components`: Other Unity components, scenes, prefabs, assets, packages, or workflows involved.
- `tags`: Search keywords, lowercase and hyphen-separated where possible.
- `unity_version`: Unity Editor version when relevant.
- `editor_bridge`: Unity Editor bridge mode involved in the issue or verification. Use `unity_ai_assistant` or `mcpforunity`.
- `mcp_tool`: Specific MCPForUnity tool or tool group, or Unity MCP tool, when relevant. `editor_bridge` records the mode; `mcp_tool` records the specific tool when relevant.
- `evidence`: Short list of verification evidence commands, tests, console checks, or smoke checks.

Example bridge metadata:

```yaml
editor_bridge: mcpforunity
mcp_tool: read_console
```

## Category Mapping

- `build_error` -> `docs/solutions/build-errors/`
- `test_failure` -> `docs/solutions/test-failures/`
- `runtime_error` -> `docs/solutions/runtime-errors/`
- `performance_issue` -> `docs/solutions/performance-issues/`
- `database_issue` -> `docs/solutions/database-issues/`
- `security_issue` -> `docs/solutions/security-issues/`
- `ui_bug` -> `docs/solutions/ui-bugs/`
- `integration_issue` -> `docs/solutions/integration-issues/`
- `logic_error` -> `docs/solutions/logic-errors/`
- `developer_experience` -> `docs/solutions/developer-experience/`
- `workflow_issue` -> `docs/solutions/workflow-issues/`
- `best_practice` -> `docs/solutions/best-practices/`
- `documentation_gap` -> `docs/solutions/documentation-gaps/`
- `architecture_pattern` -> `docs/solutions/architecture-patterns/`
- `design_pattern` -> `docs/solutions/design-patterns/`
- `tooling_decision` -> `docs/solutions/tooling-decisions/`
- `convention` -> `docs/solutions/conventions/`

## Validation Rules

1. Determine the track from `problem_type` using the Tracks table.
2. All shared required fields must be present.
3. Bug-track docs must include `symptoms`, `root_cause`, and `resolution_type`.
4. Knowledge-track docs have no additional required fields beyond the shared required fields.
5. Enum fields must match the allowed values exactly.
6. Array fields must respect min/max item counts.
7. `date` must match `YYYY-MM-DD`.
8. `tags` should be lowercase and hyphen-separated where possible.
9. Prefer bridge-neutral values for new docs: `component: editor_bridge` or `bridge_tooling`, `root_cause: stale_bridge_tools`, and `resolution_type: bridge_retarget`. `unity_mcp`, `stale_mcp_tools`, and `unity_mcp_retarget` are legacy aliases for old MCPForUnity-only records.

## YAML Safety Rules

Strict YAML 1.2 parsers can reject or silently reinterpret array items that start with a reserved indicator character as unquoted scalars. When writing items for any array-of-strings field (`symptoms`, `applies_when`, `tags`, `related_components`, `evidence`, or any future array field), wrap the value in double quotes if it starts with any of:

`-`, `?`, `:`, `,`, `[`, `]`, `{`, `}`, `#`, `&`, `*`, `!`, `|`, `>`, `'`, `"`, `%`, `@`, or `` ` ``

Also quote if the value contains the substring `: ` or ` #`. That punctuation can confuse parsers or truncate the value.

Example before, which can break strict YAML:

```yaml
symptoms:
  - `Application.dataPath` points at the wrong active project
```

Example after, which parses cleanly:

```yaml
symptoms:
  - "`Application.dataPath` points at the wrong active project"
editor_bridge: mcpforunity
```

Scalar string fields such as `title:` also need quotes when they start with a reserved indicator or contain ` #` or `: `. The validator catches those parser-safety risks.
