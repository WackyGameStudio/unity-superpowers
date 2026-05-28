# How To Install Unity Superpowers With An AI Agent

You are installing this Unity Superpowers package into a Unity project for a coding agent.

Source package:

```text
unity-superpowers-0.0.1/
  AGENTS.md
  README.md
  HowToInstall_AI.md
  skills/
```

Install only the root guidance file and `skills/` directory needed by the target coding agent. Do not copy repository history, generated Unity folders, unrelated docs, or temporary files.

## Before Installing

1. Confirm the target folder is the Unity project root or the intended project-local agent root.
2. Inspect the target for existing agent guidance and skills.
3. Preserve existing user guidance. Merge intentionally instead of overwriting silently.
4. Use the user's language for explanations. Keep file paths, skill names, Unity API names, package URLs, and command names unchanged.

## Codex Install

For Codex project-local installation, create or update:

```text
<target-project>/
  AGENTS.md
  .agents/
    skills/
```

Steps:

1. Create `.agents/skills/` if it does not exist.
2. Copy every folder under this package's `skills/` into `<target-project>/.agents/skills/`.
3. Copy this package's `AGENTS.md` to `<target-project>/AGENTS.md` if none exists.
4. If `<target-project>/AGENTS.md` already exists, merge the Unity Superpowers sections into it without deleting project-specific rules.
5. Tell the user to restart or refresh Codex if the new skills do not appear immediately.

Codex skill discovery is session-scoped. If `using-superpowers-unity` or another Unity Superpowers skill does not appear, verify the copied path first:

```text
<target-project>/.agents/skills/using-superpowers-unity/SKILL.md
```

If the file exists, start a new Codex session or refresh Codex so it reloads project-local skills. If the file does not exist, the package was not installed into the active project.

## Claude Code Install

For Claude Code project-local installation, prefer the project guidance file that Claude Code reads in that project.

Typical shape:

```text
<target-project>/
  CLAUDE.md
  .claude/
    skills/
```

Steps:

1. Create `.claude/skills/` if the project uses Claude Code project-local skills.
2. Copy every folder under this package's `skills/` into `<target-project>/.claude/skills/`.
3. Convert or merge this package's `AGENTS.md` content into `<target-project>/CLAUDE.md`.
4. Preserve existing Claude Code project rules.
5. Tell the user to restart or refresh Claude Code if skill discovery is not immediate.

## Gemini CLI Install

For Gemini CLI project-local installation, use the project guidance file that Gemini reads.

Typical shape:

```text
<target-project>/
  GEMINI.md
  .gemini/
    skills/
```

Steps:

1. Create `.gemini/skills/` if the project uses Gemini project-local skills.
2. Copy every folder under this package's `skills/` into `<target-project>/.gemini/skills/`.
3. Convert or merge this package's `AGENTS.md` content into `<target-project>/GEMINI.md`.
4. Preserve existing Gemini project rules.
5. Tell the user to restart or refresh Gemini CLI if skill discovery is not immediate.

## Other Coding Agents

If the target agent uses a different project-local convention:

1. Identify the agent's project guidance filename.
2. Identify the agent's project-local skill directory.
3. Copy `skills/` into that directory.
4. Convert or merge `AGENTS.md` into the agent-specific guidance file.
5. Keep the skill folder names unchanged.
6. Preserve existing project guidance.

## Verification

After installation, verify:

- all 16 skill folders are present
- every skill folder contains `SKILL.md`
- installed guidance mentions MCPForUnity as the Unity Editor control path
- installed guidance tells the agent not to claim Unity Editor or runtime verification from file-state checks alone
- existing project-specific guidance was preserved

If the target project already has Unity-specific skills, report conflicts before replacing them.
