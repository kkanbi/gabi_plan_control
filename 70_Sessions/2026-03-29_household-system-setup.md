---
date: 2026-03-29
topic: 집사 시스템 구축 + 작업일지 자동화 수리
tags: [session, system, household, bugfix]
---

# 2026-03-29 세션 요약 — 집사 시스템 구축 + 자동화 수리

## 한 일

### 1. household 문서 정리 (기억 모드 첫 운용)
- 쇼핑 구매내역 이미지 → 신규 아이템 분류·추가 (Food 13개, Supplies 2개)
- 기존 문서에 있는 항목은 스킵, 신규만 추가하는 방식 확정

### 2. 레포 구조 개선
- `25_Home/` 폴더 신설 → household 문서 이동 (기존 50_Strategy는 전략 문서만)
- `gabi_brain/`, `work_log.md` 삭제
- 브랜치 작업 → main 직접 작업 방식으로 전환 (1인 레포 기준)

### 3. 작업일지 자동화 완전 수리
| 문제 | 원인 | 해결 |
|------|------|------|
| 저널 26일까지만 생성 | run_worklog.bat git 미커밋 | 이미 3.27 세션에서 수정됨 |
| python 명령 미인식 | Python PATH 미등록 | setx로 WindowsApps 경로 추가 |
| requests 없음 | 신규 Python 설치라 미설치 | pip install requests |
| Task Scheduler 조건 미흡 | Principal 미지정 등 | setup_scheduler.ps1 개선 후 재등록 |
| 누락 저널 27~29일 | 위 문제들로 미생성 | 스텁 생성 + 스크립트로 커밋 내역 갱신 |

### 4. 집사 시스템 운용 방식 확정
- `기억` + 이미지/링크 → 해당 문서에 정리
- `계획` → 현재 재고 기반 식단·일정 제안
- 알림 기능 → 차후 슬랙 연동 예정

## 다음 세션 참고
- 내일 `60_Journal/2026-03-30.md` 자동 생성 확인 (23:50 Task Scheduler)
- 실패 시: `schtasks /run /tn GabiBrain_DailyWorkLog` 로 수동 실행
- household_supplies.md 데이터 계속 쌓기 (청소용품·세탁세제 등 비어있음)
- 슬랙 알림 연동 검토 (소모품 재구매 주기 기반)
