# 개발 환경 설정 — [프로젝트명]

---

## 요구사항

- Python 3.11+ / Node.js 18+ / Flutter 3.x (해당 항목만 남길 것)
- Git

---

## 빠른 시작

```bash
# 1. 레포 클론
git clone https://github.com/kkanbi/[repo-name]
cd [repo-name]

# 2. 가상환경 생성 (Python 프로젝트)
python -m venv venv
source venv/bin/activate  # Mac/Linux
venv\Scripts\activate     # Windows

# 3. 의존성 설치
pip install -r requirements.txt

# 4. 환경변수 설정
cp .env.example .env
# .env 파일 열어서 API 키 등 입력

# 5. 실행
python main.py
```

---

## 환경변수

`.env.example` 파일을 복사해서 `.env` 만들고 아래 항목 채우기:

| 변수명 | 설명 | 예시 |
|--------|------|------|
| `API_KEY` | 서비스 API 키 | `sk-...` |
| `DEBUG` | 디버그 모드 | `true` / `false` |

---

## 자주 쓰는 명령어

```bash
# 실행
python main.py

# 테스트
pytest tests/

# 린트
flake8 src/
```

---

## 트러블슈팅

문제가 생기면 먼저 `docs/CHANGELOG.md`의 **문제 해결 기록** 섹션 확인.
