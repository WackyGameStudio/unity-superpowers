# Unity Superpowers

This package contains project-local Unity Superpowers skills for coding agents.

## Operating Model

Use the skills in this order for non-trivial Unity work:

1. `unity-init` when project setup, Git state, Unity Editor Bridge, or Editor verification is missing or uncertain
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

## Unity Editor Bridge

Unity Editor integration is modeled as `Unity Editor Bridge`.

Bridge modes:

- `unity_ai_assistant`: Unity AI Assistant + Unity Official MCP Server.
- `mcpforunity`: external coding agent + MCPForUnity.
- `file_only`: no Editor bridge; file-state evidence only.

`unity-init` asks for bridge mode before installing or configuring Editor integration.

Before changing scenes, prefabs, assets, packages, ProjectSettings, tests, or runtime behavior:

- confirm the active Editor bridge target is the intended Unity project
- confirm project identity with `Application.dataPath` through the active bridge when available, or equivalent directly observed Unity evidence
- if multiple Unity Editors are open, select or confirm the correct active instance first
- if no active Editor bridge exists, or it is pointed at another project, report that Editor-backed control and runtime verification are unavailable

Editor-backed claims require active Editor bridge evidence or directly observed Unity evidence. Do not claim Unity Editor or runtime verification from file-state checks alone. `file_only` cannot prove compile, import, runtime, scene, or prefab behavior.

### Unity AI Assistant / Official MCP Setup

Use this branch for the official in-Editor AI workflow.

- Unity AI Assistant path may require Unity 6.3+ for the open beta guide flow.
- Unity AI generally requires Unity 6.0+, an AI package, accepted terms, and a Unity Cloud project link according to the Unity AI product FAQ.
- `com.unity.ai.assistant` is the AI Assistant package named by Unity support docs.
- Unity AI seat, subscription, or trial state can affect MCP or AI Gateway connection.
- Seat changes can require a full Unity Editor restart.
- Do not buy subscriptions, start trials, assign seats, accept terms, or change Cloud links without user approval.

Links: [Unity AI open beta guide](https://support.unity.com/hc/en-us/articles/48060149523476-Getting-started-with-Unity-AI-open-beta-user-guide), [Unity AI product page](https://unity.com/features/ai/), [Unity AI MCP connection error](https://support.unity.com/hc/en-us/articles/48958235901460-Unity-AI-MCP-Connection-Fails-Unity-AI-Gateway-connection-Error).

### MCPForUnity Setup

Use this branch for an external coding agent with MCPForUnity.

- Install after approval with `https://github.com/CoplayDev/unity-mcp.git?path=/MCPForUnity#main`.
- Use `Window > MCP for Unity` setup wizard or client configurator when available.
- Restart or refresh the AI coding agent if MCP tools do not appear.
- Verify active MCPForUnity target and `Application.dataPath` before trusting MCPForUnity tools.

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

- Unity Editor Bridge mode and active Editor bridge target identity
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
