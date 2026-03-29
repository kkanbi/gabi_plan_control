# GabiOS 사용 가이드

> 가비의 프로젝트 관리 + Claude 연동 시스템
> 마지막 업데이트: 2026-03-29

---

## GabiOS가 뭐야?

Claude Code + Obsidian vault를 연결해서
**"기억하고, 기록하고, 추적하는"** 개인 운영체제.

새 대화를 열어도 Claude가 이전 상황을 기억하고, 작업 기록이 자동으로 쌓이고,
프로젝트마다 일관된 문서 구조가 유지된다.

---

## 시스템 전체 흐름 (처음부터 이해하기)

> 개념이 헷갈릴 때 여기서 다시 읽기

### 한 줄 요약

**"코딩 기록을 자동으로 수집해서 일기 써주는 시스템"**

```
Gabi가 코딩한다
    ↓
GitHub에 커밋 (저장)
    ↓
매일 밤 자동으로 "오늘 뭐 했는지" 일지 작성
    ↓
Obsidian 볼트(이 레포)에 저장
```

---

### GitHub가 뭔지부터

GitHub = **코드 저장하는 구글 드라이브** 같은 것.

파일 저장할 때 "저장" 버튼 누르는 대신 **"커밋(commit)"** 이라고 함.
커밋할 때마다 "어떤 작업했는지 한 줄 메모"가 기록됨.

```
예: "온보딩 화면 3페이지 완성"  ← 이게 커밋 메시지
```

Gabi의 주요 레포:
- `Pomory` — 뽀모도로 앱
- `Novel_Assistant` — 웹소설 어시스턴트
- `instatoon-studio` — 인스타툰 자동생성기
- `gabi_plan_control` — 이 레포 (노트/일지 모음)

---

### 이 레포가 뭔지

Obsidian으로 열어서 보는 **마크다운 노트 모음**.

```
gabi_plan_control/
├── 60_Journal/    ← 자동으로 만들어지는 매일 작업일지
├── 50_Strategy/   ← 2026-2027 플랜 (스크립트가 이걸 읽음)
└── _system/
    └── scripts/
        └── generate_worklog.py  ← 핵심 자동화 스크립트
```

---

### 매일 밤 자동으로 일어나는 일

밤 11시 50분, 윈도우가 알아서 스크립트를 실행함.

```
윈도우 Task Scheduler (알람 앱 같은 것)
    ↓ 23:50 딱 되면 자동 실행
run_worklog.bat (배치파일 = 실행 버튼 같은 것)
    ↓
generate_worklog.py (파이썬 스크립트 = 진짜 일 하는 애)
```

---

### 스크립트가 하는 일 (핵심)

스크립트는 **3가지 질문에 답**을 만들어냄:

**① "이번 달 계획이 뭐였지?"**
```
50_Strategy/2026_ProjectTimeline.md 파일을 읽음
→ "3월엔 뽀모도로 MVP 개발하기로 했었네"
```

**② "오늘 실제로 뭐 했지?"**
```
GitHub API에 물어봄 (여기서 GitHub 토큰 필요)
→ "Pomory 레포에 커밋 3개 있네, Novel_Assistant엔 없네"
```

**③ "계획이랑 실제가 맞아?"**
```
① + ② 비교
→ "뽀모도로 작업함 ✅ / 웹소설은 오늘 작업 없음 ➖"
```

이걸 합쳐서 `60_Journal/YYYY-MM-DD.md` 파일로 자동 작성.

---

### 토큰이 뭔지

GitHub API에 "오늘 커밋 뭐야?" 하고 물어볼 때 **신분증이 필요함**.
그게 **GitHub Personal Access Token (PAT)**.

```
스크립트: "안녕 GitHub, kkanbi 오늘 커밋 뭐야?"
GitHub:  "신분증 보여줘"
스크립트: "이거" (토큰 제시)
GitHub:  "확인됨, 커밋 목록 줄게"
```

토큰은 **환경변수**라는 곳에 저장돼 있음.

> 환경변수 = 컴퓨터 전체에서 쓸 수 있는 비밀 메모장.
> 윈도우 설정에 `GITHUB_PAT=xxxx` 이렇게 저장해두면
> 어떤 프로그램도 꺼내 쓸 수 있음.

현재 사용 중인 토큰: GitHub → Settings → Fine-grained tokens → `gabi-worklog`

---

### git push는 왜 토큰 없이 됨?

"커밋 목록 읽어오기"랑 "파일 업로드하기"는 **완전 다른 경로**를 씀.

| 작업 | 인증 방식 | 어디서 설정? |
|------|----------|------------|
| GitHub API 호출 (커밋 읽기) | `GITHUB_PAT` 환경변수 | 윈도우 환경변수 |
| `git push` (파일 업로드) | Windows Credential Manager | 처음 GitHub 로그인 때 자동 저장 |

Windows Credential Manager = 크롬이 비밀번호 저장해주는 것과 같은 개념.
처음에 GitHub 로그인할 때 "저장할까요?" 눌렀으면 그게 남아있는 것.

---

### 전체 흐름 한눈에

```
[매일 밤 23:50]
      ↓
윈도우 알람 → run_worklog.bat 실행
      ↓
파이썬 스크립트 시작
      ↓
2026_ProjectTimeline.md 읽기  →  "이달 계획이 뭐야?"
      ↓
GitHub API 호출 (토큰 사용)   →  "오늘 커밋 뭐야?"
      ↓
계획 vs 실제 비교 후 일지 작성  →  "오늘 뭐 했는지 정리"
      ↓
git push (자격증명 관리자 사용)  →  "Obsidian 볼트에 저장"
      ↓
다음날 Obsidian 열면 60_Journal에 일지 생성돼 있음 ✅
```

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
│   └── scripts/
│       ├── generate_worklog.py  ← 일지 자동생성 스크립트
│       ├── run_worklog.bat      ← Task Scheduler 진입점
│       └── setup_scheduler.ps1 ← Task Scheduler 등록
├── 25_Home/                  ← 집안 관리 (식재료, 소모품)
├── 40_Projects/              ← 프로젝트 노트
├── 50_Strategy/              ← 전략 문서 (타임라인, 목표)
│   └── 2026_ProjectTimeline.md ← ⭐ 프로젝트 일정 원본 (스크립트가 읽음)
├── 60_Journal/               ← 날짜별 작업일지 (자동생성)
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

## 작업일지 자동화 워크플로우

매일 밤 23:50에 자동으로 돌아가는 흐름.

```
[Windows Task Scheduler]
       ↓ 23:50 알람
run_worklog.bat
       ↓ 파이썬 실행
generate_worklog.py
       ↓
  ┌─ 1. 타임라인 읽기 ────────────────────────────────────────┐
  │  50_Strategy/2026_ProjectTimeline.md                      │
  │  → 이번 달 프로젝트별 계획 추출                              │
  │  → 현재 Phase 파악                                         │
  └───────────────────────────────────────────────────────────┘
       ↓
  ┌─ 2. GitHub 커밋 수집 ─────────────────────────────────────┐
  │  GitHub API (GITHUB_PAT 사용)                             │
  │  → kkanbi 계정 전체 레포 스캔                               │
  │  → 오늘 날짜 커밋만 필터링                                   │
  └───────────────────────────────────────────────────────────┘
       ↓
  ┌─ 3. 계획과 대조 ──────────────────────────────────────────┐
  │  커밋 메시지·레포명 ↔ 프로젝트 키워드 매칭                    │
  │  → "오늘 뽀모도로 작업했어?" / "웹소설은?" 체크               │
  └───────────────────────────────────────────────────────────┘
       ↓
  ┌─ 4. 일지 파일 생성 ───────────────────────────────────────┐
  │  60_Journal/YYYY-MM-DD.md 자동 작성                        │
  │  → 커밋 내역 / 플랜 매칭 결과 / 요약                         │
  │  → 기존 메모 섹션은 보존                                     │
  └───────────────────────────────────────────────────────────┘
       ↓
  git pull → git add → git commit → git push
```

### 핵심 포인트
- **프로젝트 일정을 바꾸고 싶으면** `2026_ProjectTimeline.md`만 수정하면 됨 (스크립트 코드 건드릴 필요 없음)
- **새 프로젝트 추가** → 타임라인 YAML frontmatter에 name/repo/emoji/keywords 추가 + Mermaid gantt에 section 추가
- **수동 실행**: `python _system/scripts/generate_worklog.py 2026-03-27`

### 문제 생기면

| 증상 | 해결 |
|------|------|
| 일지 자동생성 안 됨 | Task Scheduler 확인: `schtasks /query /tn GabiBrain_DailyWorkLog` |
| python 명령 안 됨 | `%LOCALAPPDATA%\Microsoft\WindowsApps\python.exe` 로 직접 실행 |
| 커밋이 플랜에 매칭 안 됨 | 타임라인 해당 프로젝트 keywords에 레포명·키워드 추가 |
| 일지 내용 틀림 | 타임라인 Mermaid gantt 날짜 범위 수정 |

---

## 문제 생기면 (시스템 전반)

| 증상 | 해결 |
|------|------|
| Claude가 이전 상황 모름 | "_system/Master_Reference.md 읽어줘" |
| 세션 요약 없음 | 세션 끝에 "세션종료" 입력 |
