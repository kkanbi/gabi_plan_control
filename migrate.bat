@echo off
chcp 65001 >nul
echo ============================================
echo   Gabi Brain 폴더 구조 마이그레이션
echo ============================================
echo.

set "VAULT=D:\2027_Git\gabi_plan_control"

:: 1) 현재 폴더 존재 확인
if not exist "%VAULT%" (
    echo [ERROR] %VAULT% 폴더를 찾을 수 없습니다.
    pause
    exit /b 1
)

echo [INFO] 작업 대상: %VAULT%
echo.

:: 2) 새 폴더 생성 (없는 것만)
echo [1/5] 새 폴더 생성 중...

if not exist "%VAULT%\20_Learn\courses" mkdir "%VAULT%\20_Learn\courses"
if not exist "%VAULT%\20_Learn\books" mkdir "%VAULT%\20_Learn\books"
if not exist "%VAULT%\30_Think\ideas" mkdir "%VAULT%\30_Think\ideas"
if not exist "%VAULT%\30_Think\patterns" mkdir "%VAULT%\30_Think\patterns"
if not exist "%VAULT%\60_Journal" mkdir "%VAULT%\60_Journal"
if not exist "%VAULT%\80_Archive" mkdir "%VAULT%\80_Archive"
if not exist "%VAULT%\_templates" mkdir "%VAULT%\_templates"
if not exist "%VAULT%\_system\scripts" mkdir "%VAULT%\_system\scripts"

echo    - 60_Journal, 80_Archive, _templates, _system 생성 완료
echo.

:: 3) 기존 폴더 이름 변경 (20_Tutorial → 20_Learn, 30_Notes → 30_Think)
echo [2/5] 폴더 리네임 중...

:: 20_Tutorial → 20_Learn (기존 파일 이동)
if exist "%VAULT%\20_Tutorial" (
    echo    - 20_Tutorial 내용을 20_Learn\courses 로 이동
    for %%f in ("%VAULT%\20_Tutorial\*") do (
        move "%%f" "%VAULT%\20_Learn\courses\" >nul 2>&1
    )
    :: 하위 폴더도 이동
    for /d %%d in ("%VAULT%\20_Tutorial\*") do (
        move "%%d" "%VAULT%\20_Learn\courses\" >nul 2>&1
    )
    rmdir "%VAULT%\20_Tutorial" 2>nul
    echo    - 20_Tutorial 제거 완료
)

:: 30_Notes → 30_Think (기존 파일 이동)
if exist "%VAULT%\30_Notes" (
    echo    - 30_Notes 내용을 30_Think\ideas 로 이동
    for %%f in ("%VAULT%\30_Notes\*") do (
        move "%%f" "%VAULT%\30_Think\ideas\" >nul 2>&1
    )
    for /d %%d in ("%VAULT%\30_Notes\*") do (
        move "%%d" "%VAULT%\30_Think\ideas\" >nul 2>&1
    )
    rmdir "%VAULT%\30_Notes" 2>nul
    echo    - 30_Notes 제거 완료
)

echo.

:: 4) 시스템 파일 이동
echo [3/5] 시스템 파일 정리 중...

if exist "%VAULT%\CLAUDE.md" (
    move "%VAULT%\CLAUDE.md" "%VAULT%\_system\CLAUDE.md" >nul
    echo    - CLAUDE.md → _system/ 이동 완료
)

if exist "%VAULT%\work_log.md" (
    move "%VAULT%\work_log.md" "%VAULT%\80_Archive\work_log_old.md" >nul
    echo    - work_log.md → 80_Archive/ 이동 완료 (이제 60_Journal에서 날짜별 생성)
)

echo.

:: 5) 새 파일 복사 안내
echo [4/5] 다음 파일들을 수동으로 복사해주세요:
echo.
echo    README.md          → %VAULT%\README.md
echo    _templates\*.md    → %VAULT%\_templates\
echo.
echo    (이 파일들은 migrate.bat과 같은 폴더에 있습니다)
echo.

:: 6) 결과 확인
echo [5/5] 최종 폴더 구조:
echo.
dir /b /ad "%VAULT%"
echo.

echo ============================================
echo   마이그레이션 완료!
echo ============================================
echo.
echo   다음 단계:
echo   1. README.md와 _templates 폴더를 볼트에 복사
echo   2. 옵시디언에서 볼트 다시 열기
echo   3. 옵시디언 설정:
echo      - 첨부파일 위치 → 90_Attachments
echo      - Templater 폴더 → _templates
echo   4. (선택) GitHub 레포 이름을 gabi_brain으로 변경
echo.
pause
