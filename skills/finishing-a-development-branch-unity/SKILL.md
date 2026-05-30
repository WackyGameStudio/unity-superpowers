---
name: finishing-a-development-branch-unity
description: Use when Unity implementation is complete, verification evidence is fresh, and you need to decide how to integrate the work through merge, PR, preserve, or discard
---

# Finishing a Development Branch

## Overview

Guide completion of Unity development work by verifying evidence, presenting clear options, and handling the chosen workflow safely.

**Core principle:** Verify Unity evidence, detect environment, present options, execute choice, clean up.

**Announce at start:** "I'm using the finishing-a-development-branch-unity skill to complete this work."

## Unity Finish Checks

Before presenting finish options, check:

- active Editor bridge target identity, plus `Application.dataPath` through the active bridge when available, when Editor work was involved
- compile/domain reload state
- Unity console errors and warnings after the final refresh
- relevant EditMode tests
- relevant PlayMode tests or explicit skipped reason
- scene smoke, prefab smoke, asset inspection, or manual runtime evidence when runtime behavior changed
- changed scenes and prefabs are intentional
- `.meta` files are present for new Unity assets
- package lock, asmdef, and ProjectSettings changes are intentional
- large binary assets are expected and Git LFS guidance is noted when applicable
- `docs/solutions/` capture was considered for non-trivial Unity lessons

Do not claim Unity Editor or runtime verification from file-state checks alone.

## The Process

### Step 1: Verify Unity Evidence

Before presenting options, verify the strongest relevant Unity evidence available.

Use the project's actual commands or active bridge tools or evidence. Typical evidence chain:

```text
Editor bridge mode -> active Editor bridge target identity -> Application.dataPath through the active bridge when available -> refresh/import evidence -> console evidence -> EditMode tests -> PlayMode tests -> scene/prefab smoke
```

If no Editor bridge is available, report the limitation and use only valid fallback evidence. Do not claim Editor/runtime proof.

**If verification fails:**

```text
Verification failing (<N> failures). Must fix before completing:

[Show failures]

Cannot proceed with merge/PR until verification passes.
```

Stop. Do not proceed to Step 2.

**If verification passes or limitations are explicit and accepted:** Continue to Step 2.

### Step 2: Detect Environment

Determine workspace state before presenting options:

```bash
GIT_DIR=$(cd "$(git rev-parse --git-dir)" 2>/dev/null && pwd -P)
GIT_COMMON=$(cd "$(git rev-parse --git-common-dir)" 2>/dev/null && pwd -P)
BRANCH=$(git branch --show-current)
```

This determines which menu to show and how cleanup works:

| State | Menu | Cleanup |
|-------|------|---------|
| `GIT_DIR == GIT_COMMON` normal repo | Standard 4 options | No worktree to clean up |
| `GIT_DIR != GIT_COMMON`, named branch | Standard 4 options | Provenance-based (see Step 6) |
| `GIT_DIR != GIT_COMMON`, detached HEAD | Reduced 3 options | No cleanup unless platform owns an exit flow |

### Step 3: Determine Base Branch

```bash
git merge-base HEAD main 2>/dev/null || git merge-base HEAD master 2>/dev/null
```

If ambiguous, ask: "This branch split from `<base-branch>` - is that correct?"

### Step 4: Present Options

**Normal repo and named-branch worktree - present exactly these 4 options:**

```text
Implementation complete. What would you like to do?

1. Merge back to <base-branch> locally
2. Push and create a Pull Request
3. Keep the branch as-is
4. Discard this work

Which option?
```

**Detached HEAD - present exactly these 3 options:**

```text
Implementation complete. You're on a detached HEAD or externally managed workspace.

1. Push as new branch and create a Pull Request
2. Keep as-is
3. Discard this work

Which option?
```

Use the user's conversation language for the actual question. Keep branch names and commands unchanged.

### Step 5: Execute Choice

#### Option 1: Merge Locally

```bash
MAIN_ROOT=$(git -C "$(git rev-parse --git-common-dir)/.." rev-parse --show-toplevel)
cd "$MAIN_ROOT"

git checkout <base-branch>
git pull
git merge <feature-branch>
```

Verify Unity evidence again on the merged result before cleanup:

```text
<Unity verification commands or active bridge checks>
```

Only after merge and verification succeed, run Step 6 and delete the branch:

```bash
git branch -d <feature-branch>
```

#### Option 2: Push and Create PR

```bash
git push -u origin <feature-branch>

gh pr create --title "<title>" --body "$(cat <<'EOF'
## Summary
<2-3 bullets of what changed>

## Test Plan
- [ ] <Unity verification evidence>
EOF
)"
```

Do NOT clean up the worktree. The user needs it alive to iterate on PR feedback.

#### Option 3: Keep As-Is

Report: "Keeping branch `<name>`. Worktree preserved at `<path>`."

Do not clean up the worktree.

#### Option 4: Discard

Confirm first:

```text
This will permanently delete:
- Branch <name>
- All commits: <commit-list>
- Worktree at <path>

Type 'discard' to confirm.
```

Wait for exact confirmation.

If confirmed:

```bash
MAIN_ROOT=$(git -C "$(git rev-parse --git-common-dir)/.." rev-parse --show-toplevel)
cd "$MAIN_ROOT"
```

Then run Step 6 and force-delete the branch:

```bash
git branch -D <feature-branch>
```

### Step 6: Cleanup Workspace

Only runs for Options 1 and 4. Options 2 and 3 always preserve the worktree.

```bash
GIT_DIR=$(cd "$(git rev-parse --git-dir)" 2>/dev/null && pwd -P)
GIT_COMMON=$(cd "$(git rev-parse --git-common-dir)" 2>/dev/null && pwd -P)
WORKTREE_PATH=$(git rev-parse --show-toplevel)
```

**If `GIT_DIR == GIT_COMMON`:** Normal repo, no worktree to clean up. Done.

**If worktree path is under `.worktrees/`, `worktrees/`, or `~/.config/superpowers/worktrees/`:** Unity Superpowers created this worktree; we own cleanup.

```bash
MAIN_ROOT=$(git -C "$(git rev-parse --git-common-dir)/.." rev-parse --show-toplevel)
cd "$MAIN_ROOT"
git worktree remove "$WORKTREE_PATH"
git worktree prune
```

**Otherwise:** The host environment owns this workspace. Do NOT remove it. If your platform provides a workspace-exit tool, use it. Otherwise, leave the workspace in place.

## Quick Reference

| Option | Merge | Push | Keep Worktree | Cleanup Branch |
|--------|-------|------|---------------|----------------|
| 1. Merge locally | yes | - | - | yes |
| 2. Create PR | - | yes | yes | - |
| 3. Keep as-is | - | - | yes | - |
| 4. Discard | - | - | - | yes, after confirmation |

## Common Mistakes

**Skipping Unity verification**
- **Problem:** Merge broken Unity state or create a failing PR
- **Fix:** Verify compile, console, tests, and relevant scene/prefab evidence before offering options

**Open-ended questions**
- **Problem:** "What should I do next?" is ambiguous
- **Fix:** Present exactly 4 structured options, or 3 for detached HEAD

**Cleaning up worktree for Option 2**
- **Problem:** Remove worktree user needs for PR iteration
- **Fix:** Only cleanup for Options 1 and 4

**Deleting branch before removing worktree**
- **Problem:** `git branch -d` fails because worktree still references the branch
- **Fix:** Merge first, remove worktree, then delete branch

**Running git worktree remove from inside the worktree**
- **Problem:** Command fails silently when CWD is inside the worktree being removed
- **Fix:** Always `cd` to main repo root before `git worktree remove`

**Cleaning up host-owned worktrees**
- **Problem:** Removing a worktree the host created causes phantom state
- **Fix:** Only clean up worktrees under `.worktrees/`, `worktrees/`, or `~/.config/superpowers/worktrees/`

**No confirmation for discard**
- **Problem:** Accidentally delete work
- **Fix:** Require typed `discard` confirmation

## Red Flags

**Never:**
- Proceed with failing verification
- Merge without verifying Unity evidence on the merged result
- Delete work without confirmation
- Force-push without explicit request
- Remove a worktree before confirming merge success
- Clean up worktrees you did not create
- Run `git worktree remove` from inside the worktree

**Always:**
- Verify Unity evidence before offering options
- Detect environment before presenting menu
- Present exactly 4 options, or 3 for detached HEAD
- Get typed confirmation for discard
- Clean up worktree for Options 1 and 4 only
- `cd` to main repo root before worktree removal
- Run `git worktree prune` after removal
