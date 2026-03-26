# Gabi Brain — 변경 이력 & 트러블슈팅

> 볼트 인프라, 스크립트, 시스템 설정 변경사항 기록
> 프로젝트별 변경사항은 각 레포의 `docs/CHANGELOG.md` 참고

---

## 업데이트 로그

| 날짜 | Phase | 내용 |
|------|-------|------|
| 2026-03-22 | Phase 2 | vault 초기 구축 — 폴더 구조, CLAUDE.md, Memory.md 등 시스템 파일 설계 |
| 2026-03-22 | Phase 2 | generate_worklog.py 작성 — GitHub 커밋 수집 → 옵시디언 일지 자동 생성 |
| 2026-03-22 | Phase 2 | Windows 작업 스케줄러(GabiBrain_DailyWorkLog) 등록 — 매일 23:50 자동 실행 |
| 2026-03-26 | Phase 2 | `.obsidian/workspace.json` git 추적 제거 (git rm --cached) |
| 2026-03-26 | Phase 2 | `run_worklog.bat` 에러 감지 추가 — Python 실패 시 ERROR 로그 기록 |

---

## 트러블슈팅

| 날짜 | 문제 | 해결 |
|------|------|------|
| 2026-03-26 | 옵시디언 열 때마다 push/pull 요청 뜸 | workspace.json이 .gitignore에 있었으나 이미 tracked 상태 → `git rm --cached` 후 커밋으로 해결 |
| 2026-03-26 | 2026-03-25 저널 파일 미생성 | run_worklog.bat이 Python 종료 코드 미확인 → 스크립트 실패해도 "Work log generated" 기록됨. %ERRORLEVEL% 체크 추가로 해결 |

---

## 🐛 문제 상세 기록 (Problem Log)

---

### [PROB-001] workspace.json git 추적 문제 (2026-03-26)

**문제 (Problem)**
옵시디언을 열 때마다 `.obsidian/workspace.json`이 변경되어 push/pull 알림 발생.
obsidian-git 자동 백업("vault backup" 커밋)에 workspace.json이 계속 포함됨.

**원인 (Cause)**
`.gitignore`에 `.obsidian/workspace.json`을 추가했지만, 이미 git이 추적 중인 파일은 .gitignore가 적용되지 않음.
git 인덱스에서 제거하는 별도 작업이 필요.

**해결 방법 (Solution)**
```bash
git rm --cached .obsidian/workspace.json
git commit -m "chore: stop tracking workspace.json (already in .gitignore)"
git push
```

---

### [PROB-002] run_worklog.bat 에러 미감지로 저널 미생성 (2026-03-26)

**문제 (Problem)**
2026-03-25 저널 파일(`60_Journal/2026-03-25.md`)이 생성되지 않았으나,
`worklog_history.log`에는 "Work log generated" 기록이 남아 있어 실패를 인지하지 못함.

**원인 (Cause)**
`run_worklog.bat`이 Python 스크립트 종료 코드를 확인하지 않음.
Python이 예외로 종료해도 그 다음 `echo` 명령이 실행되어 성공 로그가 기록됨.

**해결 방법 (Solution)**
`run_worklog.bat`에 `%ERRORLEVEL%` 체크 추가:
```bat
python "%VAULT_PATH%\_system\scripts\generate_worklog.py"

if %ERRORLEVEL% neq 0 (
    echo [%date% %time%] ERROR: Python script failed with exit code %ERRORLEVEL% >> log
    exit /b %ERRORLEVEL%
)

echo [%date% %time%] Work log generated >> log
```

**참고**
`run_worklog.bat`은 `.gitignore`에 포함되어 git에 커밋되지 않음 (PAT 토큰 포함).
로컬 파일 직접 수정 필요.

---
