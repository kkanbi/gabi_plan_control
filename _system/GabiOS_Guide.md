# GabiOS 사용 가이드

> 가비의 프로젝트 관리 + Claude 연동 시스템
> 마지막 업데이트: 2026-03-24

---

## GabiOS가 뭐야?

Claude Code + Obsidian vault를 연결해서
**"기억하고, 기록하고, 추적하는"** 개인 운영체제.

새 대화를 열어도 Claude가 이전 상황을 기억하고, 작업 기록이 자동으로 쌓이고,
프로젝트마다 일관된 문서 구조가 유지된다.

---

## 핵심 파일 구조

```
gabi_plan_control/
├── _system/
│   ├── CLAUDE.md             ← Claude 행동 규칙 (자동 읽힘)
│   ├── Memory.md             ← 현재 상태 스냅샷 (페이즈, 진행중 프젝)
│   ├── Action_Tracker.md     ← 할 일 목록 + 기한
│   ├── Decision_Log.md       ← 중요 결정 이력
│   ├── Master_Reference.md   ← 새 대화 시작용 전체 요약
│   ├── GabiOS_Guide.md       ← 이 파일
│   └── repo_configs/         ← 프로젝트별 CLAUDE.md 템플릿
│       ├── Novel_Assistant_CLAUDE.md
│       ├── instatoon-studio_CLAUDE.md
│       └── Pomory_CLAUDE.md
├── work_log.md               ← 날짜별 실제 작업 기록
├── 40_Projects/              ← 프로젝트 노트
├── 50_Strategy/              ← 전략 문서
├── 60_Journal/               ← 일별 메모
└── 70_Sessions/              ← 세션 요약 기록
```

---

## 자동으로 되는 것 vs 내가 해야 하는 것

### ✅ Claude가 자동으로 하는 것
| 상황 | 자동 동작 |
|------|----------|
| 세션 시작 | Memory.md, Action_Tracker.md 읽고 상황 파악 |
| 세션 시작 | 오늘 work_log 항목 없으면 "뭐 했어?" 질문 |
| Novel_Assistant 세션 시작 | 구글 드라이브 소설 폴더 체크, 수정 파일 있으면 알림 |
| 중요 결정 나왔을 때 | Decision_Log.md에 기록 제안 |
| 세션 끝 | 세션 요약 파일 생성 제안 |
| 작업 중 | 관련 기존 노트 먼저 검색 후 답변 |

### 🙋 내가 직접 해야 하는 것
| 상황 | 할 일 |
|------|-------|
| 새 대화 시작 | 그냥 열면 됨 (CLAUDE.md 자동 읽힘) |
| work_log 업데이트 | "오늘 work_log 업데이트해줘: [한 일]" |
| 세션 저장 | "오늘 세션 저장해줘" (안 하면 안 저장됨) |
| Memory.md 업데이트 | 페이즈 바뀌었을 때 "Memory 업데이트해줘" |

---

## 새 프로젝트 시작할 때 체크리스트

새 GitHub 레포 만들었을 때 아래를 순서대로:

### 1. vault에 프로젝트 노트 생성
```
40_Projects/[프로젝트명]/
├── overview.md     ← 목표, 기술 스택, 마감
└── notes.md        ← 작업 메모
```

### 2. 레포 루트 기본 구조 만들기
```
레포-루트/
├── README.md           ← 프로젝트 개요 + 진행 현황
├── CLAUDE.md           ← AI 컨텍스트 (아래 참고)
└── docs/
    ├── CHANGELOG.md    ← 변경이력 + 문제해결 기록
    ├── ARCHITECTURE.md ← 구조 설계
    └── SETUP.md        ← 개발환경 설정
```

### 3. 레포용 CLAUDE.md 만들기
- `_system/repo_configs/` 안에 있는 기존 파일 참고해서 작성
- 세션 시작 루틴, 기록 위치, 프로젝트 특이사항 포함
- 완성하면 레포 루트에 복사

### 4. _system/repo_configs/ 에 추가
- 위에서 만든 CLAUDE.md를 `[프로젝트명]_CLAUDE.md`로 저장
- 나중에 레포 날려도 설정 유지됨

### 5. Action_Tracker.md에 추가
- 새 프로젝트 마일스톤 기한 입력

### 6. Memory.md 업데이트
- 진행중 프로젝트 목록에 추가

---

## 자주 쓰는 명령어

```
# 작업 기록
"오늘 work_log 업데이트해줘: [한 일]"

# 현황 파악
"지금까지 어디쯤 왔는지 요약해줘"
"이번 주 work_log 보고 요약해줘"
"다음에 뭐 해야 할지 정리해줘"

# 세션 관리
"오늘 세션 저장해줘"
"Memory.md 업데이트해줘"

# 계획
"Action_Tracker 기한 지난 거 있어?"
"[프로젝트명] 다음 단계 뭐야?"
```

---

## 새 대화 시작하는 법

Claude Code를 **어느 레포에서 여느냐**에 따라 컨텍스트가 달라진다:

| 여는 위치 | 읽히는 CLAUDE.md | 컨텍스트 |
|-----------|----------------|--------|
| `gabi_plan_control/` | `_system/CLAUDE.md` | 전체 vault 관리 |
| `Novel_Assistant/` | 레포 루트 `CLAUDE.md` | 소설 어시스턴트 특화 |
| `instatoon-studio/` | 레포 루트 `CLAUDE.md` | 인스타툰 특화 |

**컨텍스트 빠르게 복구하고 싶을 때:**
> "_system/Master_Reference.md 읽어줘" 라고 하면 끝

---

## 현재 연결된 프로젝트

| 프로젝트 | 레포 | 특이사항 |
|---------|------|---------|
| 웹소설 어시스턴트 | kkanbi/Novel_Assistant | 구글 드라이브 소설 폴더 연동 |
| 인스타툰 자동생성기 | kkanbi/instatoon-studio | — |
| 뽀모도로 RPG (Flutter) | kkanbi/Pomory | 위 둘 완료 후 재개 |

---

## 문제 생기면

| 증상 | 해결 |
|------|------|
| Claude가 이전 상황 모름 | "_system/Master_Reference.md 읽어줘" |
| 구글 드라이브 체크 안 됨 | 드라이브 앱 동기화 확인, 경로 맞는지 확인 |
| work_log 찾기 어려움 | `gabi_plan_control/work_log.md` 직접 열기 |
| 세션 요약 없음 | 세션 끝에 "오늘 세션 저장해줘" 습관 들이기 |
