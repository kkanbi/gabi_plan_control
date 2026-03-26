# Work Log

---

### 2026-03-26 (세션 5)
- [버그수정] Gemini 429 에러 → 명확한 한국어 메시지로 처리
- [기능] 일반 링크 제목 자동추출 (allorigins.win CORS 프록시 → og:title / <title> 파싱)
- [기능] Twitter/X 트윗 내용 자동추출 (publish.twitter.com oEmbed, 무료)
- [기능] Threads 게시물 제목 추출 (allorigins 프록시 → og:title)
- [기능] Instagram 공개 게시물 제목 시도 (allorigins, 로그인 필요 게시물은 불가)
- [개선] detectPlatform에 threads.net 추가
- 옵시디언 저장 경로: 00_Inbox/날짜/ 구조로 변경

### 2026-03-26 (세션 4)
- [기능] Gemini API 통합 - 제목 기반 카테고리/태그 자동 분류
  - YouTube API 제거 → Gemini API 하나로 통합
  - API 설정 모달: Gemini API 키 입력 (Google AI Studio 무료 발급)
  - 제목 옆 "✨ AI 분류" 버튼: 현재 제목으로 Gemini 분류 즉시 실행
  - URL 붙여넣기 시 제목 확보 후 Gemini 자동 호출 (키 없으면 URL 기반 폴백)
  - 기존 카테고리/태그 목록 프롬프트에 포함 → 일관된 분류 유지
  - 모델: gemini-2.0-flash (무료 티어)

### 2026-03-26 (세션 3)
- [기능] 옵시디언 Vault 연동 구현 (File System Access API)
  - 사이드바 "Vault 폴더 연결" 버튼 → showDirectoryPicker()로 폴더 권한 부여
  - 저장 시 category/{title}.md 자동 생성 (YAML frontmatter + 마크다운 형식)
  - 삭제 시 .md 파일 자동 삭제
  - "전체 동기화" 버튼으로 기존 항목 일괄 export
  - IndexedDB에 폴더 핸들 저장 → 재시작 시 권한 재요청으로 재연결
- [기능] Toast 알림 시스템 추가 (success/error 색상 구분)
- [기능] API 설정 모달 추가
  - YouTube Data API v3 키 입력 → 영상 설명/태그 기반 자동 분류
  - API 키 없으면 기존 oEmbed 폴백 유지
- [기능] 컨텐츠 내용 기반 태그 추출 (extractKeywordsFromText) - 설명 텍스트 키워드 분석

### 2026-03-26 (세션 2)
- [버그수정] 테이블 뷰 날짜/아이콘 겹침 → card-actions width 90→116px로 확대
- [기능개선] 카테고리·태그 칩 UI 추가
  - 폼 하단에 기존 카테고리/태그 칩 표시, 클릭으로 선택/토글
  - 저장·로드·클리어·URL 자동완성 시 칩 갱신 (updateFormChips)
  - 선택된 항목 active 상태로 시각적 표시
- [버그수정] URL 붙여넣기 자동완성 미동작 수정
  - suggestCategory: 기존 항목 없어도 도메인 기본값 반환 (youtube→영상, github→개발 등)
  - suggestTags: 기존 태그 없어도 플랫폼 기본 태그 반환 (youtube→영상/유튜브 등)

### 2026-03-26
- [실제] vault 인프라 버그 2건 수정
  - `.obsidian/workspace.json` git 추적 제거 (git rm --cached → push)
  - `run_worklog.bat` Python 오류 감지 추가 (%ERRORLEVEL% 체크)
- [실제] 2026-03-25 저널 수동 생성 (스크립트 직접 실행)
- [분석] ContentSaver 프로젝트 현황 파악
  - Phase 1 (단일 HTML PWA 앱) 100% 완료 상태 확인
  - Phase 2~4 미구현 항목 정리 (Google Drive, IndexedDB, Chrome Extension 등)
  - SPEC.md 기준 PHASE별 진행 현황 정리
- [개발] ContentSaver 신규 기능 2개 구현
  - URL 붙여넣기 자동 메타데이터 입력 (YouTube oEmbed 제목/썸네일, 기존 데이터 기반 카테고리/태그 추론)
  - 페이지네이션 (24개/페이지, 필터·정렬 변경 시 자동 리셋, 모바일 호환)
- [테스트] ContentSaver Phase 1 전체 기능 테스트 완료
  - 9개 항목 테스트 (레이아웃, 추가/수정/삭제, 카테고리/태그, 검색/필터, 즐겨찾기, 뷰전환/다크모드, Export/Import, 북마클릿, 키보드단축키)
  - 버그 2건 수정 (즐겨찾기 수정 시 초기화, 수정 모드 버튼 라벨)
  - 잔여 이슈 3건 확인 (삭제 confirm 블록, 한/영 정렬, .html 리다이렉트 쿼리 드롭)
