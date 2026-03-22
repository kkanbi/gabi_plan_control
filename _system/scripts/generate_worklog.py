#!/usr/bin/env python3
"""
Gabi Brain - Daily Work Log Generator
=====================================
매일 밤 실행: GitHub 커밋 수집 → 마스터 플랜 매칭 → 옵시디언 일지 자동 생성

사용법:
  python generate_worklog.py              # 오늘 날짜 기준
  python generate_worklog.py 2026-03-21   # 특정 날짜 지정
"""

import os
import re
import sys
import json
import subprocess
from datetime import datetime, timezone, timedelta
from pathlib import Path
from html.parser import HTMLParser

try:
    import requests
except ImportError:
    print("[ERROR] requests 라이브러리가 필요합니다: pip install requests")
    sys.exit(1)


# ═══════════════════════════════════════════════════════════════
# 설정
# ═══════════════════════════════════════════════════════════════

GITHUB_TOKEN = os.environ.get("GITHUB_PAT", "")
GITHUB_USERNAME = "kkanbi"

# 작업일지 레포 (이 레포는 커밋 수집에서 제외)
EXCLUDE_REPOS = ["gabi_plan_control"]

# 옵시디언 볼트 경로 (Windows)
VAULT_PATH = Path(os.environ.get(
    "VAULT_PATH",
    r"D:\2027_Git\gabi_plan_control"
))

# 일지 저장 폴더
JOURNAL_DIR = VAULT_PATH / "60_Journal"

# 마스터 플랜 HTML 경로
MASTER_PLAN_PATH = VAULT_PATH / "50_Strategy" / "2026_ProjectTimeline.html"

KST = timezone(timedelta(hours=9))


# ═══════════════════════════════════════════════════════════════
# 1. GitHub API: 모든 레포에서 커밋 수집
# ═══════════════════════════════════════════════════════════════

def get_all_repos():
    """kkanbi 계정의 모든 레포 목록 (exclude 제외)"""
    headers = {
        "Accept": "application/vnd.github+json",
        "Authorization": f"Bearer {GITHUB_TOKEN}",
        "X-GitHub-Api-Version": "2022-11-28",
    }
    repos = []
    page = 1
    while True:
        url = f"https://api.github.com/user/repos?per_page=100&page={page}&affiliation=owner"
        r = requests.get(url, headers=headers, timeout=30)
        if r.status_code != 200:
            print(f"[WARN] Repo list API error: {r.status_code}")
            break
        data = r.json()
        if not data:
            break
        for repo in data:
            name = repo["name"]
            if name not in EXCLUDE_REPOS:
                repos.append(repo["full_name"])
        page += 1
    return repos


def fetch_commits(repo_full, date_str):
    """특정 레포에서 해당 날짜의 커밋 수집"""
    headers = {
        "Accept": "application/vnd.github+json",
        "Authorization": f"Bearer {GITHUB_TOKEN}",
        "X-GitHub-Api-Version": "2022-11-28",
    }
    since = f"{date_str}T00:00:00+09:00"
    until = f"{date_str}T23:59:59+09:00"
    
    url = f"https://api.github.com/repos/{repo_full}/commits"
    params = {
        "author": GITHUB_USERNAME,
        "since": since,
        "until": until,
        "per_page": 100,
    }
    
    try:
        r = requests.get(url, headers=headers, params=params, timeout=30)
        if r.status_code != 200:
            return []
        
        commits = []
        for c in r.json():
            commits.append({
                "repo": repo_full.split("/")[1],
                "sha": c["sha"][:7],
                "message": c["commit"]["message"].split("\n")[0],
                "time": c["commit"]["author"]["date"],
                "url": c["html_url"],
            })
        return commits
    except Exception as e:
        print(f"[WARN] {repo_full} fetch error: {e}")
        return []


def collect_all_commits(date_str):
    """모든 레포에서 커밋 수집"""
    print(f"  Scanning repos for {GITHUB_USERNAME}...")
    repos = get_all_repos()
    print(f"  Found {len(repos)} repos (excluding {EXCLUDE_REPOS})")
    
    all_commits = {}
    total = 0
    for repo_full in repos:
        commits = fetch_commits(repo_full, date_str)
        if commits:
            repo_name = repo_full.split("/")[1]
            all_commits[repo_name] = commits
            total += len(commits)
            print(f"    {repo_name}: {len(commits)} commits")
    
    print(f"  Total: {total} commits from {len(all_commits)} repos")
    return all_commits


# ═══════════════════════════════════════════════════════════════
# 2. 마스터 플랜 HTML 파싱
# ═══════════════════════════════════════════════════════════════

# 월 → 그리드 컬럼 매핑 (HTML 구조 기반)
MONTH_TO_COLUMN = {
    (2025, 12): 1,
    (2026, 1): 2,  (2026, 2): 3,  (2026, 3): 4,
    (2026, 4): 5,  (2026, 5): 6,  (2026, 6): 7,
    (2026, 7): 8,  (2026, 8): 9,  (2026, 9): 10,
    (2026, 10): 11, (2026, 11): 12, (2026, 12): 13,
    (2027, 1): 14, (2027, 2): 15, (2027, 3): 16,
}
# 4~6월 2027 → 17, 복직후 → 18

# Phase 정보
PHASES = [
    {"name": "Phase 1 — 출산 직후 (휴식)", "months": [(2025,12),(2026,1),(2026,2)], "emoji": "😴"},
    {"name": "Phase 2 — 회복기", "months": [(2026,3)], "emoji": "🌱"},
    {"name": "Phase 3 — 본격 시작", "months": [(2026,4),(2026,5),(2026,6),(2026,7),(2026,8),(2026,9)], "emoji": "🔥"},
    {"name": "Phase 4 — 버튜버 집중", "months": [(2026,10),(2026,11),(2026,12),(2027,1),(2027,2)], "emoji": "🎨"},
    {"name": "Phase 5 — 버튜버 외주 시작", "months": [(2027,3)], "emoji": "💼"},
    {"name": "Phase 6 — 복직 후", "months": [], "emoji": "🎉"},
]

# 프로젝트별 월간 계획 (HTML 간트차트에서 추출)
PROJECT_SCHEDULE = {
    "뽀모도로 앱": {
        "emoji": "📱",
        "keywords": ["pomory", "pomodoro", "뽀모도로", "fairy", "요정"],
        "schedule": {
            (2026, 3): "개발 재개",
            (2026, 4): "개발", (2026, 5): "개발", (2026, 6): "개발", (2026, 7): "개발",
            (2026, 8): "출시",
            (2026, 9): "수익/유지보수", (2026, 10): "유지보수", (2026, 11): "유지보수",
            (2026, 12): "유지보수", (2027, 1): "유지보수", (2027, 2): "유지보수",
        }
    },
    "타임블록 앱": {
        "emoji": "📱",
        "keywords": ["timeblock", "타임블록", "time-block"],
        "schedule": {
            (2026, 10): "개발", (2026, 11): "개발", (2026, 12): "개발", (2027, 1): "개발",
            (2027, 2): "출시",
        }
    },
    "버튜버 외주": {
        "emoji": "🎨",
        "keywords": ["vtuber", "버튜버", "blender", "블렌더", "unity", "유니티", "rigging", "리깅", "vrm"],
        "schedule": {
            (2026, 4): "블렌더 학습", (2026, 5): "블렌더 학습", (2026, 6): "블렌더 학습",
            (2026, 7): "블렌더 학습", (2026, 8): "블렌더 학습", (2026, 9): "블렌더 학습",
            (2026, 10): "유니티+리깅", (2026, 11): "유니티+리깅",
            (2026, 12): "유니티+리깅", (2027, 1): "유니티+리깅",
            (2027, 2): "포트폴리오", (2027, 3): "포트폴리오",
        }
    },
    "웹소설": {
        "emoji": "📝",
        "keywords": ["novel", "웹소설", "소설", "novel_assistant"],
        "schedule": {
            # 3월부터 계속 (틈틈이)
            (2026, 3): "틈틈이 집필", (2026, 4): "틈틈이 집필", (2026, 5): "틈틈이 집필",
            (2026, 6): "틈틈이 집필", (2026, 7): "틈틈이 집필", (2026, 8): "틈틈이 집필",
            (2026, 9): "틈틈이 집필", (2026, 10): "틈틈이 집필", (2026, 11): "틈틈이 집필",
            (2026, 12): "틈틈이 집필", (2027, 1): "틈틈이 집필", (2027, 2): "틈틈이 집필",
        }
    },
    "스톡이미지": {
        "emoji": "🖼️",
        "keywords": ["stock", "스톡", "이미지"],
        "schedule": {
            (2026, 8): "부산물 업로드 시작", (2026, 9): "업로드",
            (2026, 10): "업로드", (2026, 11): "업로드", (2026, 12): "업로드",
            (2027, 1): "업로드", (2027, 2): "업로드",
        }
    },
    "인스타툰": {
        "emoji": "🎨",
        "keywords": ["insta", "인스타", "sideproject", "toon", "만화", "webtoon"],
        "schedule": {
            (2026, 3): "월 2회", (2026, 4): "월 2회", (2026, 5): "월 2회",
            (2026, 6): "월 2회", (2026, 7): "월 2회", (2026, 8): "월 2회",
        }
    },
}

# 레포 → 프로젝트 매핑 (알려진 레포)
REPO_PROJECT_MAP = {
    "Pomory": "뽀모도로 앱",
    "Novel_Assistant": "웹소설",
    "SideProject_Plan": "인스타툰",
}


def get_current_phase(year, month):
    """현재 날짜의 Phase 반환"""
    for phase in PHASES:
        if (year, month) in phase["months"]:
            return phase
    # Phase 5 이후 (2027.4~6)
    if year == 2027 and 4 <= month <= 6:
        return PHASES[4]
    # 복직 후
    if year >= 2027 and month >= 7:
        return PHASES[5]
    return PHASES[0]


def get_month_plans(year, month):
    """해당 월에 예정된 프로젝트별 계획 반환"""
    plans = []
    for project_name, info in PROJECT_SCHEDULE.items():
        key = (year, month)
        if key in info["schedule"]:
            plans.append({
                "project": project_name,
                "emoji": info["emoji"],
                "task": info["schedule"][key],
                "keywords": info["keywords"],
            })
    return plans


def match_commits_to_plan(commits, plans):
    """커밋을 마스터 플랜 항목과 매칭"""
    matched = []     # (plan, [commits])
    unmatched = []   # commits not matching any plan
    
    used_commits = set()
    
    for plan in plans:
        plan_commits = []
        keywords = plan["keywords"]
        
        for repo_name, repo_commits in commits.items():
            # 1차: 레포 이름으로 매칭
            mapped_project = REPO_PROJECT_MAP.get(repo_name)
            if mapped_project == plan["project"]:
                for c in repo_commits:
                    commit_id = f"{repo_name}:{c['sha']}"
                    if commit_id not in used_commits:
                        plan_commits.append(c)
                        used_commits.add(commit_id)
                continue
            
            # 2차: 키워드로 매칭
            for c in repo_commits:
                commit_id = f"{repo_name}:{c['sha']}"
                if commit_id in used_commits:
                    continue
                msg_lower = c["message"].lower()
                repo_lower = repo_name.lower()
                for kw in keywords:
                    if kw.lower() in msg_lower or kw.lower() in repo_lower:
                        plan_commits.append(c)
                        used_commits.add(commit_id)
                        break
        
        matched.append({
            "plan": plan,
            "commits": plan_commits,
            "status": "진행됨" if plan_commits else "오늘 작업 없음",
        })
    
    # 매칭 안 된 커밋
    for repo_name, repo_commits in commits.items():
        for c in repo_commits:
            commit_id = f"{repo_name}:{c['sha']}"
            if commit_id not in used_commits:
                unmatched.append({**c, "repo": repo_name})
    
    return matched, unmatched


# ═══════════════════════════════════════════════════════════════
# 3. 마크다운 일지 생성
# ═══════════════════════════════════════════════════════════════

def generate_journal(date_str, commits, matched, unmatched, phase):
    """마크다운 형식의 일지 생성"""
    dt = datetime.strptime(date_str, "%Y-%m-%d")
    weekday = ["월", "화", "수", "목", "금", "토", "일"][dt.weekday()]
    
    prev_date = (dt - timedelta(days=1)).strftime("%Y-%m-%d")
    next_date = (dt + timedelta(days=1)).strftime("%Y-%m-%d")
    
    total_commits = sum(len(v) for v in commits.values())
    matched_count = sum(1 for m in matched if m["commits"])
    total_plans = len(matched)
    
    lines = []
    
    # 프론트매터
    lines.append("---")
    lines.append(f"date: {date_str}")
    lines.append("type: journal")
    lines.append(f"phase: \"{phase['name']}\"")
    lines.append(f"total_commits: {total_commits}")
    lines.append(f"plan_progress: {matched_count}/{total_plans}")
    lines.append("tags: [journal, auto-generated]")
    lines.append("---")
    lines.append("")
    
    # 헤더
    lines.append(f"# {date_str} ({weekday}) 작업일지")
    lines.append("")
    lines.append(f"<< [[{prev_date}]] | [[{next_date}]] >>")
    lines.append("")
    
    # Phase 정보
    lines.append(f"> {phase['emoji']} **{phase['name']}**")
    lines.append("")
    
    # 커밋 내역
    lines.append("## 커밋 내역")
    lines.append("")
    if not commits:
        lines.append("오늘 커밋 없음")
    else:
        for repo_name, repo_commits in sorted(commits.items()):
            lines.append(f"### {repo_name} ({len(repo_commits)}건)")
            for c in repo_commits:
                lines.append(f"- `{c['sha']}` {c['message']}")
            lines.append("")
    lines.append("")
    
    # 마스터 플랜 매칭
    lines.append("## 마스터 플랜 매칭")
    lines.append("")
    lines.append("| 계획 항목 | 예정 작업 | 오늘 진행 | 커밋 수 |")
    lines.append("|-----------|----------|----------|--------|")
    for m in matched:
        plan = m["plan"]
        status = "✅ 진행됨" if m["commits"] else "➖ 작업 없음"
        count = f"{len(m['commits'])}건" if m["commits"] else "-"
        lines.append(f"| {plan['emoji']} {plan['project']} | {plan['task']} | {status} | {count} |")
    lines.append("")
    
    # 계획 외 작업
    if unmatched:
        lines.append("## 계획 외 작업")
        lines.append("")
        for c in unmatched:
            lines.append(f"- `{c['repo']}` {c['message']} ({c['sha']})")
        lines.append("")
    
    # 요약
    lines.append("## 요약")
    lines.append("")
    if total_plans > 0:
        rate = round(matched_count / total_plans * 100)
        lines.append(f"- **진행률**: {matched_count}/{total_plans} ({rate}%)")
    lines.append(f"- **총 커밋**: {total_commits}건")
    if unmatched:
        lines.append(f"- **계획 외 작업**: {len(unmatched)}건")
    lines.append("")
    
    # 메모 섹션 (수동 작성용)
    lines.append("## 메모")
    lines.append("")
    lines.append("")
    
    return "\n".join(lines)


# ═══════════════════════════════════════════════════════════════
# 4. 파일 저장 및 Git push
# ═══════════════════════════════════════════════════════════════

def save_journal(date_str, content):
    """일지 파일 저장 (기존 메모 보존)"""
    JOURNAL_DIR.mkdir(parents=True, exist_ok=True)
    filepath = JOURNAL_DIR / f"{date_str}.md"
    
    # 기존 파일이 있으면 수동 메모 섹션 보존
    if filepath.exists():
        old_text = filepath.read_text(encoding="utf-8")
        old_memo = ""
        if "## 메모" in old_text:
            memo_part = old_text.split("## 메모")[1]
            # 다음 ## 섹션이 나오기 전까지가 메모 내용
            if "\n## " in memo_part:
                old_memo = memo_part.split("\n## ")[0]
            else:
                old_memo = memo_part
            old_memo = old_memo.strip()
        
        # 기존 메모가 있으면 새 일지의 메모 섹션에 삽입
        if old_memo:
            content = content.replace(
                "## 메모\n\n\n",
                f"## 메모\n\n{old_memo}\n\n"
            )
            print(f"  Preserved existing memo")
    
    filepath.write_text(content, encoding="utf-8")
    print(f"  Saved: {filepath}")
    return filepath


def git_commit_and_push(date_str):
    """볼트 레포에 커밋 & 푸시"""
    try:
        os.chdir(VAULT_PATH)
        
        # pull first (충돌 방지)
        subprocess.run(["git", "pull", "--rebase"], capture_output=True, timeout=30)
        
        # add & commit
        subprocess.run(["git", "add", "."], check=True, capture_output=True, timeout=30)
        
        result = subprocess.run(
            ["git", "status", "--porcelain"],
            capture_output=True, text=True, timeout=10
        )
        
        if result.stdout.strip():
            subprocess.run(
                ["git", "commit", "-m", f"auto: {date_str} work log"],
                check=True, capture_output=True, timeout=30
            )
            subprocess.run(
                ["git", "push"],
                check=True, capture_output=True, timeout=60
            )
            print(f"  Git push complete")
        else:
            print(f"  No changes to commit")
    except Exception as e:
        print(f"  [WARN] Git error: {e}")


# ═══════════════════════════════════════════════════════════════
# 메인
# ═══════════════════════════════════════════════════════════════

def main():
    # 날짜 결정
    if len(sys.argv) > 1:
        date_str = sys.argv[1]
    else:
        date_str = datetime.now(KST).strftime("%Y-%m-%d")
    
    dt = datetime.strptime(date_str, "%Y-%m-%d")
    year, month = dt.year, dt.month
    
    print(f"{'='*50}")
    print(f"  Gabi Brain - Work Log Generator")
    print(f"  Date: {date_str}")
    print(f"{'='*50}")
    
    # 토큰 확인
    if not GITHUB_TOKEN:
        print("[ERROR] GITHUB_PAT 환경변수를 설정해주세요.")
        print("  set GITHUB_PAT=ghp_xxxxxxxxxxxx")
        sys.exit(1)
    
    # Phase 확인
    phase = get_current_phase(year, month)
    print(f"\n  Phase: {phase['emoji']} {phase['name']}")
    
    # 이번 달 계획 가져오기
    plans = get_month_plans(year, month)
    print(f"  Plans this month: {len(plans)}")
    for p in plans:
        print(f"    {p['emoji']} {p['project']}: {p['task']}")
    
    # 커밋 수집
    print(f"\n  Collecting commits...")
    commits = collect_all_commits(date_str)
    
    # 매칭
    print(f"\n  Matching commits to plan...")
    matched, unmatched = match_commits_to_plan(commits, plans)
    
    # 일지 생성
    print(f"\n  Generating journal...")
    content = generate_journal(date_str, commits, matched, unmatched, phase)
    save_journal(date_str, content)
    
    # Git push
    print(f"\n  Pushing to Git...")
    git_commit_and_push(date_str)
    
    # 완료
    total_commits = sum(len(v) for v in commits.values())
    matched_count = sum(1 for m in matched if m["commits"])
    print(f"\n{'='*50}")
    print(f"  Done! {total_commits} commits, {matched_count}/{len(matched)} plans matched")
    print(f"{'='*50}")


if __name__ == "__main__":
    main()
