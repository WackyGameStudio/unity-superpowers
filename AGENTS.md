# Unity Superpowers

This package contains project-local Unity Superpowers skills for coding agents.

## Operating Model

Use the skills in this order for non-trivial Unity work:

1. `unity-init` when project setup, Git state, MCPForUnity, or Editor verification is missing or uncertain
2. `brainstorming-unity` before gameplay features, tools, packages, scenes, prefabs, or behavior changes
3. `writing-plans-unity` after a design is approved and before implementation
4. `using-git-worktrees-unity` before executing implementation plans, unless the user explicitly approves working in place
5. `subagent-driven-development-unity` or `executing-plans-unity` to execute a plan
6. `test-driven-development-unity` for feature and bugfix implementation
7. `systematic-debugging-unity` for failures, regressions, console errors, broken scene behavior, or package issues
8. `requesting-code-review-unity` and `receiving-code-review-unity` for review loops
9. `verification-before-completion-unity` before any completion claim
10. `compound-unity` after a reusable Unity workaround or lesson is verified
11. `finishing-a-development-branch-unity` when implementation is complete and verified

After `brainstorming-unity` writes a spec, explicitly ask whether to proceed to `writing-plans-unity`.

After `writing-plans-unity` writes a plan, explicitly ask whether to use `using-git-worktrees-unity` and then execute with `subagent-driven-development-unity` or `executing-plans-unity`.

## MCPForUnity

MCPForUnity is the required Unity Editor control path.

Before changing scenes, prefabs, assets, packages, ProjectSettings, tests, or runtime behavior:

- confirm the active MCPForUnity target is the intended Unity project
- confirm project identity with `Application.dataPath` through MCPForUnity when Editor access is available
- if multiple Unity Editors are open, select or confirm the correct active instance first
- if MCPForUnity is unavailable or pointed at another project, report that Editor-backed control and runtime verification are unavailable

Do not claim Unity Editor or runtime verification from file-state checks alone.

## Unity Architecture Rules

- Split MonoBehaviours by responsibility.
- Prefer GameObject composition before inheritance.
- Use small interfaces for optional capabilities.
- Use state objects and explicit transitions for mode-specific behavior.
- Use strategy objects for interchangeable calculations or policies.
- Use `ScriptableObject` assets for designer-tunable data.
- Treat scene, prefab, serialized field, package, asmdef, ProjectSettings, and `.meta` changes as implementation surfaces.

## Evidence

Report exactly what was verified:

- MCPForUnity target identity
- compile/domain reload state
- console errors and warnings
- EditMode tests
- PlayMode tests
- scene smoke
- prefab smoke
- asset or serialized-field inspection
- manual runtime observation with reason

## Language

Use the user's conversation language for prose, questions, specs, plans, reviews, `docs/solutions/` entries, and final handoffs.

English structural labels, Markdown headings, YAML keys, and template labels may stay in English. Body prose under those labels must use the user's conversation language.

Keep identifiers, paths, command names, Unity API names, package names, frontmatter values, tags, and quoted source text unchanged.
