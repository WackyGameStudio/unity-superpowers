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
