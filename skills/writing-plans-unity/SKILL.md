---
name: writing-plans-unity
description: Use when an approved Unity design or requirements need an implementation plan before touching code, scenes, prefabs, assets, packages, tests, or MCPForUnity tools
---

# Writing Unity Implementation Plans

## Overview

Write comprehensive Unity implementation plans assuming the engineer has zero project context. A Unity plan is not complete until it names the code, scene, prefab, asset, serialized-field, package/settings, MCPForUnity, and verification surfaces needed to make the feature real in the Editor and at runtime.

Assume the implementer is a skilled developer, but does not know this Unity project, its scene hierarchy, prefab conventions, package state, test setup, or MCPForUnity target. Give them bite-sized, executable tasks with exact paths, exact wiring, exact commands, and expected evidence. DRY. YAGNI. TDD when automated tests are feasible. Frequent commits when the workspace is git-backed.

**Announce at start:** "I'm using the writing-plans-unity skill to create the implementation plan."

**Context:** If working in an isolated worktree, it should have been created via the `using-git-worktrees-unity` skill at execution time.

**Save plans to:** `docs/superpowers/plans/YYYY-MM-DD-<feature-name>.md`
- User preferences for plan location override this default.

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
- MCPForUnity tools to use, including target identity checks when Editor work is involved
- file-state limitations to report when MCPForUnity is unavailable, stale, or aimed at the wrong project
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

**Unity Surface:** [Scenes, prefabs, assets, scripts, packages, ProjectSettings, asmdefs, tests, and MCPForUnity/editor surfaces touched]

**Architecture:** [2-3 sentences naming MonoBehaviour boundaries, State/Strategy/interface/ScriptableObject decisions, and scene/prefab wiring]

**Verification:** [Compile, console, EditMode, PlayMode, scene/prefab smoke, MCPForUnity, or manual evidence with reason]

**Tech Stack:** [Unity version if known, render pipeline, packages, input system, test framework, MCP tools]

---
```

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

**MCPForUnity:**
- Target identity: [active instance/project check plus `Application.dataPath` evidence where Editor work is involved]
- Tools: [`manage_scene`, `manage_prefabs`, `manage_asset`, `manage_scriptable_object`, `validate_script`, `refresh_unity`, `read_console`, `run_tests`, or `None`]
- Limitation: [state explicitly when MCPForUnity is unavailable and Editor/runtime proof cannot be claimed]

**Verification:**
- Expected evidence: [compile/domain reload result, console result, EditMode/PlayMode output, scene smoke, prefab smoke, runtime/manual observation with reason]

- [ ] **Step 1: Write the failing automated test, if feasible**

```csharp
// Include the exact EditMode or PlayMode test code, or state why automation is infeasible.
```

- [ ] **Step 2: Run the test and verify RED**

Run: `[exact MCPForUnity run_tests command or explicit infeasible-automation reason]`
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

When automated tests are feasible, the task MUST include red, green, and refactor steps. When automation is infeasible, the task MUST say why and replace RED/GREEN with precise Unity evidence such as MCPForUnity inspection, console output, scene smoke, prefab smoke, or manual observation.

## Plan Rejection Rules

Reject and rewrite the plan if any of these are true:

- It only says "edit scripts and run tests" while scene, prefab, asset, package, ProjectSettings, Animator, physics, or Unity Editor wiring is involved.
- It names code files but does not name the affected scene path, prefab path, asset path, serialized field wiring, package/settings file, or `.meta` risk when those surfaces matter.
- It claims Unity runtime or Editor verification from file-only checks.
- It adds a `MonoBehaviour` without explaining where it is attached and how required serialized fields are assigned.
- It adds an interface, `State`, `Strategy`, event, factory, or `ScriptableObject` without showing the scene/prefab/code wiring that makes it active.
- It uses MCPForUnity without checking the active target.

## No Placeholders

Every step must contain the actual content an engineer needs. These are plan failures; never write them:

- `TBD`, `TODO`, `implement later`, `fill in details`
- "Add appropriate error handling", "add validation", or "handle edge cases"
- "Write tests for the above" without actual test code or an explicit infeasible-automation reason
- "Wire it in the prefab" without the exact prefab path, component, field, and expected value/reference
- "Update the scene" without the exact scene path, GameObject, component, and serialized field changes
- "Run tests" without exact EditMode, PlayMode, MCPForUnity command, or infeasible-automation reason and expected evidence
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

**2. Unity surface coverage:** For every task, check the `Code`, `Scene`, `Prefab`, `Asset`, `Package/Settings`, `Test`, `MCP/Fallback`, and `Verification` fields. Required Unity surfaces must be exact; irrelevant surfaces must say `None`.

**3. Architecture consistency:** Do MonoBehaviour boundaries, interfaces, `State`, `Strategy`, factory, observer/event, and `ScriptableObject` decisions match the approved design and source-grounded Unity architecture rules?

**4. Wiring consistency:** Do serialized field names, GameObject names, prefab paths, scene paths, Animator parameter names, layer names, package names, asmdef references, and asset paths match across tasks?

**5. Evidence consistency:** Does each task define the expected compile/domain reload, console, EditMode, PlayMode, scene smoke, prefab smoke, MCPForUnity, or manual evidence? Manual evidence must include the reason automation is infeasible.

**6. Placeholder scan:** Search your plan for the red flags from "No Placeholders" and "Plan Rejection Rules." Fix every hit.

If you find issues, fix them inline. If a design requirement has no task, add the task before handoff.

## Execution Handoff

After saving the plan, offer execution choice:

**"Plan complete and saved to `docs/superpowers/plans/<filename>.md`. Two execution options:**

**1. Subagent-Driven (recommended)** - I dispatch a fresh subagent per task, review between tasks, fast iteration

**2. Inline Execution** - Execute tasks in this session using executing-plans-unity, batch execution with checkpoints

**Which approach?"**

**If Subagent-Driven chosen:**
- **REQUIRED SUB-SKILL:** Use subagent-driven-development-unity
- Fresh subagent per task + two-stage review

**If Inline Execution chosen:**
- **REQUIRED SUB-SKILL:** Use executing-plans-unity
- Batch execution with checkpoints for review
