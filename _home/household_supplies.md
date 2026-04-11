# 🧴 소모품 / 생활용품 기록부

> 마지막 업데이트 : 2026-04-11
> 데이터 위치: `_home/supplies/` 폴더 — 항목 추가·수정은 개별 파일에서

---

## 📊 전체 현황

```dataview
TABLE WITHOUT ID
  length(filter(rows, (r) => r.상태 = "확정")) AS "✅ 확정",
  length(filter(rows, (r) => r.상태 = "테스트중")) AS "🔄 테스트중",
  length(filter(rows, (r) => r.상태 = "탈락")) AS "❌ 탈락"
FROM "_home/supplies"
GROUP BY true
```

---

## 🧻 위생용품

```dataview
TABLE WITHOUT ID
  이름 AS "아이템",
  출처 AS "산 곳",
  용량 AS "용량/수량",
  가격표시 AS "가격",
  재구매주기 AS "재구매 주기",
  메모 AS "메모"
FROM "_home/supplies"
WHERE 카테고리 = "위생용품" AND 상태 = "확정"
SORT 가격 ASC
```

---

## 🧹 청소용품

```dataview
TABLE WITHOUT ID
  이름 AS "아이템",
  출처 AS "산 곳",
  가격표시 AS "가격",
  재구매주기 AS "재구매 주기",
  메모 AS "메모"
FROM "_home/supplies"
WHERE 카테고리 = "청소용품" AND 상태 = "확정"
SORT 가격 ASC
```

---

## 🫧 세탁 / 주방세제

```dataview
TABLE WITHOUT ID
  이름 AS "아이템",
  출처 AS "산 곳",
  용량 AS "용량/수량",
  가격표시 AS "가격",
  재구매주기 AS "재구매 주기",
  메모 AS "메모"
FROM "_home/supplies"
WHERE 카테고리 = "세탁/주방세제" AND 상태 = "확정"
SORT 가격 ASC
```

---

## 🏠 기타 생활용품

```dataview
TABLE WITHOUT ID
  이름 AS "아이템",
  출처 AS "산 곳",
  가격표시 AS "가격",
  재구매주기 AS "재구매 주기",
  메모 AS "메모"
FROM "_home/supplies"
WHERE 카테고리 = "기타생활용품" AND 상태 = "확정"
SORT 가격 ASC
```

---

## 🔄 테스트 중

```dataview
TABLE WITHOUT ID
  이름 AS "아이템",
  카테고리 AS "카테고리",
  출처 AS "산 곳",
  가격표시 AS "가격",
  메모 AS "메모"
FROM "_home/supplies"
WHERE 상태 = "테스트중"
SORT 카테고리 ASC
```

---

## ❌ 탈락 목록

```dataview
TABLE WITHOUT ID
  이름 AS "아이템",
  카테고리 AS "카테고리",
  가격표시 AS "가격",
  메모 AS "탈락 이유"
FROM "_home/supplies"
WHERE 상태 = "탈락"
```

---

## 📝 새 항목 추가 방법

`_home/supplies/` 폴더에 아래 형식으로 파일 하나 생성하면 대시보드 자동 반영:

```yaml
---
이름: "[브랜드] 제품명"
카테고리: 위생용품|청소용품|세탁/주방세제|기타생활용품
출처: 네이버스토어
가격: 10000
가격표시: "10,000원"
용량: "-"
상태: 확정
재구매주기: "3개월"
메모: "메모"
구매일: "4.11"
---
```

---

## 📝 메모

- 네이버 브랜드관 링크는 직접 읽기 불가 → 스크린샷 or 상품명+가격으로 전달
