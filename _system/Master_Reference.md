# 마스터 레퍼런스 — 2026-07-01

> 새 Claude 세션 시작 시 이 파일 한 장으로 전체 현황 파악 가능.
> 상세 내용은 링크된 원본 파일 참조.

---

## 1. 나는 누구인가

- **이름**: Gabi (kkanbi)
- **상태**: 육아휴직 중 (출산 2026.01), 밤 2시간 중심
- **현재 페이즈**: Phase 1 — 👶 베이비 트래커 코어 (2026.07)
- **원칙**: 번아웃 방지 최우선. 한 번에 다 안 함.
- **최종 목표**: 베이비 트래커 9월 출시, 복직 후 월 20~30만원 유지

---

## 파일 원칙

- 일정 원본: `50_Strategy/2026_ProjectTimeline.md` 하나만 수정
- HTML 타임라인: 시각화 전용
- 이 문서와 `Memory.md`는 참고용 요약

---

## 2. SNS 계정

| 계정 | 성격 | 목적 |
|------|------|------|
| @kkanddabia | 개발/TA | 출시 후기, 워킹맘 개발자 브랜딩 |
| @creator_kkanbi | 감성/창작 | 육아/창작 기록 |

---

## 3. 프로젝트 현황

| 순위 | 프로젝트 | 상태 | 레포 |
|------|---------|------|------|
| 1 | 베이비 트래커 | 🔄 2026.09 출시 목표 | - |
| 2 | 복직 준비 | 📅 2026.11 시작 | - |
| 3 | kkanddabia 콘텐츠 | 🌿 가볍게 유지 | - |
| 4 | 뽀모도로 RPG | ⏸️ 복직 후 재검토 | github.com/kkanbi/Pomory |
| 5 | 버튜버 외주 | ⏸️ 복직 후 탐색 | - |

---

## 4. 수익 타임라인 (요약)

| 시점 | 예상 월수입 |
|------|-----------|
| 2026.09 | 0~5만원 |
| 2026.10 | 5~10만원 |
| 2026.11 | 10~15만원 |
| 2026.12 | 15~20만원 |
| 2027.01 | 20만원 |
| 2027.02~ | 20~30만원 |

---

## 5. 로컬 경로 (Windows)

| 레포 | 경로 |
|------|------|
| vault (이 레포) | `D:\2027_Git\gabi_plan_control` |
| Novel_Assistant | `D:\2027_Novel_Assistant` |
| instatoon-studio | `D:\2027_Git_SideProject\SideProject_Plan\instatoon-studio` |
| Pomory | `D:\2027_Git\Pomory` |

---

## 6. 자동화 시스템

| 파일 | 역할 | 상태 |
|------|------|------|
| `_system/scripts/generate_worklog.py` | 60_Journal에 날짜별 작업일지 자동 생성 | 기본 정리 완료 |
| `_system/scripts/setup_all_repos.ps1` | 여러 레포 git 세팅 | 구축 완료 |
| `_system/scripts/setup_scheduler.ps1` | Windows 작업 스케줄러 등록 | 구축 완료 |
| obsidian-git 플러그인 | Vault 자동 백업 (커밋) | 활성 |
| Dataview 플러그인 | 대시보드 쿼리 | 활성 |

> PowerShell 스크립트 실행 전 1회 필요: `Set-ExecutionPolicy -Scope CurrentUser RemoteSigned`

---

## 7. 지금 당장 해야 할 것 (Active Actions)

| # | 할 일 | 데드라인 |
|---|-------|---------|
| 1 | 베이비 트래커 코어 입력 + Hive 저장 | 2026-07-31 |
| 2 | Riverpod 진행 상태 토글 + 헬멧 24h 로직 | 2026-07-31 |
| 3 | 8월 차트 + 알림 작업 준비 | 2026-08-01 |

→ 상세: `_system/Action_Tracker.md`

---

## 8. 자주 쓰는 Claude 명령어

```
"Memory.md 읽고 시작해줘"
"오늘 work_log 업데이트해줘: [한 일]"
"Action Tracker 확인해줘"
"지금까지 계획 대비 어디쯤 왔는지 분석해줘"
"이번 주 work_log 요약해줘"
```

---

*생성: 2026-03-23 세션 | 업데이트: 2026-07-01*
