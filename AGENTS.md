# Unity Superpowers

This package contains project-local Unity Superpowers skills for coding agents.

## Operating Model

Use the skills in this order for non-trivial Unity work:

1. `unity-init` when project setup, Git state, MCPForUnity, or Editor verification is missing or uncertain
2. `brainstorming-unity` before gameplay features, tools, packages, scenes, prefabs, or behavior changes
3. `writing-plans-unity` after a design is approved and before implementation
4. `subagent-driven-development-unity` or `executing-plans-unity` to execute a plan
5. `test-driven-development-unity` for feature and bugfix implementation
6. `systematic-debugging-unity` for failures, regressions, console errors, broken scene behavior, or package issues
7. `requesting-code-review-unity` and `receiving-code-review-unity` for review loops
8. `verification-before-completion-unity` before any completion claim
9. `compound-unity` after a reusable Unity workaround or lesson is verified
10. `finishing-a-development-branch-unity` when implementation is complete and verified

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

Keep identifiers, paths, command names, Unity API names, package names, frontmatter values, tags, and quoted source text unchanged.
