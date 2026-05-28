---
name: unity-init
description: Use when starting or repairing a Unity project workspace for Codex, especially when Unity project markers, Git, MCPForUnity, Codex config, or Editor verification may be missing
---

# Unity Init

## Overview

Prepare a folder so Codex can work as a Unity project operator with correct project identity, Git state, MCPForUnity access, tool groups, compile/console evidence, and smoke-test readiness.

Ask questions and write user-facing guidance in the user's language. Preserve identifiers, paths, commands, Unity API names, package URLs, config paths, frontmatter values, and quoted source text exactly.

Do not silently create a project, initialize Git, install packages, edit Codex config, add remotes, or mutate Unity assets/settings. Explain what would change, ask for approval, and proceed only after the user confirms.

## Detection Order

Check in this order and report what each check proves.

1. Unity project markers:
   - `Assets/`
   - `Packages/manifest.json`
   - `ProjectSettings/ProjectVersion.txt`
2. Git:
   - `git rev-parse --show-toplevel`
3. Unity creation paths:
   - Unity Hub CLI
   - installed Unity Editors
   - known editor executable paths such as `%ProgramFiles%\Unity\Hub\Editor\<version>\Editor\Unity.exe`
   - any existing `ProjectSettings/ProjectVersion.txt` that names a target Unity version
4. MCPForUnity:
   - `Packages/manifest.json`
   - Codex MCP config
   - MCPForUnity package visibility
   - MCPForUnity tool visibility
5. Target identity:
   - MCPForUnity active project
   - `Application.dataPath` queried through MCPForUnity

If MCPForUnity is missing, stale, or aimed at the wrong project, use only file checks and report that Editor-backed control and runtime verification are unavailable.

## No Project Flow

If the folder does not contain Unity project markers, ask whether the user wants automatic project creation or manual Unity Hub creation.

If the user chooses manual creation, stop. Tell the user to create the Unity project in this folder and say when ready. Do not continue into Git setup, MCPForUnity setup, or Codex config changes until the project exists or the user explicitly redirects.

If automatic creation is feasible, ask only for missing decisions:

- project name
- Unity version or installed Editor executable
- template: `2D`, `3D`, `URP`, `HDRP`, `Mobile`, or another installed template
- render pipeline: `Built-in`, `URP`, or `HDRP`
- target platform

Do not invent defaults silently when choices affect project shape. If a choice can be inferred from an existing file or explicit user request, state the inference and ask only for the remaining missing choice.

When automatic creation is not feasible, explain which creation path is missing, such as Unity Hub CLI, installed editor, or known template metadata. Then offer the manual Unity Hub path.

## Template Resolution

For automatic project creation, resolve the requested Unity template before mutating the target folder.

1. Locate the selected Editor, then inspect installed templates under:

```text
<UnityEditor>\Editor\Data\Resources\PackageManager\ProjectTemplates
```

2. For candidate `.tgz` templates, extract into a temporary folder and inspect:
   - `package/package.json`
   - `package/ProjectData~`
3. Match the user-facing template request against `displayName`, package `name`, package filename, render pipeline, and platform intent. For example, a `3D URP` request may correspond to a template package whose `displayName` is `3D URP` even when the archive filename uses another naming convention.
4. If no installed template clearly matches, do not guess. Report the installed template options and ask the user to choose or use manual Unity Hub creation.

## Automatic Creation Strategy

Treat Unity automatic creation as a verified strategy, not a trusted single command.

Before creating in the real project folder, run a smoke creation in a temporary folder when using `Unity.exe -createProject` or `-createProjectTemplate`.

After the smoke run, inspect the generated `Packages/manifest.json`, `Assets/`, and `ProjectSettings/`:

- If the generated manifest reflects the requested template, render pipeline, and key dependencies, the command path can be used.
- If the command only creates generic Unity project markers or misses the requested template dependencies, do not use that result as proof. Switch to the `ProjectData~` fallback.
- If the real target folder already contains user files such as `.agents/`, docs, or repository metadata, first smoke-test non-empty-folder behavior in a temporary folder containing a sentinel file. Confirm that the sentinel is preserved before considering real-folder creation.

## ProjectData Fallback

Use `ProjectData~` fallback when Unity's creation command is available but does not apply the requested template correctly.

Fallback steps:

1. Extract the selected template archive to a temporary folder.
2. Copy only Unity source surfaces from `package/ProjectData~` into the target project:
   - `Assets/`
   - `Packages/`
   - `ProjectSettings/`
3. If `ProjectVersion.txt` is missing, create it from the selected Editor version and revision. Prefer evidence from the installed Editor or a temporary smoke-created project.
4. Do not overwrite existing user files silently. If a target file already exists, inspect it, report the collision, and merge only after approval.
5. Preserve `.meta` files from the template. Do not regenerate or delete `.meta` files as a cleanup shortcut.

## Manifest Compatibility Repair

After automatic creation or `ProjectData~` fallback, compare `Packages/manifest.json` against the selected Editor's bundled package manifest:

```text
<UnityEditor>\Editor\Data\Resources\PackageManager\Editor\manifest.json
```

Check direct dependencies that commonly drift between templates and Editor patch versions, including:

- `com.unity.inputsystem`
- `com.unity.render-pipelines.universal`
- `com.unity.render-pipelines.high-definition`
- `com.unity.test-framework`
- `com.unity.visualscripting`
- IDE integration packages

If an installed template pins an older direct dependency that fails or conflicts with the selected Editor, update the project manifest to the Editor-compatible bundled version. Explain the exact package version change before editing. Do not downgrade a dependency unless the user explicitly approves and there is evidence the selected Editor supports it.

## First Import Recovery

Run the first import in Unity batchmode after project files exist.

Use `-projectPath`, `-batchmode`, `-nographics`, `-quit`, and an explicit log file under the project or a temporary diagnostics folder.

If the first import fails with compile or package errors:

1. Read the log and identify the failing package, compiler error, or package-resolution conflict.
2. Fix the manifest or project setting that caused the failure.
3. Remove only generated import state before retrying:
   - `Library/`
   - `Packages/packages-lock.json`
4. Do not remove `Assets/`, `Packages/manifest.json`, `ProjectSettings/`, `.meta` files, or user-authored docs/scripts as part of recovery.
5. Re-run import and record the final log path and exit code.

Do not treat a successful later import as proof that earlier log errors vanished. State which log is authoritative for the final result.

## Project Identity Normalization

Templates can leave template names in project settings. After creation, inspect `ProjectSettings/ProjectSettings.asset` and normalize identity fields when the user provided or approved values:

- `companyName`
- `productName`
- platform application identifiers such as Android, Standalone, and iPhone bundle identifiers

Ask for missing company/publisher or application identifier decisions when they affect build output or store identity. For throwaway prototypes, state the inferred values before editing.

## Git Setup

If no Git repository exists, ask before running `git init`.

If a repository exists, report the toplevel path from `git rev-parse --show-toplevel` and do not reinitialize it.

Ask whether to add a remote. If the user wants a remote and no URL was provided, request the URL before running any `git remote add` command. Do not add or replace remotes without approval.

Create or merge a Unity `.gitignore` only after checking whether one already exists. Preserve existing project-specific ignores. A Unity `.gitignore` should normally ignore generated folders and files such as `Library/`, `Temp/`, `Obj/`, `Build/`, `Builds/`, `Logs/`, `UserSettings/`, `.vs/`, `.idea/`, and generated solution/project files, while preserving tracked Unity source surfaces such as `Assets/**/*.meta`, `Packages/`, `ProjectSettings/`, and intended source assets.

Offer Git LFS for large binary/art-heavy projects, especially projects with large textures, audio, video, models, or frequent art asset churn. Do not install, initialize, or configure Git LFS without approval.

## MCPForUnity Setup

Explain that MCPForUnity will be installed/configured and ask for approval before installing packages, changing `Packages/manifest.json`, running configurators, editing Codex config, or creating skill files.

Use the project-approved MCPForUnity package source. Newer MCPForUnity versions may be used after checking availability. If version freshness cannot be checked, say so and use the approved package URL or the version already pinned by the project.

Default UPM URL:

```text
https://github.com/CoplayDev/unity-mcp.git?path=/MCPForUnity#main
```

Use a local source override or embedded package only after explicit approval. State why the override is needed and what path will be referenced before mutating the project.

Configure Codex through the MCPForUnity configurator when possible. Mention affected config locations before changing them, including global Codex MCP configuration and any project-local guidance or skill directories.

If Codex must be restarted for MCP server or skill discovery changes to take effect, tell the user exactly when the restart is required.

## Verification Ladder

Use this ladder after initialization or when auditing an existing folder. Stop at the highest evidence level available and report any missing surface.

1. Project identity:
   - confirm Unity version from `ProjectSettings/ProjectVersion.txt`
   - confirm `Application.dataPath` through MCPForUnity
2. MCP connection and editor state:
   - query editor state through MCPForUnity
   - if MCPForUnity is unavailable, state that Editor control and runtime verification are not available
3. Multi-instance active target:
   - if multiple Unity Editors are open, confirm the active target points at this project before scene, prefab, asset, package, or test changes
   - use MCPForUnity active instance controls such as `set_active_instance` when available
4. Tool groups:
   - run `manage_tools list_groups`
   - run `sync` when tool visibility is stale
   - activate needed groups such as `testing`, `docs`, `ui`, `vfx`, and `animation`
5. Compile and console:
   - prefer `validate_script`, `refresh_unity`, and `read_console`
   - if MCPForUnity is unavailable, report that compile and console evidence is limited to file-state or external batchmode checks
6. Import and target verification:
   - for newly generated projects, run batchmode import and capture the log path
   - switch each requested target platform in batchmode, for example `StandaloneWindows64` and `Android`
   - after target checks, restore the user's preferred working target if they named one
   - scan the final authoritative logs for `error CS`, `Scripts have compiler errors`, `return code 1`, `Aborting batchmode`, `Exception`, and `Error`
   - distinguish stale errors in earlier failed logs from the final target verification logs
7. Test readiness:
   - run an EditMode smoke test when the Test Framework is available
   - run a PlayMode smoke test when project startup allows it
   - use MCPForUnity `run_tests` and `get_test_job` where available
8. Final report:
   - project path
   - Unity version
   - creation path used: Unity command, Unity Hub/manual, or `ProjectData~` fallback
   - template package and display name when known
   - render pipeline
   - target platforms requested and verified
   - manifest compatibility changes
   - Git state
   - remote state
   - Git LFS state if considered
   - MCPForUnity package/config state
   - active MCPForUnity target evidence
   - enabled tool groups
   - import, compile, console, and target-switch evidence
   - EditMode and PlayMode readiness
   - limitations when only file checks were possible
   - next recommended skill

## Safety Constraints

- Do not delete existing Unity assets, scenes, prefabs, `.meta` files, packages, or `ProjectSettings/` content.
- Do not initialize Git, install packages, edit Codex config, configure MCPForUnity, add remotes, or configure Git LFS without approval.
- Do not trust `Unity.exe -createProjectTemplate` until a temporary smoke project proves the generated manifest and template surfaces match the user's request.
- Do not use `ProjectData~` fallback as a blind overwrite. Treat every existing `Assets/`, `Packages/`, and `ProjectSettings/` collision as a merge decision.
- If multiple Unity Editors are open, confirm the active instance before scene, prefab, asset, package, or test changes.
- Do not claim Unity Editor, runtime, compile, console, EditMode, or PlayMode verification from file-only checks.
- Report limitations plainly when MCPForUnity, Unity Hub, installed Editors, or network version checks are unavailable.
- Preserve unrelated user or agent edits. If an existing file must be merged, inspect it first and make the smallest project-setup change.

## Next Skill Routing

After successful initialization, recommend the next Unity Superpowers skill based on the user's goal.

- Use `brainstorming-unity` when the user wants to design a feature, gameplay behavior, scene, prefab workflow, package choice, or architecture direction.
- Use `verification-before-completion-unity` when the user wants a readiness audit of an already-initialized project or needs proof that setup is complete.
- Use `compound-unity` after a non-obvious Unity initialization workaround, template fallback, package compatibility repair, target-switch failure, stale MCP binding, or repeated import recovery. Write the reusable lesson in the user's language unless the project documentation uses another language.
