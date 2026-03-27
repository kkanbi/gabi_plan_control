@echo off
chcp 65001 > nul

:: ================================================
:: Gabi Brain - Daily Work Log Runner
:: Task Scheduler가 매일 23:50에 이 파일을 실행
:: GITHUB_PAT는 Windows 사용자 환경변수에서 읽음
:: ================================================

set SCRIPT_DIR=%~dp0
set VAULT_PATH=%SCRIPT_DIR%..\..
set PYTHON_SCRIPT=%SCRIPT_DIR%generate_worklog.py

:: GITHUB_PAT 확인
if "%GITHUB_PAT%"=="" (
    echo [ERROR] GITHUB_PAT 환경변수가 설정되지 않았습니다.
    echo 설정 방법: 시스템 속성 ^> 환경 변수 ^> 사용자 변수 ^> GITHUB_PAT 추가
    exit /b 1
)

:: Python 확인
where python > nul 2>&1
if %ERRORLEVEL% neq 0 (
    echo [ERROR] Python을 찾을 수 없습니다. PATH를 확인해주세요.
    exit /b 1
)

:: 실행
echo [INFO] %DATE% %TIME% - Work log 생성 시작
python "%PYTHON_SCRIPT%"

if %ERRORLEVEL% neq 0 (
    echo [ERROR] generate_worklog.py 실행 실패 (ERRORLEVEL=%ERRORLEVEL%)
    exit /b %ERRORLEVEL%
)

echo [INFO] Work log 생성 완료
exit /b 0
