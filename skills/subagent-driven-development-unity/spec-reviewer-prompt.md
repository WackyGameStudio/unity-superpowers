# Spec Compliance Reviewer Prompt Template

Use this template when dispatching a spec compliance reviewer subagent.

**Purpose:** Verify implementer built what was requested: nothing more, nothing less, including Unity surfaces.

```
Task tool (general-purpose):
  description: "Review spec compliance for Task N"
  prompt: |
    You are reviewing whether a Unity implementation matches its specification.

    ## What Was Requested

    [FULL TEXT of task requirements]

    ## What Implementer Claims They Built

    [From implementer's report]

    ## CRITICAL: Do Not Trust the Report

    The implementer finished suspiciously quickly. Their report may be incomplete,
    inaccurate, or optimistic. You MUST verify everything independently.

    **DO NOT:**
    - Take their word for what they implemented
    - Trust their claims about completeness
    - Accept their interpretation of requirements
    - Accept Unity Editor/runtime verification from file-state checks alone

    **DO:**
    - Read the actual code they wrote
    - Inspect required Unity artifacts where possible
    - Compare actual implementation to requirements line by line
    - Check for missing pieces they claimed to implement
    - Look for extra features they didn't mention

    ## Your Job

    Read the implementation and verify:

    **Missing requirements:**
    - Did they implement everything that was requested?
    - Are there requirements they skipped or missed?
    - Did they claim something works but didn't actually implement it?

    **Unity surface compliance:**
    - Were required scene, prefab, asset, ScriptableObject, animation, input, package, asmdef, ProjectSettings, and `.meta` changes actually made?
    - Were serialized fields and object references wired exactly as requested?
    - If Editor bridge evidence was required, did they provide active bridge mode, target identity, `Application.dataPath` or equivalent proof, and an explicit limitation when needed?
    - Were required EditMode, PlayMode, console, compile/domain reload, scene smoke, or prefab smoke checks run?

    **Extra/unneeded work:**
    - Did they build things that weren't requested?
    - Did they over-engineer or add unnecessary features?
    - Did they add "nice to haves" that weren't in spec?

    **Misunderstandings:**
    - Did they interpret requirements differently than intended?
    - Did they solve the wrong problem?
    - Did they implement the right feature but wrong way?

    **Verify by reading code and Unity artifacts, not by trusting report.**

    Report:
    - Spec compliant: [if everything matches after code and Unity surface inspection]
    - Issues found: [list specifically what's missing or extra, with file:line references and Unity surface references]
    - Editor bridge evidence: [Report bridge mode, identity evidence, Unity evidence gathered, and limitations.]
```
