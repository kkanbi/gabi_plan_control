# Memory.md — Gabi's AI Brain

> Claude는 매 세션 시작 시 이 파일을 먼저 읽습니다.
> 상세 전략과 프로젝트 추가는 `50_Strategy/2026_ProjectTimeline.md`를 기준으로 합니다. 이 파일은 요약만 유지합니다.
> Last updated: 2026-07-01

---

## Identity & Context

- **이름**: Gabi (kkanbi)
- **현재 상태**: 육아휴직 중 (출산 2026.01)
- **현재 페이즈**: Phase 1 — 👶 베이비 트래커 코어 (2026.07)
- **가용 시간**: 밤 2시간 실개발 + 낮잠 시간 짧은 학습
- **핵심 원칙**: 번아웃 방지 최우선. 무리하지 않기. 한 번에 다 안 함.
- **최종 목표**: 베이비 트래커 9월 출시 + 복직 후 월 20~30만원 유지

---

## 파일 원칙

- 일정 원본: `50_Strategy/2026_ProjectTimeline.md`
- 시각화: `50_Strategy/2026_ProjectTimeline.html`
- 이 파일은 요약 전용

---

## SNS 계정 구분

| 계정 | 성격 | 플랫폼 | 목적 |
|------|------|--------|------|
| @kkanddabia | 전문/개발/TA | Instagram + Threads | 출시 후기, 워킹맘 개발자 기록 |
| @creator_kkanbi | 감성/창작/육아툰 | Instagram + Threads | 육아/창작 기록 |

---

## Active Projects (우선순위 순)

### 1. 베이비 트래커 — ACTIVE
- 상태: 최우선 진행 중
- 목표: 2026.09 Play Store MVP 출시
- 기술: Flutter + Hive + Riverpod
- 2026.07 할 일: 기본 입력, 로컬 저장, 헬멧 24시간 로직

### 2. 복직 준비 — SCHEDULED
- 상태: 2026.11 시작 예정
- 목표: TA 실무 감각 복원 + 포트폴리오 정리
- 범위: 3ds Max, Maya, MaxScript, Python, Unreal, Blender 리깅

### 3. kkanddabia 콘텐츠 — LIGHT
- 상태: 출시 후기와 육아/복직 기록 위주
- 목표: 앱 출시 경험과 워킹맘 개발자 관점 정리

### 보류
- **뽀모도로 RPG** → 복직 후 여력 보고 재검토
- **버튜버 외주** → 복직 적응 후 시장 조사

---

## Revenue Timeline (요약)

| 시점 | 앱 수익 |
|------|----------|
| 2026.09 | 0~5만 |
| 2026.10 | 5~10만 |
| 2026.11 | 10~15만 |
| 2026.12 | 15~20만 |
| 2027.01 | 20만 |
| 2027.02~ | 20~30만 |

> 상세 내용: [[50_Strategy/2026_ProjectTimeline]]

---

## 페이즈별 로드맵 (현재 위치 표시)

| 페이즈 | 기간 | 테마 | 상태 |
|--------|------|------|------|
| 준비 | 2026.06 | 체력 회복 + 환경 세팅 | 완료 |
| **Phase 1** | **2026.07** | **👶 베이비 트래커 코어** | **← 현재** |
| Phase 2 | 2026.08 | 차트 + 알림 | 예정 |
| Phase 3 | 2026.09 | 테스트 + Play Store 출시 | 예정 |
| Phase 4 | 2026.10 | 안정화 + 위젯 | 예정 |
| 복직 준비 | 2026.11 ~ 2027.01 | TA 실무 감각 회복 | 예정 |
| 복직 후 | 2027.02~ | 앱 유지 + 외주 탐색 | 예정 |

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
