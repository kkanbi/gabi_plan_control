#!/usr/bin/env python3
"""
Gabi Brain - Daily Work Log Generator
=====================================
매일 밤 실행: GitHub 커밋 수집 → 마스터 플랜 매칭 → 옵시디언 일지 자동 생성

프로젝트 일정/페이즈는 50_Strategy/2026_ProjectTimeline.md 에서 자동으로 읽음.
하드코딩 없이 마크다운 파일만 수정하면 반영됨.

사용법:
  python generate_worklog.py              # 오늘 날짜 기준
  python generate_worklog.py 2026-03-21   # 특정 날짜 지정
"""

import os
import re
import sys
import subprocess
from datetime import datetime, timezone, timedelta, date
from pathlib import Path

try:
    import requests
except ImportError:
    print("[ERROR] requests 라이브러리가 필요합니다: pip install requests")
    sys.exit(1)


# ═══════════════════════════════════════════════════════════════
# 설정
# ═══════════════════════════════════════════════════════════════

GITHUB_TOKEN    = os.environ.get("GITHUB_PAT", "")
GITHUB_USERNAME = "kkanbi"

VAULT_PATH   = Path(os.environ.get("VAULT_PATH") or Path(__file__).resolve().parent.parent.parent)
JOURNAL_DIR  = VAULT_PATH / "60_Journal"
TIMELINE_PATH = VAULT_PATH / "50_Strategy" / "2026_ProjectTimeline.md"

# 소설 폴더 경로 (환경변수로 override 가능)
NOVEL_PATH = Path(os.environ.get("NOVEL_PATH", r"D:\Google_Drive_Online\소설\BL_껍질이깨지는파열음"))

KST = timezone(timedelta(hours=9))


# ═══════════════════════════════════════════════════════════════
# 1. 타임라인 파싱 (2026_ProjectTimeline.md)
# ═══════════════════════════════════════════════════════════════

def _parse_frontmatter(text):
    """YAML frontmatter에서 projects 목록 파싱 (PyYAML 없이)"""
    fm_match = re.match(r'^---\n(.*?)\n---', text, re.DOTALL)
    if not fm_match:
        return {}

    yaml_text = fm_match.group(1)
    projects = {}

    # "  - name: X" 기준으로 프로젝트 블록 분리
    blocks = re.split(r'\n  - name:', yaml_text)
    for block in blocks[1:]:
        lines = block.strip().split('\n')
        name = lines[0].strip()

        repo_m     = re.search(r'repo:\s*(.+)',              block)
        emoji_m    = re.search(r'emoji:\s*"?([^"\n]+)"?',   block)
        keywords_m = re.search(r'keywords:\s*\[([^\]]+)\]', block)

        projects[name] = {
            "repo":     repo_m.group(1).strip()                                      if repo_m     else "",
            "emoji":    emoji_m.group(1).strip()                                     if emoji_m    else "📌",
            "keywords": [k.strip() for k in keywords_m.group(1).split(',')]         if keywords_m else [],
        }

    return projects


def _parse_gantt(text):
    """Mermaid gantt 블록에서 section → tasks 파싱"""
    gantt_match = re.search(r'```mermaid\ngantt(.*?)```', text, re.DOTALL)
    if not gantt_match:
        return {}

    sections = {}
    current  = None
    skip_keywords = {'title', 'dateFormat', 'axisFormat'}

    for raw_line in gantt_match.group(1).split('\n'):
        line = raw_line.strip()
        if not line or any(line.startswith(k) for k in skip_keywords):
            continue

        if line.startswith('section '):
            current = line[8:].strip()
            sections[current] = []
            continue

        if current is None:
            continue

        m = re.match(r'^(.+?)\s*:(.*?)$', line)
        if not m:
            continue

        task_name = m.group(1).strip()
        rest      = m.group(2).strip()
        parts     = [p.strip() for p in rest.split(',')]

        if any('milestone' in p for p in parts):
            continue

        dates = [p for p in parts if re.match(r'\d{4}-\d{2}-\d{2}', p)]
        if len(dates) < 2:
            continue

        try:
            start = datetime.strptime(dates[0], '%Y-%m-%d').date()
            end   = datetime.strptime(dates[1], '%Y-%m-%d').date()
        except ValueError:
            continue

        sections[current].append({"task": task_name, "start": start, "end": end})

    return sections


def _month_schedule(tasks):
    """task 리스트 → {(year, month): task_name} 딕셔너리"""
    schedule = {}
    for t in tasks:
        cur = t["start"].replace(day=1)
        while cur < t["end"]:
            key = (cur.year, cur.month)
            if key not in schedule:
                schedule[key] = t["task"]
            # 다음 달
            if cur.month == 12:
                cur = cur.replace(year=cur.year + 1, month=1)
            else:
                cur = cur.replace(month=cur.month + 1)
    return schedule


def _strip_emoji(s):
    """문자열 앞 이모지·공백 제거"""
    return re.sub(r'^[\U0001F000-\U0001FFFF\u2600-\u26FF\u2700-\u27BF\s]+', '', s).strip()


PHASE_EMOJI_MAP = {
    "휴식": "😴", "회복": "🌱", "개발": "🔥", "집중": "🎯",
    "출시": "🚀", "수익": "💼", "복직": "🎉",
}


def parse_timeline(path=TIMELINE_PATH):
    """
    2026_ProjectTimeline.md 파싱 → (projects, phases) 반환

    projects : [{"name", "emoji", "keywords", "repo", "schedule": {(y,m): str}}]
    phases   : [{"name", "emoji", "start": date, "end": date}]
    """
    if not path.exists():
        print(f"[WARN] 타임라인 파일 없음: {path}")
        return [], []

    text       = path.read_text(encoding="utf-8")
    fm_projects = _parse_frontmatter(text)
    sections    = _parse_gantt(text)

    # ── phases ──────────────────────────────────────────────────
    phases = []
    for section_name, tasks in sections.items():
        if '페이즈' not in section_name and 'phase' not in section_name.lower():
            continue
        for t in tasks:
            emoji = next(
                (em for kw, em in PHASE_EMOJI_MAP.items() if kw in t["task"]),
                "📅"
            )
            phases.append({
                "name":  t["task"],
                "emoji": emoji,
                "start": t["start"],
                "end":   t["end"],
            })
        break   # 페이즈 섹션은 하나만

    # ── projects ─────────────────────────────────────────────────
    projects = []
    for section_name, tasks in sections.items():
        if '페이즈' in section_name or 'phase' in section_name.lower():
            continue

        # section 이름 → 프로젝트 이름 정규화
        clean = _strip_emoji(section_name)
        clean = re.sub(r'\s*\(.+\)', '', clean).strip()   # "(서브)" 등 제거

        info     = fm_projects.get(clean, {})
        repo     = info.get("repo", "")
        keywords = list(info.get("keywords", []))

        # repo 이름이 keywords에 없으면 자동 추가
        if repo and repo.lower() not in [k.lower() for k in keywords]:
            keywords.insert(0, repo.lower())

        # keywords 없으면 프로젝트 이름 단어로 대체
        if not keywords:
            keywords = [w.lower() for w in clean.split() if len(w) > 1]

        projects.append({
            "name":     clean,
            "emoji":    info.get("emoji", "📌"),
            "keywords": keywords,
            "repo":     repo,
            "schedule": _month_schedule(tasks),
        })

    return projects, phases


def get_current_phase(phases, dt):
    """날짜에 해당하는 Phase 반환"""
    d = dt.date() if isinstance(dt, datetime) else dt
    for phase in phases:
        if phase["start"] <= d < phase["end"]:
            return phase
    return phases[-1] if phases else {"name": "Unknown", "emoji": "❓"}


def get_month_plans(projects, year, month):
    """해당 월에 예정된 프로젝트별 계획 반환"""
    key = (year, month)
    return [
        {
            "project":  p["name"],
            "emoji":    p["emoji"],
            "task":     p["schedule"][key],
            "keywords": p["keywords"],
        }
        for p in projects
        if key in p.get("schedule", {})
    ]


# ═══════════════════════════════════════════════════════════════
# 2. GitHub API: 커밋 수집
# ═══════════════════════════════════════════════════════════════

def _gh_headers():
    return {
        "Accept":               "application/vnd.github+json",
        "Authorization":        f"Bearer {GITHUB_TOKEN}",
        "X-GitHub-Api-Version": "2022-11-28",
    }


def get_all_repos():
    repos, page = [], 1
    while True:
        url = f"https://api.github.com/user/repos?per_page=100&page={page}&affiliation=owner"
        r = requests.get(url, headers=_gh_headers(), timeout=30)
        if r.status_code != 200:
            print(f"[WARN] Repo list API error: {r.status_code}")
            break
        data = r.json()
        if not data:
            break
        repos.extend(repo["full_name"] for repo in data)
        page += 1
    return repos


def fetch_commits(repo_full, date_str):
    url    = f"https://api.github.com/repos/{repo_full}/commits"
    params = {
        "author":   GITHUB_USERNAME,
        "since":    f"{date_str}T00:00:00+09:00",
        "until":    f"{date_str}T23:59:59+09:00",
        "per_page": 100,
    }
    try:
        r = requests.get(url, headers=_gh_headers(), params=params, timeout=30)
        if r.status_code != 200:
            return []
        return [
            {
                "repo":    repo_full.split("/")[1],
                "sha":     c["sha"][:7],
                "message": c["commit"]["message"].split("\n")[0],
                "time":    c["commit"]["author"]["date"],
                "url":     c["html_url"],
            }
            for c in r.json()
        ]
    except Exception as e:
        print(f"[WARN] {repo_full} fetch error: {e}")
        return []


def collect_all_commits(date_str):
    print(f"  Scanning repos for {GITHUB_USERNAME}...")
    repos = get_all_repos()
    print(f"  Found {len(repos)} repos")

    all_commits, total = {}, 0
    for repo_full in repos:
        commits = fetch_commits(repo_full, date_str)
        if commits:
            name = repo_full.split("/")[1]
            all_commits[name] = commits
            total += len(commits)
            print(f"    {name}: {len(commits)} commits")

    print(f"  Total: {total} commits from {len(all_commits)} repos")
    return all_commits


# ═══════════════════════════════════════════════════════════════
# 3. 소설 집필 체크 (로컬 Google Drive 동기화 폴더)
# ═══════════════════════════════════════════════════════════════

def check_novel_activity(date_str):
    """
    NOVEL_PATH 폴더에서 해당 날짜에 수정된 파일 목록 반환.
    폴더가 없으면 빈 리스트.
    """
    if not NOVEL_PATH.exists():
        print(f"  [SKIP] 소설 폴더 없음: {NOVEL_PATH}")
        return []

    target = datetime.strptime(date_str, "%Y-%m-%d").date()
    modified = []

    for f in NOVEL_PATH.rglob("*"):
        if not f.is_file():
            continue
        mtime = datetime.fromtimestamp(f.stat().st_mtime, tz=KST).date()
        if mtime == target:
            modified.append(f.name)

    return modified


# ═══════════════════════════════════════════════════════════════
# 4. 커밋 → 플랜 매칭
# ═══════════════════════════════════════════════════════════════

def match_commits_to_plan(commits, plans, projects):
    repo_project_map = {p["repo"]: p["name"] for p in projects if p["repo"]}

    used_commits = set()
    matched      = []

    for plan in plans:
        plan_commits = []
        keywords     = plan["keywords"]

        for repo_name, repo_commits in commits.items():
            mapped = repo_project_map.get(repo_name)
            if mapped == plan["project"]:
                for c in repo_commits:
                    cid = f"{repo_name}:{c['sha']}"
                    if cid not in used_commits:
                        plan_commits.append(c)
                        used_commits.add(cid)
                continue

            for c in repo_commits:
                cid = f"{repo_name}:{c['sha']}"
                if cid in used_commits:
                    continue
                msg_lower  = c["message"].lower()
                repo_lower = repo_name.lower()
                if any(kw.lower() in msg_lower or kw.lower() in repo_lower for kw in keywords):
                    plan_commits.append(c)
                    used_commits.add(cid)

        matched.append({
            "plan":    plan,
            "commits": plan_commits,
            "status":  "진행됨" if plan_commits else "오늘 작업 없음",
        })

    # 매칭 안 된 커밋
    unmatched = [
        {**c, "repo": repo_name}
        for repo_name, repo_commits in commits.items()
        for c in repo_commits
        if f"{repo_name}:{c['sha']}" not in used_commits
    ]

    return matched, unmatched


# ═══════════════════════════════════════════════════════════════
# 5. 마크다운 일지 생성
# ═══════════════════════════════════════════════════════════════

def generate_journal(date_str, commits, matched, unmatched, phase, novel_files=None):
    dt      = datetime.strptime(date_str, "%Y-%m-%d")
    weekday = ["월", "화", "수", "목", "금", "토", "일"][dt.weekday()]
    prev    = (dt - timedelta(days=1)).strftime("%Y-%m-%d")
    nxt     = (dt + timedelta(days=1)).strftime("%Y-%m-%d")

    total_commits  = sum(len(v) for v in commits.values())
    matched_count  = sum(1 for m in matched if m["commits"])
    total_plans    = len(matched)

    lines = [
        "---",
        f"date: {date_str}",
        "type: journal",
        f"phase: \"{phase['name']}\"",
        f"total_commits: {total_commits}",
        f"plan_progress: {matched_count}/{total_plans}",
        "tags: [journal, auto-generated]",
        "---",
        "",
        f"# {date_str} ({weekday}) 작업일지",
        "",
        f"<< [[{prev}]] | [[{nxt}]] >>",
        "",
        f"> {phase['emoji']} **{phase['name']}**",
        "",
        "## 커밋 내역",
        "",
    ]

    if not commits:
        lines.append("오늘 커밋 없음")
    else:
        for repo_name, repo_commits in sorted(commits.items()):
            lines.append(f"### {repo_name} ({len(repo_commits)}건)")
            lines.extend(f"- `{c['sha']}` {c['message']}" for c in repo_commits)
            lines.append("")

    lines += [
        "",
        "## 마스터 플랜 매칭",
        "",
        "| 계획 항목 | 예정 작업 | 오늘 진행 | 커밋 수 |",
        "|-----------|----------|----------|--------|",
    ]
    for m in matched:
        plan   = m["plan"]
        status = "✅ 진행됨" if m["commits"] else "➖ 작업 없음"
        count  = f"{len(m['commits'])}건" if m["commits"] else "-"
        lines.append(f"| {plan['emoji']} {plan['project']} | {plan['task']} | {status} | {count} |")
    lines.append("")

    if unmatched:
        lines += ["## 계획 외 작업", ""]
        lines.extend(f"- `{c['repo']}` {c['message']} ({c['sha']})" for c in unmatched)
        lines.append("")

    lines += ["## 웹소설 집필", ""]
    if novel_files:
        lines.append("✅ 오늘 집필함")
        for fname in novel_files:
            lines.append(f"- {fname}")
    else:
        lines.append("➖ 오늘 집필 없음")
    lines.append("")

    lines += ["## 요약", ""]
    if total_plans > 0:
        rate = round(matched_count / total_plans * 100)
        lines.append(f"- **진행률**: {matched_count}/{total_plans} ({rate}%)")
    lines.append(f"- **총 커밋**: {total_commits}건")
    if unmatched:
        lines.append(f"- **계획 외 작업**: {len(unmatched)}건")

    lines += ["", "## 메모", "", ""]

    return "\n".join(lines)


# ═══════════════════════════════════════════════════════════════
# 6. 파일 저장 및 Git push
# ═══════════════════════════════════════════════════════════════

def save_journal(date_str, content):
    JOURNAL_DIR.mkdir(parents=True, exist_ok=True)
    filepath = JOURNAL_DIR / f"{date_str}.md"

    if filepath.exists():
        old_text = filepath.read_text(encoding="utf-8")
        old_memo = ""
        if "## 메모" in old_text:
            memo_part = old_text.split("## 메모")[1]
            old_memo  = (memo_part.split("\n## ")[0] if "\n## " in memo_part else memo_part).strip()
        if old_memo:
            content = content.replace("## 메모\n\n\n", f"## 메모\n\n{old_memo}\n\n")
            print("  Preserved existing memo")

    filepath.write_text(content, encoding="utf-8")
    print(f"  Saved: {filepath}")
    return filepath


def git_commit_and_push(date_str):
    try:
        os.chdir(VAULT_PATH)
        subprocess.run(["git", "pull", "--rebase"], capture_output=True, timeout=30)
        subprocess.run(["git", "add", "."],         check=True, capture_output=True, timeout=30)

        result = subprocess.run(
            ["git", "status", "--porcelain"],
            capture_output=True, text=True, timeout=10
        )
        if result.stdout.strip():
            subprocess.run(
                ["git", "commit", "-m", f"auto: {date_str} work log"],
                check=True, capture_output=True, timeout=30
            )
            subprocess.run(["git", "push"], check=True, capture_output=True, timeout=60)
            print("  Git push complete")
        else:
            print("  No changes to commit")
    except Exception as e:
        print(f"  [WARN] Git error: {e}")


# ═══════════════════════════════════════════════════════════════
# 메인
# ═══════════════════════════════════════════════════════════════

def main():
    date_str = sys.argv[1] if len(sys.argv) > 1 else datetime.now(KST).strftime("%Y-%m-%d")
    dt       = datetime.strptime(date_str, "%Y-%m-%d")

    print(f"{'='*50}")
    print(f"  Gabi Brain - Work Log Generator")
    print(f"  Date: {date_str}")
    print(f"{'='*50}")

    if not GITHUB_TOKEN:
        print("[ERROR] GITHUB_PAT 환경변수를 설정해주세요.")
        sys.exit(1)

    # 타임라인 파일에서 프로젝트·페이즈 로드
    print(f"\n  Loading timeline from: {TIMELINE_PATH.name}")
    projects, phases = parse_timeline()
    print(f"  Projects: {len(projects)}개 / Phases: {len(phases)}개")

    phase = get_current_phase(phases, dt)
    print(f"  Phase: {phase['emoji']} {phase['name']}")

    plans = get_month_plans(projects, dt.year, dt.month)
    print(f"  Plans this month: {len(plans)}")
    for p in plans:
        print(f"    {p['emoji']} {p['project']}: {p['task']}")

    print(f"\n  Collecting commits...")
    commits = collect_all_commits(date_str)

    print(f"\n  Matching commits to plan...")
    matched, unmatched = match_commits_to_plan(commits, plans, projects)

    print(f"\n  Checking novel activity...")
    novel_files = check_novel_activity(date_str)
    if novel_files:
        print(f"  소설 집필 감지: {len(novel_files)}개 파일 수정됨")
    else:
        print(f"  소설 집필 없음")

    print(f"\n  Generating journal...")
    content = generate_journal(date_str, commits, matched, unmatched, phase, novel_files)
    save_journal(date_str, content)

    print(f"\n  Pushing to Git...")
    git_commit_and_push(date_str)

    total_commits = sum(len(v) for v in commits.values())
    matched_count = sum(1 for m in matched if m["commits"])
    print(f"\n{'='*50}")
    print(f"  Done! {total_commits} commits, {matched_count}/{len(matched)} plans matched")
    print(f"{'='*50}")


if __name__ == "__main__":
    main()
