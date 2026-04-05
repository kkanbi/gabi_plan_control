# Action Tracker

> 매 세션 시작 시 Claude가 이 파일을 확인합니다.
> 완료 항목 → ## Done 섹션으로 이동 (최근 30일 유지)
> 활성 항목은 10개 이하로 유지. 나머지는 Backlog으로.

---

## Active Actions

| # | 할 일 | 프로젝트 | 데드라인 | 페이즈 | 추가일 |
|---|-------|---------|---------|-------|-------|
| 1 | 타이머 화면 UI 구현 | Pomory | 2026-04-15 | Ph3 | 2026-03-25 |
| 2 | 육아타이쿤 기획 문서 초안 작성 | 육아타이쿤 | - | Ph3 | 2026-04-05 |
| 3 | 웹소설 하루 5천자 (일일 목표) | 웹소설 | 매일 | Ph3 | 2026-04-05 |

---

## Backlog (데드라인 없음)

| 할 일 | 프로젝트 | 메모 |
|-------|---------|------|
| 블렌더 학습 시작 | 버튜버외주 | Phase 3 시작 시 (2026.04) |
| Claude Desktop MCP 설정 | System | Windows에서 직접: claude_desktop_config.json 편집 |
| Claude Desktop Custom Instruction 입력 | System | 설정 > Custom Instructions |
| AI Brain 시스템 3주 후 효과 평가 | System | 2026-04-15 재검토 |

---

## Done (최근 30일)

| 할 일 | 프로젝트 | 완료일 |
|-------|---------|-------|
| 웹소설 어시스턴트 기능 개발 완성 | Novel_Assistant | 2026-04-05 |
| 인스타툰 자동생성기 파이프라인 테스트 (사용 안 하기로 결정) | InstatoonGen | 2026-04-05 |
| Vault 구조 셋업 | System | 2026-03-22 |
| AI Brain 시스템 도입 (Memory.md + 라우팅 규칙) | System | 2026-03-22 |
| Pomory 온보딩 화면 완성 (스플래시 + 3페이지) | Pomory | 2026-03-25 |
| workspace.json git 추적 제거 + bat 에러 감지 추가 | System | 2026-03-26 |
| run_worklog.bat 생성 + GITHUB_PAT 환경변수 설정 완료 | System | 2026-03-27 |
| _system/CHANGELOG.md 신규 생성 | System | 2026-03-26 |

---

## 사용법

- **Claude**: 세션 끝에 새 할 일 발견 시 Active 테이블에 행 추가
- **완료 표시**: Active → Done으로 행 이동, 완료일 기입
- **기한 초과**: 데드라인 < 오늘 항목은 세션 시작 시 Claude가 알림
- **10개 초과**: 새 항목 추가 전 기존 항목 Backlog으로 이동 검토
