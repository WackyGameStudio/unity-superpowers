# Resolution Templates

Choose the template matching the `problem_type` track in `references/schema.yaml`.

---

## Bug/Failure Track Template

Use for Unity blockers, failures, workarounds, and verification gaps classified with preserved `ce-compound` bug values: `build_error`, `test_failure`, `runtime_error`, `performance_issue`, `database_issue`, `security_issue`, `ui_bug`, `integration_issue`, and `logic_error`. Put Unity specificity such as MCPForUnity, scene/prefab, asmdef, package, PlayMode, Input System, or physics timing in `component`, `tags`, `root_cause`, and `resolution_type`.

YAML safety: array items in `symptoms`, `applies_when`, `tags`, `related_components`, or future array fields must be wrapped in double quotes when they start with a reserved indicator character or contain colon followed by a space. Reserved indicators include backtick, left bracket, asterisk, ampersand, exclamation mark, pipe, greater-than sign, percent sign, at sign, and question mark. See `references/yaml-schema.md` for details.

```markdown
---
title: [Clear Unity problem title]
date: [YYYY-MM-DD]
category: [docs/solutions subdirectory]
module: [Unity project area, package, scene, prefab, or workflow]
problem_type: [schema enum]
component: [schema enum]
symptoms:
  - [Observable symptom, error, console entry, or broken behavior]
root_cause: [schema enum]
resolution_type: [schema enum]
severity: [schema enum]
tags: [unity, keyword-two]
---

# [Clear Unity problem title]

## Problem
[1-2 sentence description of the Unity issue and impact.]

## Symptoms
- [Observable symptom, Unity console error, test failure, or runtime behavior.]

## What Didn't Work
- [Attempted fix, blocked route, stale MCP target, wrong test mode, or incomplete verification and why it failed.]

## Solution
[The fix that worked. Include relevant commands, code snippets, package edits, scene/prefab wiring, or asset steps.]

## Why This Works
[Unity-specific root cause explanation and why the solution addresses it.]

## Unity Verification Evidence
- [Fresh evidence: target identity, compile/domain reload, console, EditMode, PlayMode, scene smoke, prefab smoke, asset inspection, or manual runtime proof with reason.]

## Prevention
- [Concrete practice, test, guardrail, workflow step, or future skill lookup.]

## Related
- [Related docs, source-analysis notes, issues, or package references.]
```

---

## Knowledge Track Template

Use for Unity architecture, design, workflow, tooling, convention, best-practice, and documentation lessons classified with preserved `ce-compound` knowledge values: `developer_experience`, `workflow_issue`, `best_practice`, `documentation_gap`, `architecture_pattern`, `design_pattern`, `tooling_decision`, and `convention`.

YAML safety: array items in `symptoms`, `applies_when`, `tags`, `related_components`, or future array fields must be wrapped in double quotes when they start with a reserved indicator character or contain colon followed by a space. Reserved indicators include backtick, left bracket, asterisk, ampersand, exclamation mark, pipe, greater-than sign, percent sign, at sign, and question mark. See `references/yaml-schema.md` for details.

```markdown
---
title: [Clear Unity guidance title]
date: [YYYY-MM-DD]
category: [docs/solutions subdirectory]
module: [Unity project area, package, scene, prefab, or workflow]
problem_type: [schema enum]
component: [schema enum]
severity: [schema enum]
applies_when:
  - [Condition where this guidance applies]
tags: [unity, keyword-two]
---

# [Clear Unity guidance title]

## Context
[What situation, gap, decision, or repeated friction prompted this guidance.]

## Guidance
[The practice, pattern, recommendation, or decision. Include examples when useful.]

## Why This Matters
[Rationale and impact of following or ignoring this guidance.]

## When to Apply
- [Conditions, Unity surfaces, or project states where this applies.]

## Unity Evidence
- [Source-analysis, compile, console, test, scene/prefab, asset, or workflow evidence supporting the guidance.]

## Examples
[Concrete before/after, file layout, component wiring, command sequence, or prompt shape.]

## Related
- [Related docs, source-analysis notes, issues, or package references.]
```
