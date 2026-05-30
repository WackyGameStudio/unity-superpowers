# Code Quality Reviewer Prompt Template

Use this template when dispatching a code quality reviewer subagent.

**Purpose:** Verify implementation is well-built, tested, maintainable, and sound for Unity.

**Only dispatch after spec compliance review passes.**

```
Task tool (general-purpose):
  Use template at requesting-code-review-unity/code-reviewer.md

  DESCRIPTION: [task summary, from implementer's report]
  PLAN_OR_REQUIREMENTS: Task N from [plan-file]
  BASE_SHA: [commit before task]
  HEAD_SHA: [current commit]
```

**In addition to standard code quality concerns, the reviewer should check:**
- Does each file have one clear responsibility with a well-defined interface?
- Are units decomposed so they can be understood and tested independently?
- Is the implementation following the file and Unity surface structure from the plan?
- Did this implementation create new files that are already large, or significantly grow existing files? Do not flag pre-existing file sizes; focus on what this change contributed.
- Are MonoBehaviours split by responsibility instead of accumulating input, movement, state, animation, VFX, UI, and persistence in one class?
- Are optional Unity capabilities represented with small interfaces rather than broad inheritance?
- Are `State`, `Strategy`, events, factories, and `ScriptableObject` assets used only where the plan calls for them?
- Are scene, prefab, asset, serialized-field, package, asmdef, ProjectSettings, and `.meta` changes intentional and reviewable?
- Does verification evidence match the Unity surfaces changed: compile, console, EditMode, PlayMode, scene smoke, prefab smoke, active Editor bridge target identity, or explicit limitation?
- Report bridge mode, identity evidence, Unity evidence gathered, and limitations.

**Code reviewer returns:** Strengths, Issues (Critical/Important/Minor), Assessment
