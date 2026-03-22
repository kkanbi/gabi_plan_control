# 작업일지 자동화 설정 가이드

## Step 1: Python 설치 확인

CMD에서 확인:
```
python --version
pip install requests
```

---

## Step 2: GitHub Fine-Grained PAT 생성

1. https://github.com/settings/personal-access-tokens/new 접속
2. 설정:
   - Token name: `gabi-worklog`
   - Expiration: 90 days (나중에 갱신)
   - Repository access: **All repositories** (새 레포도 자동 추적)
   - Permissions:
     - **Contents**: Read-only (커밋 읽기)
     - **Metadata**: Read-only (레포 목록)
3. Generate token 클릭
4. 토큰 복사 (ghp_xxxx... 형태)

---

## Step 3: run_worklog.bat 수정

`_system\scripts\run_worklog.bat` 파일을 열어서:
```
set GITHUB_PAT=여기에_토큰_붙여넣기
```
이 부분에 복사한 토큰을 붙여넣기.

---

## Step 4: 테스트 실행

CMD에서:
```
cd D:\2027_Git\gabi_plan_control\_system\scripts
set GITHUB_PAT=ghp_여기에토큰
python generate_worklog.py
```

성공하면 `60_Journal\2026-03-22.md` 파일이 생성됩니다.

특정 날짜로 테스트:
```
python generate_worklog.py 2026-03-21
```

---

## Step 5: 매일 자동 실행 등록

PowerShell을 **관리자 권한**으로 열고:
```powershell
cd D:\2027_Git\gabi_plan_control\_system\scripts
.\setup_scheduler.ps1
```

매일 밤 11:50에 자동 실행됩니다.

---

## 수동 실행

언제든 직접 실행 가능:
```
D:\2027_Git\gabi_plan_control\_system\scripts\run_worklog.bat
```

---

## 새 레포 추가 시

별도 설정 필요 없음! 스크립트가 kkanbi 계정의 모든 레포를 자동 스캔합니다.
`gabi_plan_control` 레포만 자동 제외됩니다.

---

## 문제 해결

### "GITHUB_PAT 환경변수를 설정해주세요"
→ run_worklog.bat에서 토큰이 설정 안 됨. 토큰 확인.

### "Repo list API error: 401"
→ 토큰이 만료되었거나 잘못됨. 새로 발급.

### 커밋이 수집 안 됨
→ 해당 레포에 PAT 권한(Contents Read)이 있는지 확인.

### Git push 실패
→ CMD에서 `cd D:\2027_Git\gabi_plan_control && git push` 직접 테스트.
