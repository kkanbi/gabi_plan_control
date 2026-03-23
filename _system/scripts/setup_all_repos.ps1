# setup_all_repos.ps1
# 모든 프로젝트 레포에 CLAUDE.md + README + docs/ 구조 자동 설정
# 사용법: PowerShell에서 실행
#   cd D:\2027_Git\gabi_plan_control\_system\scripts
#   .\setup_all_repos.ps1

$vault = "D:\2027_Git\gabi_plan_control"
$templates = "$vault\_templates"
$configs = "$vault\_system\repo_configs"

$repos = @(
    @{
        path          = "D:\2027_Novel_Assistant"
        claude_config = "Novel_Assistant_CLAUDE.md"
        name          = "Novel_Assistant"
    },
    @{
        path          = "D:\2027_Git_SideProject\SideProject_Plan\instatoon-studio"
        claude_config = "instatoon-studio_CLAUDE.md"
        name          = "instatoon-studio"
    }
    # Pomory 경로 확인 후 아래 추가:
    # @{
    #     path          = "D:\[Pomory 경로]"
    #     claude_config = "Pomory_CLAUDE.md"
    #     name          = "Pomory"
    # }
)

foreach ($repo in $repos) {
    $path = $repo.path
    $name = $repo.name

    if (-not (Test-Path $path)) {
        Write-Host "SKIP: $name — 경로 없음 ($path)" -ForegroundColor Yellow
        continue
    }

    Write-Host "Setting up $name ..." -ForegroundColor Cyan

    # docs 폴더 생성
    New-Item -ItemType Directory -Force -Path "$path\docs" | Out-Null

    # docs 템플릿 복사 (이미 있으면 덮어쓰지 않음)
    $files = @(
        @{ src = "$templates\docs\CHANGELOG_template.md"; dest = "$path\docs\CHANGELOG.md" },
        @{ src = "$templates\docs\ARCHITECTURE_template.md"; dest = "$path\docs\ARCHITECTURE.md" },
        @{ src = "$templates\docs\SETUP_template.md"; dest = "$path\docs\SETUP.md" },
        @{ src = "$templates\README_template.md"; dest = "$path\README.md" },
        @{ src = "$configs\$($repo.claude_config)"; dest = "$path\CLAUDE.md" }
    )

    foreach ($f in $files) {
        if (Test-Path $f.dest) {
            Write-Host "  EXISTS (skip): $($f.dest | Split-Path -Leaf)" -ForegroundColor DarkGray
        } else {
            Copy-Item $f.src $f.dest -Force
            Write-Host "  CREATED: $($f.dest | Split-Path -Leaf)" -ForegroundColor Green
        }
    }

    Write-Host "Done: $name`n"
}

Write-Host "All repos set up!" -ForegroundColor Green
