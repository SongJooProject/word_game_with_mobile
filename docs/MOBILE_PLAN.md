# 모바일 버전 계획서 (Mobile PWA Plan)

> 목표: `word-game_with_mobile`(정적 웹 게임)을 폰에서 **앱처럼** 쓸 수 있는 모바일 최적화 + PWA 버전으로 만든다.
> Hermes가 계획/검증/배포, **OpenCode가 코드 작성**을 담당한다.

---

## 0. 저장소/배포 컨텍스트 (이미 처리됨)
- 이 폴더는 **독립 repo** (HERMES repo와 무관). 원격: `https://github.com/SongJooProject/word_game_with_mobile.git` (사용자 기존 repo)
- 빌드 없음: 순수 정적 (HTML/CSS/vanilla JS), `data/questions.json`을 `fetch`로 로드
- OpenCode 기본 모델: `opencode/deepseek-v4-flash-free` (`opencode.jsonc` 설정 완료)
- ⚠️ 정적 사이트라 `file://` 더블클릭으로는 `fetch` 차단 → 반드시 HTTP 서버 필요 (테스트/배포 모두)

## 1. 최종 결과물 (Definition of Done)
1. 폰 브라우저에서 `https://songjooproject.github.io/word-game_with_mobile/` 접속 시 **모바일 UI**로 표시
2. "홈 화면에 추가" 시 **앱 아이콘**으로 설치되고, 독립 실행(상단 주소줄 없음)
3. 오프라인에서도 최소 앱 셸(메뉴) 동작
4. 터치 타깃 ≥ 44px, iOS 입력 시 화면 줌 없음, 노치/안전영역 대응
5. 기존 데스크톱 UI는 깨지지 않음 (반응형 보존)

## 2. 파일 변경 목록 (OpenCode 담당)
| 파일 | 변경 |
|------|------|
| `index.html` | `<head>`에 PWA 메타 추가 (theme-color, apple-mobile-web-app-capable, manifest 링크), SW 등록 스크립트 |
| `css/style.css` | 모바일 UX 개선 (아래 §4), 기존 768px 미디어쿼리 확장 |
| `js/game.js` | SW 등록(`navigator.serviceWorker.register`), 모바일용 인터랙션(사이드바 닫기/터치) 보강 |
| `manifest.webmanifest` | 신규 — PWA 매니페스트 |
| `sw.js` | 신규 — 서비스 워커 (앱 셸 + JSON 캐시, 오프라인 폴백) |
| `.nojekyll` | 신규 — GitHub Pages가 Jekyll 처리 안 하도록 |
| `icons/icon-192.png`, `icons/icon-512.png` | **Hermes가 생성** (바이너리 자산) — OpenCode는 경로만 참조 |

## 3. PWA 요구사항 (OpenCode가 작성)
### manifest.webmanifest
```json
{
  "name": "법률 용어 게임",
  "short_name": "법률게임",
  "description": "형사소송법 등 법률 용어 학습 게임",
  "start_url": ".",
  "scope": ".",
  "display": "standalone",
  "orientation": "portrait",
  "background_color": "#f7f6f3",
  "theme_color": "#2383e2",
  "icons": [
    { "src": "icons/icon-192.png", "sizes": "192x192", "type": "image/png", "purpose": "any" },
    { "src": "icons/icon-512.png", "sizes": "512x512", "type": "image/png", "purpose": "any maskable" }
  ]
}
```

### sw.js (캐시 전략)
- `install`: 앱 셸(index.html, css/style.css, js/game.js, manifest, icon)을 `CACHE`에 프리캐시
- `fetch`:
  - `data/*.json` → stale-while-revalidate (캐시 우선, 백그라운드 갱신)
  - 정적 자산 → cache-first
  - 그 외 → network, 실패 시 캐시 폴백
- `activate`: 구버전 캐시 정리 (버전 상수 `CACHE_v1`)
- SW 등록은 `js/game.js` 최상단(또는 `window load`)에서 `navigator.serviceWorker` 지원 시에만

## 4. 모바일 UX 개선 명세 (OpenCode가 작성)
기존 노션 스타일 색상/디자인 유지(DESIGN.md 준수), **모바일에서만** 아래 적용:

1. **뷰포트/메타**
   - `<meta name="viewport" content="width=device-width, initial-scale=1, viewport-fit=cover">`
   - `<meta name="theme-color" content="#2383e2">`
   - `<meta name="apple-mobile-web-app-capable" content="yes">`
   - `<meta name="apple-mobile-web-app-status-bar-style" content="default">`

2. **안전영역(노치) 대응**
   - `.app`, `.header`, `.sidebar`, `.result-modal`에 `env(safe-area-inset-*)` 패딩 적용
   - iOS 상태바/홈 인디케이터 가림 방지

3. **터치 타깃**
   - 모든 버튼/메뉴아이템/섹션버튼 최소 높이 `44px`, 폰트 `1rem` 이상
   - `:hover` 의존 동작을 터치에도 동작하도록 (active 상태 추가)

4. **입력 필드(iOS 줌 방지)**
   - 빈칸 입력 `.inputs input` 폰트사이즈 **≥16px** (포커스 시 iOS 자동줌 차단)

5. **사이드바 → 풀스크린 메뉴**
   - 기존 768px 드로어 유지하되, 열릴 때 배경 오버레이(반투명) + 바깥 터치 시 닫힘
   - 메뉴 열릴 때 `body` 스크롤 잠금

6. **게임 진행 영역**
   - 진행률 바 sticky (상단 고정)
   - 문제 카드 풀폭, 선택지 버튼 세로 스택 + 세로 탭 영역 넓힘
   - 정답확인/다음 버튼 하단 고정(sticky footer) 또는 터치 쉽게 크게
   - 가상키보드 올라올 때 레이아웃 깨짐 방지 (`100dvh` 사용 권장)

7. **결과 모달**
   - 모바일에서 풀스크린 카드로 표시

8. **스크롤/바운스**
   - 불필요한 바디 바운스 억제, 게임 영역만 스크롤

9. **애니메이션** 기존 유지(0.3s 슬라이드 등), 모바일에서 과도한 모션 자제

## 5. 검증 (Hermes 담당, OpenCode 빌드 직후)
1. 로컬 서버 기동: `python -m http.server 8000` (이 폴더 루트)
2. `curl -s localhost:8000/data/questions.json | head` → JSON 로드 확인
3. `curl -s localhost:8000/manifest.webmanifest` → 200
4. `curl -s localhost:8000/sw.js` → 200, MIME 가능
5. 기존 `python scripts/auto_test.py` 통과 확인 (파일구조/문법)
6. 브라우저(데스크톱 폭 375px 에뮬)로 메뉴→게임→결과 플로우 동작 확인
7. 콘솔 에러(특히 SW 등록, fetch) 없음 확인

## 6. 배포 (Hermes 담당 — gh 인증 필요)
1. `gh auth login` (사용자 수행, 또는 토큰) — 현재 gh 미로그인 상태
2. 기존 repo `SongJooProject/word_game_with_mobile` 가정 (사용자 확인). 없으면 `gh repo create SongJooProject/word_game_with_mobile --public`
3. `git add -A && git commit -m "feat: mobile PWA (responsive + manifest + service worker)"`
4. `git push -u origin master`
5. GitHub Pages 설정: Settings → Pages → Source = `master` / root → `.nojekyll` 있음
6. URL 공유: `https://songjooproject.github.io/word_game_with_mobile/`
7. 폰에서 접속 → "홈 화면에 추가" → 앱 설치 확인

## 7. 역할 분담
- **Hermes**: 계획 작성, 아이콘 PNG 생성, 로컬 서버 검증, gh 배포, 최종 확인
- **OpenCode**: §2/§3/§4 의 실제 코드(text 파일) 작성. 바이너리(아이콘)는 생성하지 않음
