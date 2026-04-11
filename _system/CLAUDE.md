# 🤖 CLAUDE.md — 갑양 프로젝트 컨텍스트

> Claude Code 세션 시작 시 이 파일을 자동으로 읽습니다.  
> 매 세션 시작 전 아래 체크리스트를 따라주세요.

---

## ⚡ 세션 시작 루틴 (Claude에게)

새 세션이 시작되면 Claude는 다음 순서로 진행합니다:

1. **`_system/Memory.md` 읽기** — 현재 페이즈, 프로젝트 상태 파악
2. **`_system/Action_Tracker.md` 확인** — 기한 초과 항목 있으면 알림
3. **오늘 `60_Journal/YYYY-MM-DD.md` 확인** — 오늘 로그 있는지 확인
4. **오늘 날짜 항목이 없으면 묻기**:
   > "오늘 뭐 했어? work_log에 기록해줄게 (한 줄이면 됨)"

**세션 끝에:**
- 중요 결정 → `_system/Decision_Log.md`에 추가
- 새 할 일 → `_system/Action_Tracker.md`에 추가
- 실질적인 세션이었다면 → `70_Sessions/YYYY-MM-DD_topic.md` 생성

---

## 🔍 Search-First Rule

질문에 답하기 전, 항상 vault에서 관련 노트 먼저 확인:
- `40_Projects/` — 프로젝트 노트
- `_system/Decision_Log.md` — 과거 결정
- `50_Strategy/` — 전략 문서
- `70_Sessions/` — 이전 세션 요약

기존 분석 반복 금지. 기존 노트 위에 쌓을 것.

---

## 📬 Routing Rules (출력물 저장 위치)

| 출력 타입 | 저장 위치 |
|-----------|---------|
| 중요 결정 | `_system/Decision_Log.md` |
| 새 할 일 / 다음 액션 | `_system/Action_Tracker.md` |
| 세션 요약 | `70_Sessions/YYYY-MM-DD_topic.md` |
| 작업 메모/업데이트 | `60_Journal/YYYY-MM-DD.md` → `## 메모` 섹션 |
| 프로젝트 노트 | `40_Projects/[project]/` |
| 식재료·소모품 기록 | `_home/household_Food.md` 또는 `_home/household_supplies.md` |

---

## 🆕 새 프로젝트 시작 전 체크

새 프로젝트 레포를 만들면:

1. **`_system/repo_configs/`에 있는 해당 레포 CLAUDE.md 템플릿**을 레포 루트에 복사
2. **레포 루트에 `docs/` 폴더 생성** — `_templates/docs/` 안의 3개 파일 복사
3. **레포 루트에 `README.md` 생성** — `_templates/README_template.md` 복사 후 수정

### 레포별 CLAUDE.md 위치
| 레포 | 템플릿 위치 | 복사 대상 |
|------|------------|----------|
| Novel_Assistant | `_system/repo_configs/Novel_Assistant_CLAUDE.md` | `D:\2027_Novel_Assistant\CLAUDE.md` |
| instatoon-studio | `_system/repo_configs/instatoon-studio_CLAUDE.md` | `D:\2027_Git_SideProject\SideProject_Plan\instatoon-studio\CLAUDE.md` |
| Pomory | `_system/repo_configs/Pomory_CLAUDE.md` | `D:\2027_Git\Pomory\CLAUDE.md` |

이것만 있으면 어느 프로젝트에서 작업해도 모든 기록이 한 vault에 쌓임.

---

## 📄 각 레포 문서 규칙

각 레포는 다음 구조를 유지:
```
repo-root/
├── README.md          ← 프로젝트 개요 + 진행 현황
├── CLAUDE.md          ← AI 컨텍스트 (_system/repo_configs/ 참고)
└── docs/
    ├── CHANGELOG.md   ← 변경이력 + 문제해결기록 (Problem/Cause/Solution)
    ├── ARCHITECTURE.md← 구조 설계 문서
    └── SETUP.md       ← 개발환경 설정
```

**CHANGELOG 문제 해결 기록 형식 (필수)**:
```
### [PROB-XXX] 제목 (YYYY-MM-DD)
**문제 (Problem)**: 증상
**원인 (Cause)**: 근본 원인
**해결 방법 (Solution)**: 해결 단계
```

---

## 🎯 현재 진행 중인 프로젝트 (최신 순)

1. **웹소설 어시스턴트** — 진행 중 🔄
2. **인스타툰 자동생성기** — 진행 중 🔄
3. **뽀모도로 RPG 앱 (Flutter)** — 위 둘 완료 후 재개 ⏸️

---

## 📐 60_Journal/YYYY-MM-DD.md 작성 규칙

```
### YYYY-MM-DD
- [예정] 계획상 이 시기에 해야 했던 것 (없으면 생략)
- [실제] 실제로 한 것
- [이유] 계획과 다를 때만 한 줄로
```

**예시:**
```
### 2026-03-21
- [실제] 웹소설 어시스턴트 프롬프트 체인 구조 설계 완료
- [실제] 인스타툰 파이프라인 Gemini API 테스트

### 2026-03-22
- [예정] 뽀모도로 앱 Flutter 기초
- [실제] 웹소설 챕터 자동생성 로직 디버깅
- [이유] 어시스턴트 먼저 마무리하는 게 우선
```

---

## ⚠️ Claude에게 주의사항

- work_log는 **완벽하게 쓰려고 하지 말 것** — 한 줄이면 충분
- 계획 변경은 **잘못된 게 아님** — 그냥 [이유] 한 줄 추가하면 됨
- "오늘 뭐 했어?" 질문은 **세션당 1번만** (귀찮으면 역효과)
- 분석 요청 없이는 계획 vs 실제 비교 언급 안 해도 됨

---

## 🔍 자주 쓰는 명령어

```
"오늘 work_log 업데이트해줘: [한 일]"
"지금까지 계획 대비 어디쯤 왔는지 분석해줘"
"work_log 보고 이번 주 요약해줘"
"다음에 뭐 해야 할지 work_log 보고 정리해줘"
```
