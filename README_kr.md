# Unity Superpowers

[English](README.md) | 한국어

Unity Superpowers는 AI 코딩 에이전트가 Unity 게임 개발을 안전하게 진행하도록 돕는 프로젝트 로컬 스킬팩입니다.

Current version: `0.1.0`.

기존 Superpowers의 작업 규율을 유지하되 Unity 프로젝트 생성, Unity Editor Bridge 모드, 씬, 프리팹, 직렬화 데이터, 패키지, 테스트, 디버깅, 리뷰, 검증에 맞게 특화합니다.

첫 단계는 `unity-init`입니다. 기능 구현 전에 Unity 프로젝트 상태를 점검하거나 준비해서 에이전트가 실제 프로젝트 경로, Git 상태, Unity Editor Bridge mode, active Editor target evidence, 검증 가능 범위를 알고 작업하게 합니다.

## 구성

```text
unity-superpowers/
  AGENTS.md
  CHANGELOG.md
  HowToInstall_AI.md
  README.md
  README_kr.md
  VERSION
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

일반적인 Unity 작업 흐름:

1. `unity-init`으로 프로젝트를 초기화하거나 점검합니다.
2. `brainstorming-unity`로 기능 방향과 요구사항을 정리합니다.
3. `writing-plans-unity`로 구현 계획을 작성합니다.
4. `subagent-driven-development-unity` 또는 `executing-plans-unity`로 계획을 실행합니다.
5. 필요하면 `test-driven-development-unity`, `systematic-debugging-unity`, 리뷰 스킬을 사용합니다.
6. `verification-before-completion-unity`로 완료 주장 전 검증합니다.
7. 반복 가능한 Unity 교훈은 `compound-unity`로 남깁니다.

## 개발 철학

Unity Superpowers는 기존 Superpowers의 규율을 유지합니다. 만들기 전에 이해하고, 가능하면 구현 전에 동작을 테스트하며, 수정 전에 root cause를 찾고, 작업을 격리하고, 일찍 리뷰하며, 완료 주장 전에 검증하고, 반복 가능한 교훈을 남깁니다.

Unity 버전에서 추가되는 핵심은 Unity 프로젝트 상태가 코드만이 아니라는 점입니다. Scene, prefab, `.meta` 파일, `ScriptableObject` asset, package manifest, asmdef, ProjectSettings, serialized field, layer, Animator parameter, physics setting, active Editor target은 모두 구현 표면입니다. Unity 에이전트는 이런 표면을 부수적인 정리 작업이 아니라 설계와 구현의 일부로 다뤄야 합니다.

아키텍처도 Unity에 맞춰 압력을 줍니다. 작은 `MonoBehaviour` 책임, GameObject composition, 좁은 capability interface, mode-specific behavior를 위한 `State`와 transition rule, policy/calculation 변형을 위한 `Strategy`, designer-tunable data를 위한 `ScriptableObject` asset을 선호합니다. Runtime 또는 Editor 기반 완료 주장은 Unity AI Assistant / Unity MCP 또는 MCPForUnity evidence와 tests, console/import 확인, scene smoke, prefab smoke, 필요 시 보조 manual observation이 필요합니다.

## 스킬 가이드

| Skill | Unity-specific focus | Superpowers 철학과의 연결 |
| --- | --- | --- |
| `using-superpowers-unity` | Unity 요청을 Unity 전용 스킬셋으로 라우팅하고 project readiness, project-local skills, `docs/solutions/`, Unity Editor Bridge target identity를 확인합니다. | "먼저 맞는 스킬을 사용한다"는 규율을 유지하되 Unity scene, prefab, Editor 작업에서 generic workflow로 후퇴하지 않게 합니다. |
| `unity-init` | Unity project structure, Git state, package state, Unity Editor Bridge setup, active Editor target, import/compile/console evidence, smoke-test readiness를 점검하거나 준비합니다. | Superpowers의 setup discipline을 Unity workspace readiness gate로 바꿉니다. |
| `brainstorming-unity` | Genre loop, input source, movement model, camera, scene/prefab boundary, component ownership, animation, physics, UI, data asset, package, verification surface를 질문합니다. | design-before-build를 유지하되 설계가 코드 동작만이 아니라 Unity architecture와 Editor/runtime wiring까지 포함하게 합니다. |
| `writing-plans-unity` | code, scene, prefab, asset, serialized field, package/settings, asmdef, test, Editor bridge 작업을 exact path와 expected evidence로 계획합니다. | fresh worker가 실행 가능한 계획을 유지하면서 Unity surface와 verification을 first-class task로 둡니다. |
| `using-git-worktrees-unity` | `.unity`, `.prefab`, `.asset`, `.meta`, packages, ProjectSettings 변경 전에 isolated workspace를 확인합니다. | work isolation 철학을 Unity generated file과 serialized asset merge risk에 맞춥니다. |
| `subagent-driven-development-unity` | runtime scripts, editor tooling, asmdefs/packages, tests, scene integration, prefab integration, data assets 같은 Unity ownership boundary로 작업을 나눕니다. | fresh subagent per task와 two-stage review를 유지하되 공유 Unity serialized state의 병렬 수정을 금지합니다. |
| `dispatching-parallel-agents-unity` | 독립된 Unity surface에서만 parallel work를 허용하고 shared scene, prefab, asset, manifest, `.meta`, ProjectSettings는 sequential하게 둡니다. | 속도를 유지하되 Unity serialization conflict로 인한 비용을 피합니다. |
| `executing-plans-unity` | active Editor bridge target, Unity surface, compile/console, tests, scene smoke, prefab smoke checkpoint로 승인된 계획을 실행합니다. | subagent를 쓰지 않거나 별도 실행 흐름을 택할 때도 plan execution discipline을 유지합니다. |
| `test-driven-development-unity` | pure C#, EditMode, PlayMode, condition-based wait, physics-aware wait, copy-safe Unity C# 예시로 TDD를 적용합니다. | red-green-refactor를 유지하면서 Unity test mode와 runtime timing을 반영합니다. |
| `systematic-debugging-unity` | console log, Editor state, package/import state, scene/prefab wiring, serialized reference, physics timing, active Editor bridge target mismatch를 따라 Unity bug를 추적합니다. | root-cause-first debugging을 유지하고 코드나 asset 수정 전에 Unity evidence path를 요구합니다. |
| `requesting-code-review-unity` | `MonoBehaviour` boundary, interface, state/strategy/data asset, serialized wiring, scene/prefab/asset changes, asmdefs, packages, evidence를 함께 리뷰합니다. | early review 철학을 유지하면서 Unity behavior risk를 review surface에 포함합니다. |
| `receiving-code-review-unity` | 피드백을 기술적으로 평가한 뒤 compile, console, tests, asset inspection, runtime evidence로 Unity-specific claim을 검증합니다. | review rigor를 유지하고 검증 없는 Unity wiring/architecture 변경을 막습니다. |
| `verification-before-completion-unity` | active bridge identity, `Application.dataPath` 또는 equivalent Unity-observed evidence, compile state, console state, EditMode/PlayMode tests, asset inspection, scene/prefab smoke evidence를 요구합니다. | Unity Editor/runtime claim에 evidence-before-assertions를 적용합니다. |
| `finishing-a-development-branch-unity` | fresh verification 이후 merge, PR, preserve, discard, cleanup 선택을 안내합니다. | branch completion을 명시적으로 유지하면서 Unity asset과 generated state를 보호합니다. |
| `compound-unity` | Editor bridge state, scene/prefab serialization, `.meta` GUID, package issue, test timing, architecture decision 같은 Unity blocker와 교훈을 저장합니다. | future agent가 Unity-specific workaround를 다시 발견하지 않도록 reusable lesson을 남깁니다. |
| `writing-skills-unity` | scene verification, prefab wiring, PlayMode timing, Unity Editor Bridge mode, oversized `MonoBehaviour` 위험을 포함한 pressure scenario로 Unity process skill을 작성/검증합니다. | skill-writing as TDD for process documentation을 유지하되 Unity-specific failure mode를 테스트에 넣습니다. |

## unity-init이 하는 일

`unity-init`은 구현 작업 전에 Unity workspace를 준비하거나 복구합니다. 프로젝트를 조용히 바꾸지 않습니다. 프로젝트 생성, Git 설정, 패키지 설치, Unity Editor Bridge 설정, Codex config 수정, remote 추가, Git LFS 설정 전에 변경 내용을 설명하고 승인을 받습니다.

점검 대상:

- Unity project markers: `Assets/`, `Packages/manifest.json`, `ProjectSettings/ProjectVersion.txt`
- Git repository와 remote 상태
- 설치된 Unity Editor와 사용 가능한 project template
- Unity Editor Bridge package/config/tool 표시 상태
- active Editor bridge target과 `Application.dataPath` 또는 equivalent Unity-observed identity evidence
- import, compile, console, EditMode, PlayMode 검증 가능 범위

현재 폴더가 Unity 프로젝트가 아니면 `unity-init`은 자동 생성과 수동 Unity Hub 생성 중 무엇을 원하는지 묻습니다. 자동 생성을 선택하면 프로젝트 형태를 결정하는 누락 정보를 질문합니다.

- project name
- Unity version 또는 설치된 Editor
- template: `2D`, `3D`, `URP`, `HDRP`, `Mobile` 등
- render pipeline: `Built-in`, `URP`, `HDRP`
- target platform

자동 생성 시 실제 폴더를 바꾸기 전에 선택한 template을 먼저 검증합니다. Unity project creation이 요청한 template을 제대로 적용하지 못하면 `.meta` 파일을 보존하고 blind overwrite를 피하면서 template `ProjectData~` fallback을 사용할 수 있습니다.

Unity 개발 harness 설정도 처리할 수 있습니다.

- 승인 후 Git 초기화
- Unity `.gitignore` 생성 또는 병합
- remote 추가 전 URL 질문
- 대용량 binary asset 프로젝트에 Git LFS 제안
- Editor integration 설치 또는 설정 전에 bridge mode 질문
- 승인 후 선택된 Unity Editor Bridge 설정
- bridge-specific setup은 아래 분기별 섹션으로 라우팅
- Unity tool을 신뢰하기 전에 active Unity Editor target 검증

최종 보고에는 project path, Unity version, creation path, template, render pipeline, target platform, manifest changes, Git state, `editor_bridge_mode`, `bridge_state`, `identity_evidence`, compile/console evidence, test readiness, selected bridge evidence gaps, next recommended skill이 포함되어야 합니다.

## Unity Editor Bridge

Unity Editor integration은 단일 필수 도구가 아니라 `Unity Editor Bridge`로 모델링합니다.

Bridge modes:

- `unity_ai_assistant`: Unity AI Assistant + Unity MCP Server.
- `mcpforunity`: external coding agent + MCPForUnity.

- `unity-init`은 Editor integration 설치 또는 설정 전에 사용할 bridge를 묻습니다.
- Editor 기반 완료 주장은 active Editor bridge evidence 또는 직접 관측한 Unity evidence가 필요합니다.
- Unity Editor 작업은 Unity AI Assistant / Unity MCP 또는 MCPForUnity 중 하나를 사용합니다.
- Scene, prefab, `.meta`, package, asmdef, ProjectSettings, serialized field 변경은 모두 주요 구현 표면입니다.
- 여러 Unity Editor가 열려 있으면 active Editor bridge target을 검증하기 전까지 routing risk로 취급합니다.

## Unity AI Assistant / Unity MCP 설정

공식 in-Editor AI workflow를 사용할 때 이 분기를 사용합니다.

Facts and constraints:

- Unity AI Assistant path는 open beta guide flow에서 Unity 6.3+가 필요할 수 있습니다.
- Unity AI는 Unity AI product FAQ 기준 일반적으로 Unity 6.0+, AI package, terms 승인, Unity Cloud project link가 필요합니다.
- `com.unity.ai.assistant`는 Unity support docs가 명시한 AI Assistant package입니다.
- Unity AI seat, subscription, trial 상태가 MCP 또는 AI Gateway connection에 영향을 줄 수 있습니다.
- Seat 변경 후 full Unity Editor restart가 필요할 수 있습니다.
- Agent는 사용자 승인 없이 subscription 구매, trial 시작, seat 할당, terms 승인, Cloud link 변경을 하면 안 됩니다.

Links: [Unity AI open beta guide](https://support.unity.com/hc/en-us/articles/48060149523476-Getting-started-with-Unity-AI-open-beta-user-guide), [Unity AI product page](https://unity.com/features/ai/), [Unity AI MCP connection error](https://support.unity.com/hc/en-us/articles/48958235901460-Unity-AI-MCP-Connection-Fails-Unity-AI-Gateway-connection-Error).

## MCPForUnity 설정

External coding agent와 MCPForUnity를 사용할 때 이 분기를 사용합니다. `unity-init`은 승인 후 Unity 프로젝트에 package를 추가하고, 가능하면 MCPForUnity client configurator를 실행하며, Codex가 MCPForUnity tools를 볼 수 있는지 확인합니다.

수동 설정:

1. Unity에서 `Window > Package Manager > + > Add package from git URL`을 엽니다.
2. `https://github.com/CoplayDev/unity-mcp.git?path=/MCPForUnity#main`을 입력합니다.
3. import 후 `Window > MCP for Unity`를 엽니다.
4. setup wizard 또는 client configurator로 감지된 AI client를 설정합니다.
5. MCP tools가 보이지 않으면 AI coding agent를 재시작하거나 refresh합니다.
6. Unity tools 사용 전 active MCPForUnity target과 `Application.dataPath`를 검증합니다.

공식 MCPForUnity 문서는 Unity 2021.3 LTS 이상, Python 3.10+와 `uv`, MCP client를 prerequisites로 안내합니다. Git URL, Asset Store, OpenUPM 설치 경로도 문서에 정리되어 있습니다.

Links: [MCP for Unity GitHub](https://github.com/CoplayDev/unity-mcp), [install docs](https://coplaydev.github.io/unity-mcp/getting-started/install), [OpenUPM package](https://openupm.com/packages/com.coplaydev.unity-mcp/).

## 설치

AI 코딩 에이전트에게 `HowToInstall_AI.md`를 읽고 사용하는 에이전트에 맞게 대상 프로젝트에 설치하라고 지시합니다.

Codex 기준 target shape:

```text
<UnityProject>/
  AGENTS.md
  .agents/
    skills/
      <all skill folders>
```

설치 후 project-local skills가 바로 발견되지 않으면 코딩 에이전트를 재시작하거나 refresh합니다.
