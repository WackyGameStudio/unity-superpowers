---
name: compound-unity
description: Use after Unity work reveals a reusable solved problem, workaround, blocked-then-solved path, Editor/MCP issue, scene/prefab serialization issue, test timing issue, or workflow lesson
---

# Compound Unity

## Purpose

Capture solved Unity learnings while context is fresh. Write one final learning doc to `docs/solutions/` so future Unity agent work can reuse the blocker, workaround, solution, architecture decision, scene/prefab wiring lesson, or verification gap.

Unity work often depends on Editor state, package state, MCPForUnity routing, scene/prefab serialization, `.meta` GUIDs, asmdefs, compile/domain reload timing, PlayMode timing, Input System wiring, `ScriptableObject` references, and asset loading. Capture both solved problems and cases where the first approach was blocked and another route worked.

The output is one durable learning under `docs/solutions/`, written in the user's conversation language by default.

## Modes

Detect a `mode:headless` token in the arguments. Tokens starting with `mode:` are flags, not context; strip `mode:headless` before treating the rest as the optional Unity context hint.

| Mode | When | Behavior |
|------|------|----------|
| Interactive Full | Default when the user wants complete capture | Ask whether to run Full or Lightweight. In Full, search existing `docs/solutions/`, check overlap, collect context carefully, and write the final doc. |
| Interactive Lightweight | User chooses faster capture | Do one focused pass. Write the same final doc structure, but skip broad duplicate detection and optional refresh work. |
| `mode:headless` | Automation or another Unity skill invokes this | Ask no blocking questions. Run Full without session-history prompts, apply the discoverability check edit when a clear gap exists, write the final report, and end with a structured terminal report. |

Headless mode never stops for consent. If no solved and verified Unity lesson is detected, report `Documentation skipped` instead of inventing a doc.

## Where Future Skills Read This

Docs created by this skill are read later by Unity skills, not left as passive notes:

- `using-superpowers-unity`: at session startup and during targeted `docs/solutions/` search by feature, subsystem, path, scene, prefab, error, package, MCP tool, or test mode.
- `brainstorming-unity`: before design questions when the requested topic matches a prior Unity lesson.
- `writing-plans-unity`: before task planning and task decomposition, especially when a lesson names scenes, prefabs, asmdefs, packages, or verification surfaces.
- `systematic-debugging-unity`: before root-cause investigation so known MCPForUnity, Editor, serialization, timing, or package failures are not rediscovered from scratch.
- `subagent-driven-development-unity`: when constructing subagent prompts so each agent receives relevant blockers, ownership boundaries, and verification expectations.
- `verification-before-completion-unity`: before final claims so prior verification gaps and required evidence shape the completion check.
- `unity-init`: before MCP/project setup repair when setup, active target identity, tool group, Codex config, or project identity issues are documented.

Search narrowly. Use the current feature, Unity subsystem, path, scene name, prefab name, package, error message, MCP tool, test mode, or architecture pattern. Do not bulk-read the entire knowledge store by default.

## Unity Capture Triggers

Create or update a learning when the work reveals reusable knowledge about:

- MCPForUnity connection/config/tool group issues
- multi-instance routing/active target drift
- compile/domain reload waiting
- console diagnostics
- scene/prefab serialization conflicts
- `.meta`/GUID issues
- asmdef references
- package/`Packages/manifest.json` changes
- EditMode vs PlayMode differences
- physics timing, `FixedUpdate`, collision, trigger, or layer behavior
- animation events, Animator parameters, transition conditions, or clip timing
- Input System action maps, bindings, `PlayerInput`, or generated wrapper wiring
- `ScriptableObject` creation/references and designer-facing tuning assets
- Addressables/Resources/asset loading
- Editor-only vs runtime assembly separation
- scene/prefab smoke verification
- architecture decisions using composition, `State`, `Strategy`, small interfaces, events, or data assets
- cases where the first approach was blocked and another route worked

## Language Policy

Write docs, questions, reports, and final handoffs in the user's conversation language.

English structural labels, Markdown headings, YAML keys, and template labels may stay in English. The explanatory body text under those labels must use the user's conversation language.

Keep identifiers, paths, Unity API names, commands, class/interface names, package names, file names, YAML frontmatter enum values, tags, and quoted source text unchanged.

If the user writes in Korean, write the `docs/solutions/` problem, symptoms, failed attempts, solution, rationale, evidence, prevention, reports, and handoff prose in natural Korean while preserving technical strings exactly.

## Support Files

Read these files only when needed for the step:

- `references/schema.yaml`: canonical Unity frontmatter fields, tracks, enum values, root causes, and resolution types.
- `references/yaml-schema.md`: quick reference, category mapping, and YAML safety rules.
- `assets/resolution-template.md`: section structure for new Unity solution docs.

When delegating or asking another agent to help, pass the relevant contract text into the prompt. Do not rely on the other agent guessing this skill's local file paths.

<critical_requirement>
Helper agents and research tasks return text only. They must not create side files, draft files, context notes, or partial documentation artifacts.

The orchestrator writes only one final `docs/solutions/<category>/<filename>.md` doc, plus the optional instruction-file edit from the Discoverability Check when needed. All delegated context analysis, solution extraction, overlap checks, and schema review must come back as text for the orchestrator to assemble.
</critical_requirement>

## Workflow

1. Confirm the lesson is solved or the workaround is verified. If the problem is still in progress, do not write the final learning yet.
2. Determine the mode. In interactive mode, ask Full vs Lightweight before doing long-running research. In headless mode, ask nothing.
3. Classify the learning with `references/schema.yaml`:
   - Bug/failure track: use preserved `ce-compound` values such as `build_error`, `test_failure`, `runtime_error`, `integration_issue`, or `logic_error`.
   - Knowledge track: use preserved `ce-compound` values such as `architecture_pattern`, `design_pattern`, `tooling_decision`, `convention`, `workflow_issue`, `developer_experience`, `documentation_gap`, or `best_practice`.
   - Put Unity specificity in `component`, `tags`, `root_cause`, `resolution_type`, and evidence fields, not in new `problem_type` values.
4. Read `references/yaml-schema.md` and choose the `docs/solutions/<category>/` directory from the `problem_type` mapping.
5. Search existing `docs/solutions/` narrowly for overlap. In Full mode, update an existing doc when it already covers the same problem, root cause, and solution. In Lightweight mode, a focused new doc is acceptable when overlap is uncertain.
6. Assemble the doc with `assets/resolution-template.md`.
7. Include concrete Unity evidence:
   - MCPForUnity target checks and `Application.dataPath` evidence when target identity mattered.
   - compile/domain reload wait evidence when relevant.
   - console diagnostics, including `read_console` or fallback output.
   - EditMode, PlayMode, scene smoke, prefab smoke, asset inspection, or manual runtime evidence with a reason when automation was not feasible.
8. Write exactly one final doc under `docs/solutions/<category>/<filename>.md`.
9. Run schema validation against `references/schema.yaml` and `references/yaml-schema.md`: validate required fields, track-specific fields, enum values, category mapping, and Unity component/tag specificity. Fix schema validation failures before continuing.
10. Run `python <this-skill>/scripts/validate-frontmatter.py <doc-path>` for parser-safety validation and fix parser-safety failures.
11. Both schema validation and parser-safety validation must pass before claiming the doc is complete.
12. Run the Discoverability Check.

## Discoverability Check

After writing the learning, check root instruction files such as `AGENTS.md`, `CLAUDE.md`, and `GEMINI.md`.

The check passes when an agent reading those files can discover:

- `docs/solutions/` exists as a searchable store of solved Unity lessons.
- Docs are organized by category with YAML frontmatter such as `module`, `problem_type`, `component`, and `tags`.
- The store is relevant before Unity design, planning, debugging, implementation decomposition, setup repair, or final verification in documented areas.

If the instruction files do not surface `docs/solutions/`:

- Interactive Full: propose the smallest update, show where it would go, and ask before applying it.
- Interactive Lightweight: mention the gap and suggest the update without blocking.
- `mode:headless`: apply the smallest clear update directly and include it in the final report.

This optional instruction-file edit is maintenance, not a second deliverable. The primary output remains the one solution doc.

## Output

Write one final doc under:

```text
docs/solutions/<category>/<filename>.md
```

An optional instruction-file edit is allowed only when the Discoverability Check finds a real gap.

## What It Captures

- Problem or decision: exact Unity blocker, workaround, architecture decision, or verification gap.
- Symptoms: errors, console diagnostics, failed tests, broken scene/prefab behavior, or runtime observation.
- What did not work: first approach, blocked path, stale target, bad package route, wrong test mode, or incomplete verification.
- Solution: exact fix, workaround, wiring, command, package change, scene/prefab change, or process adjustment.
- Why this works: Unity-specific root cause and why the solution addresses it.
- Unity evidence: compile, console, target identity, EditMode, PlayMode, scene smoke, prefab smoke, asset inspection, or manual proof.
- Prevention: small rule future Unity skills should apply before repeating the mistake.
- Related docs: prior `docs/solutions/` entries, issues, source-analysis docs, or package references.

## Categories

Use `references/yaml-schema.md` for the canonical mapping. Category directories follow preserved `ce-compound` `problem_type` values, for example:

- `build-errors/`
- `test-failures/`
- `runtime-errors/`
- `performance-issues/`
- `database-issues/`
- `security-issues/`
- `ui-bugs/`
- `integration-issues/`
- `logic-errors/`
- `architecture-patterns/`
- `design-patterns/`
- `tooling-decisions/`
- `conventions/`
- `workflow-issues/`
- `developer-experience/`
- `documentation-gaps/`
- `best-practices/`

Use `component` and `tags` to distinguish MCPForUnity, scene, prefab, asmdef, package, PlayMode, Input System, and other Unity-specific surfaces inside those categories.

## Headless Report

End a successful headless run with:

```text
Documentation complete (headless mode)

File: docs/solutions/<category>/<filename>.md (created | updated)
Track: <bug | knowledge>
Category: <category>
Overlap: <none | low | moderate - see <path> | high - existing doc updated>
Instruction-file edit: <none needed | applied to <path> | gap noted, not applied>
Refresh recommendation: <none | scope hint>

Documentation complete
```

When no doc was written:

```text
Documentation skipped (headless mode)

Reason: <one sentence>

Documentation skipped
```
