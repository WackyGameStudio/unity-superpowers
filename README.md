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
