# AGENTS.md - word-game 프로젝트 가이드라인

## 참고 문서
작업 전 아래 문서를 반드시 확인하세요.

- 디자인 사양: `DESIGN.MD` — UI/UX 디자인 규칙이 담겨 있습니다
- 코딩 규칙: 아래 코딩 컨벤션 섹션

## 프로젝트 개요
- **이름**: word-game
- **언어**: Python 3.10+
- **목적**: 뻥뚜리 문제 생성 및 파이썬 게임

## 프로젝트 구조
```
word-game/
├── AGENTS.md
├── pyproject.toml
├── src/
│   └── word_game/
│       ├── __init__.py
│       └── main.py
├── tests/
│   └── __init__.py
├── data/
│   └── words.json
└── docs/
```

## 코딩 컨벤션
- PEP 8 준수
- 라인 길이: 88자
- 따옴표: 더블 쿼트 (")
- 들여쓰기: 4칸

## 검증 시스템
```bash
ruff check .           # 린팅 검사
python -m pytest       # 테스트 실행
```

## 에이전트 역할

### design-manager
- **역할**: 디자인 사양 관리
- **파일**: `DESIGN.MD`
- **동작**: UI 변경 시 DESIGN.MD 업데이트

### general
- **역할**: 일반적인 작업 수행
- **사용 시점**: 복잡한 작업, 여러 파일 수정 필요 시
