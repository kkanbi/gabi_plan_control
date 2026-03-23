# CLAUDE.md — Pomory

> 이 파일을 Pomory 레포 루트의 `CLAUDE.md`에 복사해서 사용

---

## 세션 시작 루틴

새 세션 시작 시 Claude는 순서대로:

1. `D:\2027_Git\gabi_plan_control\_system\Memory.md` 읽기 — 현재 페이즈 파악
2. `D:\2027_Git\gabi_plan_control\_system\Action_Tracker.md` 확인 — 기한 초과 항목 알림
3. 이 레포의 `docs/CHANGELOG.md` 확인 — 최근 변경사항 파악

---

## 기록 위치

| 기록 타입 | 저장 위치 |
|-----------|---------|
| 작업 로그 | `D:\2027_Git\gabi_plan_control\work_log.md` |
| 중요 결정 | `D:\2027_Git\gabi_plan_control\_system\Decision_Log.md` |
| 새 할 일 | `D:\2027_Git\gabi_plan_control\_system\Action_Tracker.md` |
| 세션 요약 | `D:\2027_Git\gabi_plan_control\70_Sessions\YYYY-MM-DD_pomory.md` |
| 프로젝트 노트 | `D:\2027_Git\gabi_plan_control\40_Projects\앱개발\` |

---

## 이 레포 문서 관리 규칙

코드 변경 시 반드시 `docs/CHANGELOG.md` 업데이트:
- **기능 추가/변경**: `Added` / `Changed` 섹션에 추가
- **버그 수정**: `Fixed` 섹션 + 문제 해결 기록 섹션에 추가

### 문제 해결 기록 형식 (CHANGELOG.md 하단)
```
### [PROB-XXX] 문제 제목 (YYYY-MM-DD)
**문제 (Problem)**: 어떤 오류/증상이 발생했는가
**원인 (Cause)**: 왜 발생했는가
**해결 방법 (Solution)**: 어떻게 해결했는가
```

---

## 프로젝트 정보

- **GitHub**: https://github.com/kkanbi/Pomory
- **로컬 경로**: `D:\2027_Git\Pomory`
- **연결된 vault**: `D:\2027_Git\gabi_plan_control`
- **목표**: 뽀모도로 RPG 앱 (Flutter + Hive)
- **상태**: ⏸️ 일시정지 (2026-04 재개 예정)

---

## 주의사항

- Flutter 버전 고정 필수 (`fvm` 사용 권장)
- 큰 변경 전 `docs/ARCHITECTURE.md` 먼저 업데이트
