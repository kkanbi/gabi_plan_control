# Memory.md — Gabi's AI Brain

> Claude는 매 세션 시작 시 이 파일을 먼저 읽습니다.
> 상세 전략은 링크된 원본 문서를 참조. 이 파일은 요약만.
> Last updated: 2026-03-22

---

## Identity & Context

- **이름**: Gabi (kkanbi)
- **현재 상태**: 육아휴직 중 (출산 2026.01)
- **현재 페이즈**: Phase 2 — 🌱 회복기 (2026.03, 종료: 2026.03.31)
- **가용 시간**: 하루 ~2시간 (육아 틈틈이)
- **핵심 원칙**: 번아웃 방지 최우선. 무리하지 않기. 한 번에 다 안 함.
- **최종 목표**: 복직 후 월 185만원 수동소득 (2027.07 기준)

---

## SNS 계정 구분

| 계정 | 성격 | 플랫폼 | 목적 |
|------|------|--------|------|
| @kkanddabia | 전문/개발/TA | Instagram + Threads | 외주 리드, 포트폴리오 |
| @creator_kkanbi | 감성/창작/육아툰 | Instagram + Threads | 웹툰/굿즈 장기 확장 |

---

## Active Projects (우선순위 순)

### 1. 웹소설 어시스턴트 (Novel_Assistant) — ACTIVE
- Repo: github.com/kkanbi/Novel_Assistant
- 상태: 진행 중
- 목적: 보조 프로젝트 → @creator_kkanbi 콘텐츠 연동

### 2. 인스타툰 자동생성기 — ACTIVE
- 상태: 진행 중 (웹소설과 병행)
- 목적: @creator_kkanbi Instagram 콘텐츠 자동화

### 3. 뽀모도로 RPG 앱 (Pomory) — ACTIVE
- Repo: github.com/kkanbi/Pomory
- 상태: 진행 중 (온보딩 화면 완료 2026-03-25)
- 완료: 스플래시, 온보딩 1/2/3 UI + 인터랙션
- 다음: 타이머 화면 구현
- 출시 목표: 2026.08
- 기술: Flutter + Hive (로컬)

### 4-6. 대기 중 프로젝트
- **타임블록 앱** → Phase 4 (2026.10 시작, 2027.02 출시 목표)
- **버튜버 외주** → Phase 3부터 블렌더 학습 (2026.04), 첫 수주 2027.04 목표
- **스톡이미지** → 버튜버 부산물 활용 (2026.08~)

---

## Revenue Timeline (요약)

| 시점 | 앱 | 버튜버 | 기타 | 합계 |
|------|-----|--------|------|------|
| 2026.08 | 30만 | - | ~1만 | ~31만 |
| 2027.02 | 50만 | 50만 | 5만 | 105만 |
| 2027.07 (복직) | 60만 | 80만 | 5만 | 145만 |
| 2028~ (안정화) | 60만 | 120만 | 5만 | **185만** |

> 상세 내용: [[50_Strategy/2026_ProjectTimeline]] | [[50_Strategy/freelancer_strategy_v2]]

---

## 페이즈별 로드맵 (현재 위치 표시)

| 페이즈 | 기간 | 테마 | 상태 |
|--------|------|------|------|
| Phase 1 | 2025.12 ~ 2026.02 | 출산직후 (휴식) | 완료 |
| **Phase 2** | **2026.03** | **🌱 회복기** | **← 현재** |
| Phase 3 | 2026.04 ~ 09 | 본격 개발기 | 예정 |
| Phase 4 | 2026.10 ~ 2027.01 | 집중 개발기 | 예정 |
| Phase 5 | 2027.02 ~ 06 | 출시·수익화 | 예정 |
| Phase 6 | 2027.07~ | 복직 후 | 예정 |

---

## Pending Actions

→ [[_system/Action_Tracker]] 참조

---

## Key Decisions

→ [[_system/Decision_Log]] 참조

---

## Session History

→ [[70_Sessions/]] 폴더 참조

---

## Vault 구조

| 폴더 | 역할 |
|------|------|
| 00_Inbox | 처리 전 임시 보관 |
| 10_Capture | 레퍼런스/스크랩 |
| 20_Learn | 학습 노트 |
| 25_Home | 집안 관리 (식재료, 소모품) |
| 30_Think | 아이디어/패턴 |
| 40_Projects | 프로젝트별 폴더 |
| 50_Strategy | 전략/타임라인 |
| 60_Journal | 자동 생성 작업일지 (generate_worklog.py) |
| 70_Sessions | Claude 세션 요약 |
| 80_Archive | 보관 |
| _system | Claude 시스템 파일 |
| _templates | Templater 템플릿 |

---

## Work Log 위치

- **자동 로그**: `60_Journal/YYYY-MM-DD.md` (generate_worklog.py 생성)
- **수동 메모**: 각 일지 파일의 `## 메모` 섹션
- **형식**: `[예정]` / `[실제]` / `[이유]`
- **원칙**: 한 줄이면 충분. 완벽하게 쓰려 하지 말 것.
