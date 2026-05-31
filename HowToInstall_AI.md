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

## Unity Editor Bridge Install Choice

Install the skill pack first. `unity-init` asks for bridge mode before installing or configuring Editor integration.

Bridge modes:

- `unity_ai_assistant`: Unity AI Assistant + Unity MCP Server.
- `mcpforunity`: external coding agent + MCPForUnity.

Editor-backed claims require Unity AI Assistant / Unity MCP or MCPForUnity evidence.

### Unity AI Assistant / Unity MCP Setup

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

1. In Unity, open `Window > Package Manager > + > Add package from git URL`.
2. Paste `https://github.com/CoplayDev/unity-mcp.git?path=/MCPForUnity#main`.
3. After import, open `Window > MCP for Unity`.
4. Use the setup wizard or client configurator to configure the detected AI client.
5. Restart or refresh the AI coding agent if MCP tools do not appear.
6. Before using Unity tools, verify the active MCPForUnity target and `Application.dataPath`.

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
- installed guidance defines Unity Editor Bridge modes: `unity_ai_assistant` and `mcpforunity`
- installed guidance keeps MCPForUnity setup only under the MCPForUnity Setup branch
- installed guidance tells the agent to verify Unity Editor/runtime claims through Unity AI Assistant / Unity MCP or MCPForUnity evidence
- existing project-specific guidance was preserved

If the target project already has Unity-specific skills, report conflicts before replacing them.
