# 📚 법률 용어 게임 (모바일 PWA)

> 형사소송법 법률 용어 퀴즈 게임 — 폰에서 앱처럼 사용하는 **모바일 PWA** 버전

![PWA](https://img.shields.io/badge/PWA-설치가능-blue)
![Static](https://img.shields.io/badge/stack-HTML%2FCSS%2FJS-orange)
![Encrypt](https://img.shields.io/badge/보안-Fernet%20암호화-green)
![License](https://img.shields.io/badge/license-Private--use-red)

---

## ✨ 특징

- 📱 **모바일 최적화** — 안전영역, 터치 타깃, 사이드바 오버레이
- 📲 **PWA 설치** — 홈 화면에 추가해서 앱처럼 사용, 오프라인 캐시 지원
- 🔒 **문제 DATA 암호화** — Fernet 암호화 + 입장 비밀번호로 보호
- 🔤 **줄바꿈 지원** — 엑셀 Alt+Enter 줄바꿈이 문제 화면에 그대로 반영
- 🔄 **자동 갱신** — 배포 시 설치된 폰에도 최신 버전이 자동 반영
- 🎯 **두 가지 유형** — 선택형(type1) / 빈칸형(type2), 섹션별·전체 풀이
- 📊 **학습 관리** — 점수, 정답률, 소요 시간 표시

## 🎮 게임 구성

- **과목**: 형사소송법 (1과목)
- **챕터**: 13개 (공소제기, 공판절차/범위, 증거, 재판, 상소, 비상구제절차, 관할 및 제척기피, 피고인 및 변호인, 소송행위, 수사의 단서, 임의수사, 대인적 강제수사, 대물적 강제수사)
- **문제 수**: **711문제** (선택형 353 + 빈칸형 358)

## 🚀 사용 방법

1. 모바일 브라우저(Chrome/Safari)로 접속
2. 입장 비밀번호 입력 (게임 설명서/공유 시 별도 안내)
3. 과목 → 챕터/섹션 선택 → 게임 시작
4. 홈 화면 추가로 설치하면 앱처럼 사용 가능

> 💡 브라우저는 캐시를 자동 갱신하므로, 배포된 새 문제는 별도 조작 없이 반영됩니다.

## 🛠 기술 스택

| 영역 | 기술 |
|------|------|
| 프론트엔드 | 바닐라 HTML / CSS / JavaScript |
| 배포 | GitHub Pages (정적 호스팅) |
| 앱 형태 | PWA (Service Worker + Manifest) |
| 보안 | Fernet 대칭 암호화 (문제 DATA), 입장 비밀번호 |
| 데이터 | Excel → JSON → 암호화(`.enc`) 파이프라인 |

## 📁 프로젝트 구조

```
word-game_with_mobile/
├── index.html              # 메인 페이지 (잠금화면 + 게임)
├── css/style.css           # 모바일 최적화 스타일
├── js/game.js              # 게임 로직 (Fernet 복호화 포함)
├── sw.js                   # Service Worker (오프라인 캐시 + 자동갱신)
├── manifest.webmanifest    # PWA 매니페스트
├── data/
│   └── questions.enc       # 암호화된 문제 DATA (배포본)
├── db/형사소송법/          # 원본 문제 엑셀 (다중 파일)
├── scripts/
│   ├── convert_excel_to_json.py  # 엑셀 → JSON 변환
│   └── encrypt_questions.py      # JSON → Fernet 암호화
└── DEPLOY_STATE.md         # 배포/보안 상태 문서 (OpenCode 컨텍스트)
```

## 🔄 데이터 갱신 워크플로

문제 DB를 수정한 경우:

```bash
# 1. 엑셀(DB_*.xlsx)을 db/형사소송법/ 에 넣기
# 2. 평문 JSON 생성
python scripts/convert_excel_to_json.py
# 3. 암호화 (questions.enc 갱신)
python scripts/encrypt_questions.py
# 4. 커밋 & 푸시 → GitHub Pages 자동 갱신
git add -A && git commit && git push
```

> ⚠️ `data/questions.json`(평문)은 `.gitignore` 대상 — **절대 커밋하지 마세요.**
> 배포되는 건 암호문 `questions.enc` 뿐입니다.

## 🔒 보안 모델

- 문제 DATA는 **Fernet 암호화**되어 `questions.enc`로만 배포
- 앱 입장 시 비밀번호로 복호화 → 비밀번호 모르면 문제 내용 열람 불가
- 저장소는 공개(public)이나, GitHub Pages가 private repo에서 비활성화되므로 공개 유지
- repo visibility / GitHub Pages 설정은 **임의로 변경 금지** (Pages가 죽음)

## 📝 라이선스

개인 학습/비영리 용도. 상업적 이용 금지.
