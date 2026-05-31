---
name: writing-plans-unity
description: Use when an approved Unity design or requirements need an implementation plan, or when reviewing an existing Unity spec/plan before execution, before touching code, scenes, prefabs, assets, packages, tests, or active bridge tools or evidence
---

# Writing Unity Implementation Plans

## Overview

Write comprehensive Unity implementation plans assuming the engineer has zero project context. A Unity plan is not complete until it names the code, scene, prefab, asset, serialized-field, package/settings, Editor bridge, and verification surfaces needed to make the feature real in the Editor and at runtime.

Assume the implementer is a skilled developer, but does not know this Unity project, its scene hierarchy, prefab conventions, package state, test setup, or active Editor bridge target. Give them bite-sized, executable tasks with exact paths, exact wiring, exact commands, and expected evidence. DRY. YAGNI. TDD when automated tests are feasible. Frequent commits when the workspace is git-backed.

**Announce at start:** "I'm using the writing-plans-unity skill to create the implementation plan."

**Context:** If working in an isolated worktree, it should have been created via the `using-git-worktrees-unity` skill at execution time.

**Save plans to:** `docs/superpowers/plans/YYYY-MM-DD-<feature-name>.md`
- User preferences for plan location override this default.

## Output Language Rules

Human-readable explanatory prose, requirement descriptions, task detail paragraphs, review notes, questions, and handoff text in generated `docs/` artifacts MUST use the user's conversation language unless the user explicitly asks for another language.

Template labels, structural labels, and Markdown headings may stay in English. Labels such as `Goal`, `Architecture`, `Verification`, `Task`, `Step`, `Expected`, `Recommendations`, and `Issues Found` are allowed. The content after those labels must be in the user's language.

If the user writes in Korean, write the plan's explanations, task details, assumptions, verification rationale, reviewer notes, and handoff prose in natural Korean.

Keep exact technical identifiers unchanged:

- file paths, class names, method names, namespaces, package names, shader names, scene/prefab/asset names
- Unity API names such as `MonoBehaviour`, `ScriptableObject`, `Rigidbody`, `Animator`, `EditMode`, and `PlayMode`
- commands, code blocks, branch names, commit message examples, URLs, and quoted source text

When using subagents, include the required prose language in every subagent prompt. Plan reviewers must check that body content follows the user's language while preserving technical identifiers and allowing template labels.

## Unity Plan Surface Requirements

Before defining tasks, map every relevant Unity implementation surface. Plans MUST name each applicable item with exact paths, GameObject/component names, and expected evidence:

- exact C# files under `Assets/`
- asmdef creation or reference changes
- scene path and scene changes
- prefab paths and prefab changes
- `ScriptableObject` asset creation and config
- serialized field wiring, including object references, numeric values, layer masks, events, and missing-reference checks
- `Packages/manifest.json` and package lock changes
- `ProjectSettings/` changes
- `.meta`/GUID risk for new, renamed, moved, or deleted assets
- Animator controllers, Animator parameters, animation clips, animation events, and transition conditions
- physics layers, colliders, triggers, Rigidbody settings, NavMesh, `WheelCollider`, and query masks
- EditMode test files
- PlayMode test files and PlayMode test scenes
- active bridge tools or evidence to use, including active Editor bridge target identity checks when Editor work is involved
- active Editor bridge mode, target identity, and tool/evidence path when Editor work is involved
- console, compile, and domain reload checks
- manual verification with a reason only when automation is infeasible

If a surface is not relevant, say `None` in the task field. Do not omit the field.

## Scope Check

If the approved design covers multiple independent Unity subsystems, it should have been broken into sub-project specs during brainstorming. If it was not, suggest breaking it into separate plans, one per subsystem. Each plan should produce working, testable Unity behavior on its own.

## File And Unity Surface Structure

Before defining tasks, map which files, scenes, prefabs, assets, packages, and settings will be created or modified and what each one is responsible for. This is where decomposition decisions get locked in.

- Split MonoBehaviours by reason to change: input collection, movement execution, physics query, animation bridge, state orchestration, feedback, and data/config should not accumulate in one script.
- Prefer GameObject composition before inheritance. Use inheritance only when stable shared lifecycle or state orchestration is clearer than component assembly.
- Use small capability interfaces such as `IInteractable`, `IDamagable`, `IAgentMovementInput`, `IAgentJumpInput`, and `IVehicleInput`.
- Use `State`, transition rules, `Strategy`, factory/data objects, observer/event flows, and `ScriptableObject` assets where the approved design calls for them.
- Treat scene and prefab wiring as architecture. Component addition/removal, serialized fields, layers, colliders, Animator parameters, package dependencies, asmdefs, and `.meta` files are implementation surfaces, not cleanup.
- In existing projects, follow established folder, asmdef, prefab, and test patterns. If a file or prefab has grown unwieldy, include the split or migration explicitly in the plan.

This structure informs task decomposition. Each task should produce self-contained Unity changes that make sense independently.

## Bite-Sized Task Granularity

Each step is one action that can be executed and verified:

- Write the failing EditMode or PlayMode test.
- Run it to confirm the expected failure.
- Implement the minimal code.
- Wire the scene, prefab, asset, serialized fields, package, or settings change.
- Refresh Unity, wait for compile/domain reload, and read the console.
- Run the relevant tests or scene smoke / prefab smoke.
- Commit, if the workspace is git-backed.

## Plan Document Header

Every plan MUST start with this header:

```markdown
# [Unity Feature Name] Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use subagent-driven-development-unity (recommended) or executing-plans-unity to implement this Unity plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** [One sentence describing the Unity feature or project setup result]

**Unity Surface:** [Scenes, prefabs, assets, scripts, packages, ProjectSettings, asmdefs, tests, and Editor bridge surfaces touched]

**Architecture:** [2-3 sentences naming MonoBehaviour boundaries, State/Strategy/interface/ScriptableObject decisions, and scene/prefab wiring]

**Verification:** [Compile, console, EditMode, PlayMode, scene/prefab smoke, Editor bridge, or manual evidence with reason]

**Tech Stack:** [Unity version if known, render pipeline, packages, input system, test framework, active bridge tools]

---
```

The header above is a structure example. English field labels may be used as-is. The explanatory content inside each field should use the user's language.

## Unity Task Structure

Each Unity task MUST include these fields. Use `None` only after checking the surface is irrelevant.

````markdown
### Task N: [Unity Component / Scene / Prefab / Asset Result]

**Code:**
- Create: `Assets/.../ExactFile.cs`
- Modify: `Assets/.../ExistingFile.cs`
- Architecture: [MonoBehaviour boundary, interface, State, Strategy, factory, event, or ScriptableObject role]

**Scene:**
- Path: `Assets/.../ExactScene.unity`
- Changes: [GameObjects, components, layers, colliders, triggers, Animator/controller links, NavMesh bake, hierarchy changes]

**Prefab:**
- Path: `Assets/.../ExactPrefab.prefab`
- Changes: [component additions/removals, prefab overrides, child hierarchy, missing-reference checks]

**Asset:**
- Create/Modify: `Assets/.../ExactAsset.asset`
- Config: [ScriptableObject values, Animator controller parameters, clips, materials, audio, sprites, input actions, Addressables/Resources if relevant]

**Package/Settings:**
- Modify: `Packages/manifest.json`, `Packages/packages-lock.json`, `ProjectSettings/...`, or asmdef references
- `.meta`/GUID risk: [new/moved/renamed/deleted asset GUID impact and mitigation]

**Test:**
- EditMode: `Assets/Tests/EditMode/.../ExactTests.cs` or `None`
- PlayMode: `Assets/Tests/PlayMode/.../ExactTests.cs` / test scene path or `None`
- TDD: [red/green/refactor steps when automated tests are feasible; otherwise manual-only reason]

**Editor Bridge:**
- Mode: [`unity_ai_assistant` | `mcpforunity`]
- Target identity: [active bridge/project check plus `Application.dataPath` or equivalent evidence where Editor work is involved]
- Tool/evidence path: [Unity AI Assistant / Unity MCP capabilities, or for `mcpforunity`: `validate_script`, `refresh_unity`, `read_console`, `run_tests`, `manage_scene`, `manage_prefabs`, `manage_asset` as applicable]
- Selected bridge evidence gaps: [state explicitly when the selected bridge cannot provide a required evidence surface]

**Verification:**
- Expected evidence: [compile/domain reload result, console result, EditMode/PlayMode output, scene smoke, prefab smoke, runtime/manual observation with reason]

- [ ] **Step 1: Write the failing automated test, if feasible**

```csharp
// Include the exact EditMode or PlayMode test code, or state why automation is infeasible.
```

- [ ] **Step 2: Run the test and verify RED**

Run: `[exact EditMode/PlayMode command, active bridge test command, batchmode test command, or explicit infeasible-automation reason]`
Expected: `FAIL` for the missing behavior, not a setup error.

- [ ] **Step 3: Implement the minimal code**

```csharp
// Include complete code or precise patch-level content for this step.
```

- [ ] **Step 4: Wire Unity surfaces**

Apply these exact Editor/file changes:
- Scene: `[exact GameObject/component/layer/collider/Animator/NavMesh changes]`
- Prefab: `[exact prefab component/override/serialized field changes]`
- Asset: `[exact ScriptableObject/Animator/material/audio/input asset changes]`
- Package/Settings: `[exact package, asmdef, ProjectSettings, or .meta changes]`

- [ ] **Step 5: Verify GREEN**

Run:

```text
[exact refresh/compile/console/test/smoke commands]
```

Expected:
- Compile/domain reload: `[expected result]`
- Console: `[expected errors/warnings state]`
- Tests: `[expected EditMode/PlayMode result]`
- Scene smoke / prefab smoke: `[expected runtime or inspection evidence]`

- [ ] **Step 6: Refactor while keeping evidence green**

Refactor only the code or Unity wiring covered by this task. Re-run the same verification command(s) and record the expected unchanged evidence.

- [ ] **Step 7: Commit, if git-backed**

```bash
git add [exact files, scenes, prefabs, assets, .meta, packages, settings, tests]
git commit -m "[type]: [short Unity task result]"
```
````

The task template above is also structural. English labels and checklist titles may be used as-is. The body content under each label should use the user's language while preserving exact Unity identifiers and paths.

When automated tests are feasible, the task MUST include red, green, and refactor steps. When automation is infeasible, the task MUST say why and replace RED/GREEN with precise Unity evidence such as Editor bridge inspection, console output, scene smoke, prefab smoke, or manual observation.

## Plan Rejection Rules

Reject and rewrite the plan if any of these are true:

- It only says "edit scripts and run tests" while scene, prefab, asset, package, ProjectSettings, Animator, physics, or Unity Editor wiring is involved.
- It names code files but does not name the affected scene path, prefab path, asset path, serialized field wiring, package/settings file, or `.meta` risk when those surfaces matter.
- It claims Unity runtime or Editor verification without Unity AI Assistant / Unity MCP or MCPForUnity evidence.
- It adds a `MonoBehaviour` without explaining where it is attached and how required serialized fields are assigned.
- It adds an interface, `State`, `Strategy`, event, factory, or `ScriptableObject` without showing the scene/prefab/code wiring that makes it active.
- It uses any Editor bridge without checking the active target.

## No Placeholders

Every step must contain the actual content an engineer needs. These are plan failures; never write them:

- `TBD`, `TODO`, `implement later`, `fill in details`
- "Add appropriate error handling", "add validation", or "handle edge cases"
- "Write tests for the above" without actual test code or an explicit infeasible-automation reason
- "Wire it in the prefab" without the exact prefab path, component, field, and expected value/reference
- "Update the scene" without the exact scene path, GameObject, component, and serialized field changes
- "Run tests" without exact EditMode, PlayMode, Editor bridge command, or infeasible-automation reason and expected evidence
- "Similar to Task N"; repeat the content because the engineer may read tasks out of order
- References to types, functions, methods, assets, scenes, or prefabs not defined in any task

## Remember

- Exact file paths always.
- Complete code in every step if a step changes code.
- Exact scene, prefab, asset, package, asmdef, ProjectSettings, and `.meta` changes when relevant.
- Explicit serialized wiring and expected Unity evidence.
- Exact commands with expected output.
- DRY, YAGNI, TDD where feasible, frequent commits when git-backed.

## Self-Review

After writing the complete plan, review it against the approved design or requirements. This is a checklist you run yourself, not a subagent dispatch.

**1. Design coverage:** For each design requirement, can you point to a task that maps it to code plus Unity surfaces and evidence? If a requirement touches behavior, the mapping must include where it lives in `Assets/`, where it is wired in scene/prefab/assets, and how it is verified.

**2. Unity surface coverage:** For every task, check the `Code`, `Scene`, `Prefab`, `Asset`, `Package/Settings`, `Test`, `Editor Bridge`, and `Verification` fields. Required Unity surfaces must be exact; irrelevant surfaces must say `None`.

**3. Architecture consistency:** Do MonoBehaviour boundaries, interfaces, `State`, `Strategy`, factory, observer/event, and `ScriptableObject` decisions match the approved design and source-grounded Unity architecture rules?

**4. Wiring consistency:** Do serialized field names, GameObject names, prefab paths, scene paths, Animator parameter names, layer names, package names, asmdef references, and asset paths match across tasks?

**5. Evidence consistency:** Does each task define the expected compile/domain reload, console, EditMode, PlayMode, scene smoke, prefab smoke, Editor bridge, or manual evidence? Manual evidence must include the reason automation is infeasible.

**6. Placeholder scan:** Search your plan for the red flags from "No Placeholders" and "Plan Rejection Rules." Fix every hit.

**7. Language compliance:** Confirm that all explanatory body content in the saved plan uses the user's conversation language. English template labels are allowed. For Korean users, the prose after labels, task descriptions, assumptions, verification rationale, and handoff text must be Korean, while code identifiers and exact technical strings remain unchanged.

If you find issues, fix them inline. If a design requirement has no task, add the task before handoff.

## Existing Plan Review Handoff

Use this section when the user asks to inspect, analyze, review, or continue from an existing spec and implementation plan before deciding the next step.

After reviewing the existing spec/plan, do not end with an open-ended "should I proceed?" question. Classify the plan and present the next-step choices explicitly.

**If the plan is execution-ready:**

**"`docs/superpowers/plans/<filename>.md` is execution-ready. Two execution options:**

**1. Worktree + Subagent-Driven (recommended)** - I use `using-git-worktrees-unity` to set up or verify an isolated workspace, then dispatch a fresh subagent per task with review between tasks

**2. Worktree + Inline Execution** - I use `using-git-worktrees-unity` to set up or verify an isolated workspace, then execute tasks in this session using `executing-plans-unity` with checkpoints

**Which approach?"**

**If the plan is not execution-ready:**

Summarize the blockers, then offer concrete choices:

**"`docs/superpowers/plans/<filename>.md` needs correction before safe execution. Options:**

**1. Fix the implementation plan first** - I update the plan so missing Unity surfaces, serialized wiring, tests, and verification evidence are explicit, then return to the execution handoff

**2. Prepare baseline isolation first** - I use `using-git-worktrees-unity` or ask for explicit in-place approval after Git-tracked Unity baseline files are handled, then return to plan correction or execution

**3. Stop here** - I leave the analysis as-is

**Which approach?"**

Use the user's conversation language for the actual question. Keep skill names and plan paths unchanged.

If the user chooses plan correction, revise the plan and then run the normal `Execution Handoff` below. If the user chooses baseline isolation, use `using-git-worktrees-unity` first, then return to this decision point.

## Execution Handoff

After saving the plan, offer execution choice. This handoff MUST make the worktree step visible, because Unity scenes, prefabs, packages, and `.meta` files are risky to edit on the user's current branch.

**"Plan complete and saved to `docs/superpowers/plans/<filename>.md`. Two execution options:**

**1. Worktree + Subagent-Driven (recommended)** - I use `using-git-worktrees-unity` to set up or verify an isolated workspace, then dispatch a fresh subagent per task with review between tasks

**2. Worktree + Inline Execution** - I use `using-git-worktrees-unity` to set up or verify an isolated workspace, then execute tasks in this session using `executing-plans-unity` with checkpoints

**Which approach?"**

Use the user's conversation language for the actual question. Keep skill names and plan path unchanged.

**If Subagent-Driven chosen:**
- **REQUIRED SUB-SKILL FIRST:** Use using-git-worktrees-unity
- **REQUIRED SUB-SKILL:** Use subagent-driven-development-unity
- Fresh subagent per task + two-stage review

**If Inline Execution chosen:**
- **REQUIRED SUB-SKILL FIRST:** Use using-git-worktrees-unity
- **REQUIRED SUB-SKILL:** Use executing-plans-unity
- Batch execution with checkpoints for review
