# Gabi Brain - Windows Task Scheduler 자동 등록
# PowerShell에서 관리자 권한으로 실행

$taskName = "GabiBrain_DailyWorkLog"
$scriptPath = "D:\2027_Git\gabi_plan_control\_system\scripts\run_worklog.bat"

# 기존 작업 삭제 (있으면)
Unregister-ScheduledTask -TaskName $taskName -Confirm:$false -ErrorAction SilentlyContinue

# 매일 밤 11시 50분에 실행
$trigger = New-ScheduledTaskTrigger -Daily -At "23:50"

# 실행 설정
$action = New-ScheduledTaskAction -Execute $scriptPath

# 옵션: 컴퓨터가 켜져 있을 때만, 배터리에서도 실행
$settings = New-ScheduledTaskSettingsSet `
    -AllowStartIfOnBatteries `
    -DontStopIfGoingOnBatteries `
    -StartWhenAvailable

# 등록
Register-ScheduledTask `
    -TaskName $taskName `
    -Trigger $trigger `
    -Action $action `
    -Settings $settings `
    -Description "Gabi Brain: Collect GitHub commits and generate daily work log"

Write-Host ""
Write-Host "Task Scheduler registered!" -ForegroundColor Green
Write-Host "  Name: $taskName" -ForegroundColor Cyan
Write-Host "  Time: Every day at 23:50" -ForegroundColor Cyan
Write-Host "  Script: $scriptPath" -ForegroundColor Cyan
Write-Host ""
Write-Host "To test now:" -ForegroundColor Yellow
Write-Host "  schtasks /run /tn $taskName" -ForegroundColor White
Write-Host ""
Write-Host "To check status:" -ForegroundColor Yellow
Write-Host "  schtasks /query /tn $taskName" -ForegroundColor White
