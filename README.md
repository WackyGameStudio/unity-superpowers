# Unity Superpowers 0.0.1

Unity Superpowers is a lightweight project-local skill pack for AI-assisted Unity game development.

It keeps the Superpowers workflow discipline while focusing on Unity-specific work: project setup, MCPForUnity, scenes, prefabs, serialized data, packages, tests, debugging, review, and verification.

## Contents

```text
unity-superpowers-0.0.1/
  AGENTS.md
  HowToInstall_AI.md
  README.md
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

## Unity Assumptions

- MCPForUnity is the Editor control path.
- Editor-backed claims require fresh evidence from MCPForUnity or directly observed Unity results.
- File checks alone are not runtime proof.
- Scene, prefab, `.meta`, package, asmdef, ProjectSettings, and serialized-field changes are first-class implementation surfaces.

## MCPForUnity Setup

Install MCP for Unity in the Unity project first:

1. In Unity, open `Window > Package Manager > + > Add package from git URL`.
2. Paste `https://github.com/CoplayDev/unity-mcp.git?path=/MCPForUnity#main`.
3. Open `Window > MCP for Unity > Configure All Detected Clients`.
4. Restart/refresh the AI coding agent if the MCP tools do not appear.
5. Before using Unity tools, verify the active MCPForUnity target and `Application.dataPath`.

Links: [MCP for Unity GitHub](https://github.com/CoplayDev/unity-mcp), [install docs](https://coplaydev.github.io/unity-mcp), [OpenUPM package](https://openupm.com/packages/com.coplaydev.unity-mcp/).

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
