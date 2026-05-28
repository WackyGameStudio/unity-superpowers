# Unity Superpowers 0.0.1

English | [한국어](README_kr.md)

Unity Superpowers is a lightweight project-local skill pack for AI-assisted Unity game development.

It keeps the Superpowers workflow discipline while focusing on Unity-specific work: project setup, MCPForUnity, scenes, prefabs, serialized data, packages, tests, debugging, review, and verification.

The intended first step is `unity-init`. It audits or prepares the Unity project before feature work so the agent knows the real project path, Git state, Unity Editor target, MCPForUnity status, and verification surface.

## Contents

```text
unity-superpowers-0.0.1/
  AGENTS.md
  HowToInstall_AI.md
  README.md
  README_kr.md
  skills/
    brainstorming-unity/
    compound-unity/
    dispatching-parallel-agents-unity/
    executing-plans-unity/
    finishing-a-development-branch-unity/
    receiving-code-review-unity/
    requesting-code-review-unity/
    subagent-driven-development-unity/
    systematic-debugging-unity/
    test-driven-development-unity/
    unity-init/
    using-git-worktrees-unity/
    using-superpowers-unity/
    verification-before-completion-unity/
    writing-plans-unity/
    writing-skills-unity/
```

## Core Flow

For non-trivial Unity work:

1. Initialize or audit the project with `unity-init`.
2. Shape the feature with `brainstorming-unity`.
3. Write a concrete implementation plan with `writing-plans-unity`.
4. Execute the plan with `subagent-driven-development-unity` or `executing-plans-unity`.
5. Use `test-driven-development-unity`, `systematic-debugging-unity`, and review skills as needed.
6. Verify with `verification-before-completion-unity`.
7. Capture reusable lessons with `compound-unity`.

## Development Philosophy

Unity Superpowers keeps the original Superpowers discipline: understand before building, test behavior before implementation when feasible, find root cause before fixing, isolate work, review early, verify before claiming completion, and preserve reusable lessons.

The Unity adaptation adds one rule: Unity project state is more than code. Scenes, prefabs, `.meta` files, `ScriptableObject` assets, package manifests, asmdefs, ProjectSettings, serialized fields, layers, Animator parameters, physics settings, and active Editor targets are implementation surfaces. A Unity agent must reason about these surfaces explicitly instead of treating them as afterthoughts.

Architecture guidance is also Unity-specific. Prefer small `MonoBehaviour` responsibilities, GameObject composition, narrow capability interfaces, `State` and transition rules for mode-specific behavior, `Strategy` for variable policy/calculation, and `ScriptableObject` assets for designer-tunable data. Runtime or Editor-backed claims require fresh Unity evidence through MCPForUnity, tests, console/import checks, scene smoke, prefab smoke, or clearly stated manual evidence.

## Skill Guide

| Skill | Unity-specific focus | How it extends Superpowers |
| --- | --- | --- |
| `using-superpowers-unity` | Routes each Unity request to the Unity-specific skill set and checks project readiness, project-local skills, `docs/solutions/`, and MCPForUnity target identity. | Keeps the "use the right skill first" discipline while preventing fallback to generic workflows for Unity scene, prefab, and Editor work. |
| `unity-init` | Audits or creates Unity project structure, Git state, package state, MCPForUnity setup, active Editor target, import/compile/console evidence, and smoke-test readiness. | Turns Superpowers setup discipline into a Unity workspace readiness gate before design or implementation. |
| `brainstorming-unity` | Asks Unity-native design questions: genre loop, input source, movement model, camera, scene/prefab boundaries, component ownership, animation, physics, UI, data assets, packages, and verification surface. | Keeps design-before-build, but makes the design include Unity architecture and Editor/runtime wiring rather than only code behavior. |
| `writing-plans-unity` | Plans code, scene, prefab, asset, serialized-field, package/settings, asmdef, test, and MCPForUnity work with exact paths and expected evidence. | Keeps implementation plans executable for a fresh worker, with Unity surfaces and verification treated as first-class tasks. |
| `using-git-worktrees-unity` | Requires isolated workspace setup before risky Unity changes, including `.unity`, `.prefab`, `.asset`, `.meta`, packages, and ProjectSettings edits. | Keeps work isolation while accounting for Unity-generated files and serialized asset merge risk. |
| `subagent-driven-development-unity` | Splits work by Unity ownership boundaries: runtime scripts, editor tooling, asmdefs/packages, tests, scene integration, prefab integration, and data assets. | Keeps fresh subagent per task and two-stage review, but forbids parallel edits to shared Unity serialized state. |
| `dispatching-parallel-agents-unity` | Allows parallel work only across independent Unity surfaces and makes shared scenes, prefabs, assets, manifests, `.meta`, and ProjectSettings sequential. | Keeps parallelism useful without trading speed for Unity serialization conflicts. |
| `executing-plans-unity` | Executes approved plans with checkpoints for MCPForUnity target, Unity surfaces, compile/console, tests, scene smoke, and prefab smoke. | Keeps plan execution disciplined when subagents are unavailable or a separate execution flow is preferred. |
| `test-driven-development-unity` | Applies TDD to Unity with pure C#, EditMode, PlayMode, condition-based waits, physics-aware waits, and copy-safe Unity C# examples. | Keeps red-green-refactor while respecting Unity test mode boundaries and runtime timing. |
| `systematic-debugging-unity` | Traces Unity bugs through console logs, Editor state, package/import state, scene/prefab wiring, serialized references, physics timing, and MCPForUnity target mismatches. | Keeps root-cause-first debugging and adds Unity evidence paths before changing code or assets. |
| `requesting-code-review-unity` | Reviews code and Unity artifacts together: `MonoBehaviour` boundaries, interfaces, state/strategy/data assets, serialized wiring, scene/prefab/asset changes, asmdefs, packages, and evidence. | Keeps early review while making Unity behavior risk part of the review surface. |
| `receiving-code-review-unity` | Evaluates feedback technically before applying it and verifies Unity-specific claims with compile, console, tests, asset inspection, or runtime evidence. | Keeps review rigor and prevents unverified changes to Unity wiring or architecture. |
| `verification-before-completion-unity` | Requires target identity, `Application.dataPath`, compile state, console state, EditMode/PlayMode tests, asset inspection, scene/prefab smoke, or explicit limitation reporting. | Keeps evidence-before-assertions and blocks runtime claims from file-only checks. |
| `finishing-a-development-branch-unity` | Finalizes Unity work only after fresh verification and then guides merge, PR, preserve, discard, or cleanup choices. | Keeps branch completion explicit while protecting Unity assets and generated state. |
| `compound-unity` | Captures solved Unity blockers and reusable lessons about MCPForUnity, Editor state, scene/prefab serialization, `.meta` GUIDs, package issues, test timing, and architecture decisions. | Keeps lessons reusable so future agents do not rediscover Unity-specific workarounds. |
| `writing-skills-unity` | Creates or revises Unity process skills with pressure scenarios involving scene verification, prefab wiring, PlayMode timing, MCPForUnity, and oversized `MonoBehaviour` risks. | Keeps skill-writing as TDD for process documentation, with Unity-specific failure modes in the tests. |

## What unity-init Does

`unity-init` prepares or repairs a Unity workspace before implementation work. It does not silently mutate the project. It explains the change and asks for approval before project creation, Git setup, package installation, MCPForUnity configuration, Codex config edits, remotes, or Git LFS setup.

It checks:

- Unity project markers: `Assets/`, `Packages/manifest.json`, `ProjectSettings/ProjectVersion.txt`
- Git repository and remote state
- installed Unity Editors and available project templates
- MCPForUnity package/config/tool visibility
- active MCPForUnity target and `Application.dataPath`
- import, compile, console, EditMode, and PlayMode verification surface

If the current folder is not a Unity project, `unity-init` asks whether to create the project automatically or wait for manual Unity Hub creation. For automatic creation, it asks for the missing project-shaping choices:

- project name
- Unity version or installed Editor
- template, such as `2D`, `3D`, `URP`, `HDRP`, or `Mobile`
- render pipeline: `Built-in`, `URP`, or `HDRP`
- target platform

For automatic creation, it verifies the selected template before touching the real folder. If Unity project creation does not apply the requested template correctly, it can use the template `ProjectData~` fallback while preserving `.meta` files and avoiding blind overwrites.

It can also set up the Unity development harness:

- initialize Git after approval
- create or merge a Unity `.gitignore`
- ask for a remote URL before adding a remote
- offer Git LFS for large binary assets
- add MCPForUnity to the Unity project after approval
- configure Codex through the MCPForUnity configurator when available
- verify the active Unity Editor target before trusting Unity tools

Final reporting from `unity-init` should include the project path, Unity version, creation path, template, render pipeline, target platform, manifest changes, Git state, MCPForUnity state, active target evidence, compile/console evidence, test readiness, limitations, and the next recommended skill.

## Unity Assumptions

- MCPForUnity is the Editor control path.
- Editor-backed claims require fresh evidence from MCPForUnity or directly observed Unity results.
- File checks alone are not runtime proof.
- Scene, prefab, `.meta`, package, asmdef, ProjectSettings, and serialized-field changes are first-class implementation surfaces.
- Multiple Unity Editor instances must be treated as a routing risk until the active MCPForUnity target is verified.

## MCPForUnity Setup

MCPForUnity is the required Editor integration path for this pack. `unity-init` can install and configure it after approval by adding the Unity package to the project, running the MCPForUnity client configurator when available, and checking that Codex can see the Unity MCP tools.

Manual setup:

1. In Unity, open `Window > Package Manager > + > Add package from git URL`.
2. Paste `https://github.com/CoplayDev/unity-mcp.git?path=/MCPForUnity#main`.
3. After import, open `Window > MCP for Unity`.
4. Use the setup wizard or client configurator to configure the detected AI client.
5. Restart/refresh the AI coding agent if MCP tools do not appear.
6. Before using Unity tools, verify the active MCPForUnity target and `Application.dataPath`.

Official MCPForUnity docs list Unity 2021.3 LTS or newer, Python 3.10+ with `uv`, and an MCP client as prerequisites. The same docs list Git URL, Asset Store, and OpenUPM install paths.

Links: [MCP for Unity GitHub](https://github.com/CoplayDev/unity-mcp), [install docs](https://coplaydev.github.io/unity-mcp/getting-started/install), [OpenUPM package](https://openupm.com/packages/com.coplaydev.unity-mcp/).

## Install

Ask an AI coding agent to read `HowToInstall_AI.md` and install this pack into the target project for the agent you use.

For Codex, the target shape is usually:

```text
<UnityProject>/
  AGENTS.md
  .agents/
    skills/
      <all skill folders>
```

After installation, restart or refresh the coding agent if it does not discover project-local skills immediately.
