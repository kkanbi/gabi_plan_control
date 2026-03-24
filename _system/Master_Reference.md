# 마스터 레퍼런스 — 2026-03-23

> 새 Claude 세션 시작 시 이 파일 한 장으로 전체 현황 파악 가능.
> 상세 내용은 링크된 원본 파일 참조.

---

## 1. 나는 누구인가

- **이름**: Gabi (kkanbi)
- **상태**: 육아휴직 중 (출산 2026.01), 하루 ~2시간 가용
- **현재 페이즈**: Phase 2 — 🌱 회복기 (2026.03, 마감 2026.03.31)
- **원칙**: 번아웃 방지 최우선. 한 번에 다 안 함.
- **최종 목표**: 복직 후 월 185만원 수동소득 (2027.07 기준)

---

## 2. SNS 계정

| 계정 | 성격 | 목적 |
|------|------|------|
| @kkanddabia | 개발/TA | 외주 리드, 포트폴리오 |
| @creator_kkanbi | 감성/창작 | 웹툰/굿즈 콘텐츠 |

---

## 3. 프로젝트 현황

| 순위 | 프로젝트 | 상태 | 레포 |
|------|---------|------|------|
| 1 | 웹소설 어시스턴트 (Novel_Assistant) | 🔄 진행 중 | github.com/kkanbi/Novel_Assistant |
| 2 | 인스타툰 자동생성기 (instatoon-studio) | 🔄 진행 중 | - |
| 3 | 뽀모도로 RPG 앱 (Pomory) | ⏸️ Phase 3 재개 | github.com/kkanbi/Pomory |
| 4 | 타임블록 앱 | 📅 Phase 4 (2026.10) | - |
| 5 | 버튜버 외주 | 📅 Phase 3 학습 시작 | - |

---

## 4. 수익 타임라인 (요약)

| 시점 | 예상 월수입 |
|------|-----------|
| 2026.08 | ~31만원 |
| 2027.02 | ~105만원 |
| 2027.07 (복직) | ~145만원 |
| 2028+ | **185만원** |

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
| `_system/scripts/generate_worklog.py` | 60_Journal에 날짜별 작업일지 자동 생성 | 구축 완료 |
| `_system/scripts/setup_all_repos.ps1` | 4개 레포 동시 git 세팅 | 구축 완료 |
| `_system/scripts/setup_scheduler.ps1` | Windows 작업 스케줄러 등록 | 구축 완료 |
| obsidian-git 플러그인 | Vault 자동 백업 (커밋) | 활성 |
| Dataview 플러그인 | 대시보드 쿼리 | 활성 |

> PowerShell 스크립트 실행 전 1회 필요: `Set-ExecutionPolicy -Scope CurrentUser RemoteSigned`

---

## 7. Claude 작업 환경

### 현재 쓰는 방식
- **Claude Code CLI** — 터미널에서 `claude` 실행
- **작업 디렉토리**: 각 레포 폴더에서 실행

### 더 편한 방식 (도입 가능)
- **VS Code 통합 터미널**: 프로젝트 폴더 워크스페이스로 저장 → 터미널에서 바로 `claude`
- **VS Code Claude Code 확장**: 사이드바에서 바로 대화 (Extension 마켓플레이스 "Claude Code" 검색)
- **Git Worktree**: 여러 브랜치를 동시에 다른 폴더에 체크아웃 → 병렬 작업 가능

### Git Worktree 기본 명령어
```bash
git worktree add ../gabi_main main      # main 브랜치를 다른 폴더에 열기
git worktree list                        # 현재 worktree 목록
git worktree remove ../gabi_main        # 제거
```

---

## 8. 이 Vault 구조

→ `_system/Memory.md` 참조 (Vault 구조 표 포함)

---

## 9. 각 레포 표준 구조

```
repo-root/
├── README.md           ← 개요 + 진행 현황
├── CLAUDE.md           ← AI 컨텍스트 (_system/repo_configs/ 참고)
└── docs/
    ├── CHANGELOG.md    ← 변경이력 + 문제해결 (Problem/Cause/Solution)
    ├── ARCHITECTURE.md ← 구조 설계
    └── SETUP.md        ← 개발환경 설정
```

**레포별 CLAUDE.md 템플릿 위치**: `_system/repo_configs/`

---

## 10. work_log 작성 규칙

→ `_system/CLAUDE.md` 참조 (작성 형식 및 원칙 포함)

---

## 11. 지금 당장 해야 할 것 (Active Actions)

| # | 할 일 | 데드라인 |
|---|-------|---------|
| 1 | 웹소설 어시스턴트 프롬프트 체인 완성 | 2026-03-31 |
| 2 | 인스타툰 자동생성기 파이프라인 테스트 | 2026-03-31 |
| 3 | Phase 3 시작 준비 (뽀모도로 재개 계획) | 2026-04-01 |

→ 상세: `_system/Action_Tracker.md`

---

## 12. 자주 쓰는 Claude 명령어

```
"Memory.md 읽고 시작해줘"
"오늘 work_log 업데이트해줘: [한 일]"
"Action Tracker 확인해줘"
"지금까지 계획 대비 어디쯤 왔는지 분석해줘"
"이번 주 work_log 요약해줘"
```

---

*생성: 2026-03-23 세션 | 다음 개선 예정: 새 대화에서*
