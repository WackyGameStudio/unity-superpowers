---
name: verification-before-completion-unity
description: Use when about to claim Unity work is complete, fixed, or passing, before committing or creating PRs; evidence before assertions always
---

# Verification Before Completion

## Overview

Claiming Unity work is complete without verification is dishonesty, not efficiency.

**Core principle:** Evidence before claims, always.

**Violating the letter of this rule is violating the spirit of this rule.**

## Unity Evidence Ladder

Before claiming Unity work is complete, gather fresh evidence:

1. Target identity: MCPForUnity active instance.
2. Project identity: `Application.dataPath` queried through MCPForUnity.
3. Compile state: wait until Unity is not compiling.
4. Console: read errors and warnings after refresh/domain reload.
5. Tests: run relevant EditMode and PlayMode tests.
6. Asset proof: inspect changed prefabs, scenes, ScriptableObjects, packages, asmdefs, and `.meta` files.
7. Runtime proof: run scene/prefab smoke or manual check when behavior is visual, physics-driven, animation-driven, or input-driven.

Do not claim Unity Editor or runtime verification if only file-state checks ran.

## The Iron Law

```text
NO COMPLETION CLAIMS WITHOUT FRESH VERIFICATION EVIDENCE
```

If you have not run the verification command in this message, you cannot claim it passes.

## The Gate Function

Before claiming any status or expressing satisfaction:

1. **IDENTIFY:** What command or MCPForUnity evidence proves this claim?
2. **RUN:** Execute the full command or tool call fresh.
3. **READ:** Read full output, exit code, console entries, and failure counts.
4. **VERIFY:** Does output confirm the claim?
   - If no: state actual status with evidence.
   - If yes: state claim with evidence.
5. **ONLY THEN:** Make the claim.

Skip any step = lying, not verifying.

## Common Failures

| Claim | Requires | Not Sufficient |
|-------|----------|----------------|
| Tests pass | EditMode/PlayMode output: 0 failures | Previous run, "should pass" |
| Unity console clean | `read_console` or authoritative log after refresh | File scan, stale console memory |
| Compile succeeds | Unity compile/domain reload evidence | C# file exists, linter passing |
| Scene wired | scene/prefab inspection or smoke evidence | Script compiled |
| Prefab wired | prefab inspection showing serialized references | Code path exists |
| Bug fixed | Original symptom reproduced and now passes | Code changed, assumed fixed |
| Regression test works | Red-green cycle verified | Test passes once |
| Agent completed | VCS diff and Unity evidence verified | Agent reports "success" |
| Requirements met | Line-by-line checklist plus Unity surface evidence | Tests passing only |

## Red Flags - STOP

- Using "should", "probably", "seems to"
- Expressing satisfaction before verification
- About to commit/push/PR without verification
- Trusting agent success reports
- Relying on partial verification
- Thinking "just this once"
- Tired and wanting work over
- Any wording implying success without having run verification

## Rationalization Prevention

| Excuse | Reality |
|--------|---------|
| "Should work now" | Run the verification |
| "I'm confident" | Confidence is not evidence |
| "Just this once" | No exceptions |
| "Linter passed" | Linter is not Unity compile/runtime proof |
| "Agent said success" | Verify independently |
| "I'm tired" | Exhaustion is an excuse |
| "Partial check is enough" | Partial proves nothing |
| "Different words so rule doesn't apply" | Spirit over letter |

## Key Patterns

**Unity tests:**

```text
GOOD: run EditMode/PlayMode tests -> see 0 failures -> "Relevant Unity tests pass"
BAD: "Should pass now" / "Looks correct"
```

**Regression tests:**

```text
GOOD: Write -> Run (pass) -> Revert fix -> Run (MUST FAIL) -> Restore -> Run (pass)
BAD: "I've written a regression test" without red-green verification
```

**Unity compile and console:**

```text
GOOD: refresh_unity -> read_console -> no new relevant errors -> "Unity compile/console check is clean"
BAD: "Files look correct" or "static check passed"
```

**Scene/prefab/runtime evidence:**

```text
GOOD: inspect changed prefab/scene -> run scene smoke -> report exact evidence
BAD: "Tests pass, so runtime wiring is complete"
```

**Agent delegation:**

```text
GOOD: Agent reports success -> check VCS diff -> verify Unity evidence -> report actual state
BAD: Trust agent report
```

## Why This Matters

From repeated failure patterns:

- User trust breaks when claims are not backed by evidence.
- Undefined or unwired Unity references can compile but fail at runtime.
- Missing requirements ship incomplete features.
- False completion causes redirect and rework.

## When To Apply

**Always before:**

- Any variation of success/completion claims
- Any expression of satisfaction
- Any positive statement about work state
- Committing, PR creation, task completion
- Moving to next task
- Delegating to agents

**Rule applies to:**

- Exact phrases
- Paraphrases and synonyms
- Implications of success
- Any communication suggesting completion/correctness

## The Bottom Line

No shortcuts for verification.

Run the command or MCPForUnity tool. Read the output. Then claim the result.
