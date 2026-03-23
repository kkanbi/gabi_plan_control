# Claude Code CLI — Windows 설정 가이드

> 로컬에 클론된 모든 레포에서 Claude Code를 자유롭게 사용하기 위한 설정

---

## 1. 사전 요구사항

- [Node.js 18+](https://nodejs.org/) 설치 확인: `node -v`
- Anthropic API 키 준비

---

## 2. Claude Code CLI 설치

```powershell
npm install -g @anthropic-ai/claude-code
```

설치 확인:
```powershell
claude --version
```

---

## 3. API 키 설정

### 방법 A: 환경변수 영구 등록 (권장)
Windows 검색 → "환경 변수 편집" → 사용자 변수 → 새로 만들기:
- 변수명: `ANTHROPIC_API_KEY`
- 값: `sk-ant-...`

### 방법 B: PowerShell 세션마다 설정
```powershell
$env:ANTHROPIC_API_KEY="sk-ant-..."
```

---

## 4. 각 레포에서 사용하기

```powershell
# Novel_Assistant
cd D:\2027_Novel_Assistant
claude

# instatoon-studio
cd D:\2027_Git_SideProject\SideProject_Plan\instatoon-studio
claude

# Pomory
cd [Pomory 경로]
claude

# vault (gabi_plan_control)
cd D:\2027_Git\gabi_plan_control
claude
```

레포 루트에 `CLAUDE.md`가 있으면 Claude가 자동으로 읽고 컨텍스트 파악.

---

## 5. 각 레포에 CLAUDE.md 복사

`D:\2027_Git\gabi_plan_control\_system\repo_configs\` 폴더에 각 레포용 CLAUDE.md 있음.

```powershell
# Novel_Assistant
copy "D:\2027_Git\gabi_plan_control\_system\repo_configs\Novel_Assistant_CLAUDE.md" "D:\2027_Novel_Assistant\CLAUDE.md"

# instatoon-studio
copy "D:\2027_Git\gabi_plan_control\_system\repo_configs\instatoon-studio_CLAUDE.md" "D:\2027_Git_SideProject\SideProject_Plan\instatoon-studio\CLAUDE.md"
```

---

## 6. 각 레포에 docs/ 폴더 생성

```powershell
# Novel_Assistant 예시
$dest = "D:\2027_Novel_Assistant\docs"
New-Item -ItemType Directory -Force -Path $dest
copy "D:\2027_Git\gabi_plan_control\_templates\docs\CHANGELOG_template.md" "$dest\CHANGELOG.md"
copy "D:\2027_Git\gabi_plan_control\_templates\docs\ARCHITECTURE_template.md" "$dest\ARCHITECTURE.md"
copy "D:\2027_Git\gabi_plan_control\_templates\docs\SETUP_template.md" "$dest\SETUP.md"

# README
copy "D:\2027_Git\gabi_plan_control\_templates\README_template.md" "D:\2027_Novel_Assistant\README.md"
```

### 한 번에 모든 레포 설정하는 스크립트

```powershell
# setup_all_repos.ps1
$vault = "D:\2027_Git\gabi_plan_control"
$templates = "$vault\_templates"
$configs = "$vault\_system\repo_configs"

$repos = @(
    @{
        path = "D:\2027_Novel_Assistant"
        claude_config = "Novel_Assistant_CLAUDE.md"
    },
    @{
        path = "D:\2027_Git_SideProject\SideProject_Plan\instatoon-studio"
        claude_config = "instatoon-studio_CLAUDE.md"
    }
)

foreach ($repo in $repos) {
    $path = $repo.path
    Write-Host "Setting up $path ..."

    # docs 폴더 생성
    New-Item -ItemType Directory -Force -Path "$path\docs" | Out-Null

    # 템플릿 복사
    Copy-Item "$templates\docs\CHANGELOG_template.md" "$path\docs\CHANGELOG.md" -Force
    Copy-Item "$templates\docs\ARCHITECTURE_template.md" "$path\docs\ARCHITECTURE.md" -Force
    Copy-Item "$templates\docs\SETUP_template.md" "$path\docs\SETUP.md" -Force
    Copy-Item "$templates\README_template.md" "$path\README.md" -Force

    # CLAUDE.md 복사
    Copy-Item "$configs\$($repo.claude_config)" "$path\CLAUDE.md" -Force

    Write-Host "Done: $path"
}

Write-Host "All repos set up!"
```

저장 후 실행:
```powershell
cd D:\2027_Git\gabi_plan_control\_system\scripts
.\setup_all_repos.ps1
```

---

## 완료 후 확인

각 레포에서:
```
repo/
├── README.md      ✅
├── CLAUDE.md      ✅
└── docs/
    ├── CHANGELOG.md    ✅
    ├── ARCHITECTURE.md ✅
    └── SETUP.md        ✅
```
