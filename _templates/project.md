---
type: project
status: 진행중
tags: []
started: <% tp.date.now("YYYY-MM-DD") %>
deadline: 
---

# <% tp.file.title %>

## 목표


## 관련 레퍼런스
<!-- 10_Capture 노트 링크 -->
- 

## 관련 학습

```dataview
TABLE course AS "강의/자료", tags AS "태그", started AS "날짜"
FROM "20_Learn"
WHERE contains(프로젝트, "<% tp.file.title %>")
SORT started DESC
```

## 관련 아이디어
<!-- 30_Think 노트 링크 -->
- 

## 진행 기록
### <% tp.date.now("YYYY-MM-DD") %>
- 
