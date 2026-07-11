# DEPLOY_STATE.md — 배포 상태 (OpenCode/에이전트 필독)

> 이 파일은 **코드가 아님**. 배포/인프라 상태를 적은 메모다.
> OpenCode를 이 repo에서 돌리기 전에 **반드시 먼저 읽을 것**.

## 현재 상태 (2026-07-11 기준)
- **repo visibility**: `public` (SongJooProject/word_game_with_mobile)
  - ⚠️ 과거 private로 바꿨다가 **GitHub Pages가 private repo에서 비활성화**되어
    사이트 404 뜸 → 다시 public으로 복원함. private로 다시 바꾸면 Pages 죽음.
- **GitHub Pages**: 활성화됨. Source = `master` / root. `.nojekyll` 있음.
  - URL: https://songjooproject.github.io/word_game_with_mobile/
- **보안**: 문제 DATA는 암호화 + 앱 입장 비밀번호로 보호 (아래 참조)

## 보안 모델 (중요)
- `data/questions.json`(평문)은 **git에 커밋되지 않음** (.gitignore에 있음, 로컬에만 임시 존재)
- 배포되는 건 `data/questions.enc` (암호문)
- **암호화**: Fernet, 키 = `SHA-256("songjoo")` (32바이트 → signing16 + enc16)
- **앱 입장 비밀번호**: `songjoo` (index.html 잠금화면)
- 비밀번호 모르면 `questions.enc` 복호 불가 → 문제 내용 열람 불가
- 관련 파일: `scripts/encrypt_questions.py`, `js/game.js`(fernetDecrypt), `index.html`(lock screen)

## DB/문제 갱신 워크플로우
1. 엑셀 → `python scripts/convert_excel_to_json.py` → `data/questions.json` (평문, 로컬임시)
2. `python scripts/encrypt_questions.py` → `data/questions.enc` 갱신
3. `git add -A && git commit && git push`
4. Pages 자동 갱신 (수십 초~1분). 폰에선 앱 새로고침.

## OpenCode 위임 시 주의
- repo visibility/Pages 설정은 **건드리지 말 것** (다시 깨짐)
- 코드 수정 시 `questions.json` 평문을 repo에 커밋하지 않도록 주의
- 새로운 보안 로직 추가 시 기존 Fernet/비밀번호 방식과 호환 유지

## OpenCode 위임 표준 프롬프트 (Hermes가 항상 포함)
위임할 때 아래 문구를 프롬프트 끝에 반드시 붙일 것:
> "작업 중 결정/배포/보안/DB갱신/에러해결/설정변경/학습이 있으면 **세션 끝나기 전에 무조건 LLM Wiki에 자동 Ingest**하라. 체크리스트: (1) 자동 대상 다뤘는가? (2) @llm-wiki 호출해 source/entity/synthesis 생성 (3) index.md/log.md/overview.md 갱신. 갱신 안 됐으면 세션 종료 금지. wiki 경로/규칙은 ~/.config/opencode/AGENTS.md 참조."
