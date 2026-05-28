# Unity Superpowers 0.0.1

[English](README.md) | 한국어

Unity Superpowers는 AI 코딩 에이전트가 Unity 게임 개발을 안전하게 진행하도록 돕는 프로젝트 로컬 스킬팩입니다.

기존 Superpowers의 작업 규율을 유지하되 Unity 프로젝트 생성, MCPForUnity, 씬, 프리팹, 직렬화 데이터, 패키지, 테스트, 디버깅, 리뷰, 검증에 맞게 특화합니다.

첫 단계는 `unity-init`입니다. 기능 구현 전에 Unity 프로젝트 상태를 점검하거나 준비해서 에이전트가 실제 프로젝트 경로, Git 상태, Unity Editor target, MCPForUnity 상태, 검증 가능 범위를 알고 작업하게 합니다.

## 구성

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

일반적인 Unity 작업 흐름:

1. `unity-init`으로 프로젝트를 초기화하거나 점검합니다.
2. `brainstorming-unity`로 기능 방향과 요구사항을 정리합니다.
3. `writing-plans-unity`로 구현 계획을 작성합니다.
4. `subagent-driven-development-unity` 또는 `executing-plans-unity`로 계획을 실행합니다.
5. 필요하면 `test-driven-development-unity`, `systematic-debugging-unity`, 리뷰 스킬을 사용합니다.
6. `verification-before-completion-unity`로 완료 주장 전 검증합니다.
7. 반복 가능한 Unity 교훈은 `compound-unity`로 남깁니다.

## unity-init이 하는 일

`unity-init`은 구현 작업 전에 Unity workspace를 준비하거나 복구합니다. 프로젝트를 조용히 바꾸지 않습니다. 프로젝트 생성, Git 설정, 패키지 설치, MCPForUnity 설정, Codex config 수정, remote 추가, Git LFS 설정 전에 변경 내용을 설명하고 승인을 받습니다.

점검 대상:

- Unity project markers: `Assets/`, `Packages/manifest.json`, `ProjectSettings/ProjectVersion.txt`
- Git repository와 remote 상태
- 설치된 Unity Editor와 사용 가능한 project template
- MCPForUnity package/config/tool 표시 상태
- active MCPForUnity target과 `Application.dataPath`
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
- 승인 후 Unity 프로젝트에 MCPForUnity package 추가
- 가능하면 MCPForUnity configurator로 Codex 설정
- Unity tool을 신뢰하기 전에 active Unity Editor target 검증

최종 보고에는 project path, Unity version, creation path, template, render pipeline, target platform, manifest changes, Git state, MCPForUnity state, active target evidence, compile/console evidence, test readiness, limitations, next recommended skill이 포함되어야 합니다.

## Unity 전제

- MCPForUnity가 Editor 제어 경로입니다.
- Editor 기반 완료 주장은 MCPForUnity 또는 직접 관측한 Unity 결과의 fresh evidence가 필요합니다.
- 파일 확인만으로 runtime proof를 주장하지 않습니다.
- Scene, prefab, `.meta`, package, asmdef, ProjectSettings, serialized field 변경은 모두 주요 구현 표면입니다.
- 여러 Unity Editor가 열려 있으면 active MCPForUnity target을 검증하기 전까지 routing risk로 취급합니다.

## MCPForUnity 설정

MCPForUnity는 이 스킬팩의 필수 Editor integration 경로입니다. `unity-init`은 승인 후 Unity 프로젝트에 package를 추가하고, 가능하면 MCPForUnity client configurator를 실행하며, Codex가 Unity MCP tools를 볼 수 있는지 확인합니다.

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
