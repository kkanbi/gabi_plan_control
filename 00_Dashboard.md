---
title: 대시보드
type: dashboard
---

# 🏠 Gabi's Second Brain

> 세컨 브레인 메인 허브 — 매일 자동 업데이트됨

---

## 📊 최근 작업일지 (Dataview)

```dataview
TABLE
  date AS "날짜",
  phase AS "페이즈",
  total_commits AS "커밋 수",
  plan_progress AS "계획 진행"
FROM "60_Journal"
WHERE type = "work-log"
SORT date DESC
LIMIT 14
```

---

## 🔥 이번 주 커밋 현황

```dataview
TABLE
  date AS "날짜",
  total_commits AS "커밋",
  plan_progress AS "진행률"
FROM "60_Journal"
WHERE type = "work-log" AND date >= date(today) - dur(7 days)
SORT date DESC
```

---

## 📁 활성 프로젝트

```dataview
TABLE
  file.mtime AS "최종 수정",
  status AS "상태"
FROM "40_Projects"
WHERE type = "project"
SORT file.mtime DESC
```

---

## 🤖 AI Brain

| 문서 | 역할 |
|------|------|
| [[_system/Memory\|🧠 Memory]] | 세션 시작 필독 — 현재 상태 총정리 |
| [[_system/Action_Tracker\|✅ Action Tracker]] | 진행 중 할 일 + 데드라인 |
| [[_system/Decision_Log\|🗂️ Decision Log]] | 결정 이력 (왜 그렇게 했는지) |

## 📝 최근 세션

```dataview
LIST
FROM "70_Sessions"
SORT file.ctime DESC
LIMIT 5
```

---

## 🗓️ 전략 & 플랜

| 문서 | 설명 |
|------|------|
| [[50_Strategy/2026_ProjectTimeline\|📊 프로젝트 타임라인]] | Gantt 차트 + 수익 계획 (Mermaid) |
| [[50_Strategy/2026_ProjectTimeline\|🎨 HTML 원본 타임라인]] | 색상/애니메이션 포함 HTML 뷰 |
| [[50_Strategy/2026_Goal\|🎯 2026 라이프 아키텍처]] | 만다라트 + 분기별 체크리스트 (HTML) |
| [[50_Strategy/freelancer_strategy_v2\|📝 프리랜서 전략 v2]] | 마스터 전략 문서 |

---

## 📈 월별 커밋 통계

```dataview
TABLE
  length(rows) AS "작업일 수",
  sum(rows.total_commits) AS "총 커밋"
FROM "60_Journal"
WHERE type = "work-log"
GROUP BY dateformat(date, "yyyy-MM") AS "월"
SORT rows.date DESC
LIMIT 6
```

---

## 🗃️ 최근 학습 노트

```dataview
LIST
FROM "20_Learn"
SORT file.mtime DESC
LIMIT 5
```

---

## 💡 최근 아이디어

```dataview
LIST
FROM "30_Think"
SORT file.mtime DESC
LIMIT 5
```

---

## 📥 받은 편지함 (처리 대기)

```dataview
LIST
FROM "00_Inbox"
SORT file.ctime DESC
```

---

*자동 생성: `generate_worklog.py` | 플러그인: Dataview, obsidian-git*
