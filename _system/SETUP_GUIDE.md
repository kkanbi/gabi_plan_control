# 작업일지 자동화 설정 가이드

## 현재 기준

- 일정 원본: `50_Strategy/2026_ProjectTimeline.md`
- 시각화: `50_Strategy/2026_ProjectTimeline.html`
- 자동 일지 생성: `_system/scripts/generate_worklog.py`
- 기본 동작: 저널 생성만 수행
- Git 동기화: `WORKLOG_GIT_SYNC=1`일 때만 수행

---

## 1. Python 확인

```
python --version
pip install requests
```

---

## 2. GitHub PAT 설정

- 환경변수 이름: `GITHUB_PAT`
- 권한: repo 메타데이터 읽기 + 커밋 읽기

Windows 사용자 환경변수에 등록합니다.

---

## 3. 수동 테스트

```
cd D:\2027_Git\gabi_plan_control\_system\scripts
python generate_worklog.py
```

특정 날짜 테스트:

```
python generate_worklog.py 2026-07-01
```

---

## 4. Git 동기화가 필요할 때만

```
set WORKLOG_GIT_SYNC=1
python generate_worklog.py
```

이제는 기본값으로 저장소 전체를 자동 커밋하지 않습니다.

---

## 5. 작업 스케줄러 등록

```powershell
cd D:\2027_Git\gabi_plan_control\_system\scripts
.\setup_scheduler.ps1
```

---

## 새 프로젝트 추가 규칙

새 레포를 만들었을 때 자동화에 반영하려면:

1. `50_Strategy/2026_ProjectTimeline.md`의 `projects:`에 추가
2. 같은 파일 mermaid gantt에 일정 추가
3. 필요하면 `40_Projects/` 안에 상태에 맞는 폴더 생성

HTML은 보기 전용이라 급하지 않으면 나중에 수정해도 됩니다.
