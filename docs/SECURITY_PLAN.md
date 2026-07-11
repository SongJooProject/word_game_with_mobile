# 보안 강화 계획 (암호화 + 비밀번호 + private repo)

> 목표: 문제 데이터를 공개하지 않고, 허가된 사람만 앱을 쓰게 한다.
> Hermes가 계획/암호화 스크립트 작성/배포, OpenCode가 앱 코드 수정 담당.

## 현재 상태
- repo: `SongJooProject/word_game_with_mobile` → **private 변경 완료**
- 정적 사이트(GitHub Pages). 백엔드 없음.
- `data/questions.json`에 문제+정답 전부 평문 포함 (현재 URL로 누구나 열람 가능)

## 한계 (솔직히)
- 프론트엔드(.js)에 키/비밀번호 검증 로직이 있으므로 "완전한 보안"은 아님.
- 하지만 (private repo) + (암호화) + (비밀번호) 조합으로 "훑어보기/퍼가기"는 실질적으로 차단됨.
- 코드(.js/.html/.css) 자체는 숨길 수 없음 — 문제 DATA 보호에 집중.

## 구현 명세 (OpenCode 담당)

### 1. 암호화 스크립트 (Hermes가 작성하거나 OpenCode가 작성 — 텍스트 파일)
- 파일: `scripts/encrypt_questions.py`
- 입력: `data/questions.json`
- 출력: `data/questions.enc` (암호화된 1줄 base64 텍스트)
- 알고리즘: `cryptography` 라이브러리의 Fernet (대칭키)
  - 키는 환경변수 `QUIZ_KEY`에서 가져오거나, 없으면 `.env`에서 로드
  - 키 생성 스크립트/가이드도 포함 (`scripts/gen_key.py` 또는 README 메모)
- 중요: **`questions.json`(평문)은 repo에서 제외** (.gitignore에 추가). `questions.enc`만 커밋.

### 2. 앱 비밀번호 화면 (OpenCode 담당)
- `index.html`: 앱 최상단에 **잠금 화면(overlay)** 추가
  - 비밀번호 입력란 1개 + "입장" 버튼
  - 비밀번호 불일치 시 에러 메시지, 3회 시도 제한(단순)
- 스타일: 기존 노션 스타일 유지(DESIGN.md 색상)

### 3. 복호화 로직 (OpenCode 담당, js/game.js)
- 비밀번호 입력 → 검증:
  - 비밀번호 자체를 **키 유도에 사용** (예: 비밀번호로 Fernet 키 derivation, 또는 비밀번호 == 특정 토큰인지 확인 후 고정키로 복호화)
  - 권장: 비밀번호를 SHA-256 해시 → Fernet 키로 사용 (so 암호 모르면 복호 불가)
- `fetch('data/questions.enc')` → base64 디코드 → Fernet 복호 → JSON 파싱 → 기존 게임 로직 그대로 사용
- 기존 `loadQuestions()` 함수를 암호화 버전으로 교체 (questions.json 로드 부분만 변경, 나머지 게임 로직 보존)
- 서비스워커(sw.js) 캐시: `questions.enc`를 캐시 대상에 추가, 평문 questions.json은 삭제

### 4. .gitignore / 정리 (OpenCode 또는 Hermes)
- `data/questions.json` → .gitignore 추가 (평문 올라가지 않게)
- `questions.enc`는 커밋 대상 유지
- `.env`는 이미 gitignore됨 확인

## 비밀번호/키 관리
- 비밀번호(앱 입장용): 사용자가 정함. Hermes가 나중에 알려줌 (예: 고정값 또는 사용자 지정)
- Fernet 키: 암호화 스크립트 실행 시 생성, `.env`에 보관 (repo 비공개라 유출 위험 낮음)
- ⚠️ 앱은 비밀번호로 키를 유도하므로, .js에 평문 키를 박지 말 것 (보안성 낮아짐). 비밀번호 기반 derivation 사용.

## 검증 (Hermes 담당)
1. 로컬 서버: `python -m http.server 8000`
2. `curl localhost:8000/data/questions.enc` → 평문 아님(암호화 텍스트) 확인
3. `curl localhost:8000/data/questions.json` → 404 확인 (gitignore됨)
4. 브라우저: 잠금 화면 노출 → 오른 비밀번호 입력 시 게임 시작, 틀린 비밀번호 거부
5. 콘솔 에러 없음
6. 기존 게임 플로우(메뉴→문제→결과) 정상

## 배포 (Hermes 담당)
- private repo도 GitHub Pages 호스팅 가능 (이미 활성화됨). 설정 유지.
- `git add -A && commit && push`
- Pages가 새 버전 서빙 확인

## 역할
- Hermes: 계획, 암호화 스크립트 작성/실행, 키 생성, .gitignore, 검증, 배포
- OpenCode: index.html 잠금화면, game.js 복호화+로드 교체, sw.js 캐시 갱신, css 스타일
