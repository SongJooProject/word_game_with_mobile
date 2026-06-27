# LAWDB.MD - 법령용어 데이터베이스 관리

## 개요
국가법령정보센터 API를 통한 법령용어 수집 및 관리 규칙

## 할루시네이션 방지 규칙
- 법령용어는 국가법령정보센터 API에서만 수집
- 임의로 법령용어를 생성하지 않음
- 수집된 데이터는 전문가 검수 후 문제 생성에 사용
- API 인증값은 `.env` 파일에 저장 (git 제외)

## DB 구조
```
db/
├── legal_terms.db      # SQLite 데이터베이스
├── schema.sql          # DB 스키마
└── create_db.bat       # DB 생성 스크립트 (Windows)
```

## DB 생성 방법
1. `db/create_db.bat` 더블클릭
2. 또는 터미널에서: `python scripts/init_db.py`

## 테이블 구조

### subjects (주제)
| 컬럼 | 타입 | 설명 |
|------|------|------|
| id | INTEGER | 기본키 |
| name | TEXT | 주제명 (예: 형사소송법) |
| description | TEXT | 설명 |
| created_at | TIMESTAMP | 생성일시 |

### keywords (키워드)
| 컬럼 | 타입 | 설명 |
|------|------|------|
| id | INTEGER | 기본키 |
| subject_id | INTEGER | 주제 ID (외래키) |
| term | TEXT | 법률 용어 |
| definition | TEXT | 정의 |
| source | TEXT | 출처 |
| is_verified | INTEGER | 검수 여부 (0/1) |
| created_at | TIMESTAMP | 생성일시 |

### questions (문제)
| 컬럼 | 타입 | 설명 |
|------|------|------|
| id | INTEGER | 기본키 |
| subject_id | INTEGER | 주제 ID (외래키) |
| question_type | TEXT | 문제 유형 (ox/blank) |
| content | TEXT | 문제 내용 |
| answer | TEXT | 정답 |
| hint | TEXT | 힌트 |
| is_verified | INTEGER | 검수 여부 (0/1) |
| created_at | TIMESTAMP | 생성일시 |

## API 정보
- **URL**: http://www.law.go.kr/DRF/lawSearch.do
- **target**: lstrm (법령용어)
- **인증값**: test (개발용) 또는 공공데이터포털 발급 키
- **문서**: https://open.law.go.kr/LSO/openApi/guideResult.do?htmlName=lsTrmListGuide

## 수집 스크립트
- **위치**: `scripts/collect_legal_terms.py`
- **실행**: `python scripts/collect_legal_terms.py`
- **결과**: `data/legal_terms.json`

## 키워드 수집 대상 (형사소송법)
### 기본 개념
- 형사소송, 피의자, 피고인, 고소인, 고발인

### 수사절차
- 수사, 고소, 고발, 진술거부권, 변호인

### 체포·구속
- 체포, 구속, 영장, 체포영장, 구속영장, 영장주의

### 기소
- 기소, 기소독점, 공소장, 공소제기

### 재판절차
- 공판절차, 공판심리주의, 변론, 선고, 판결

### 판결 유형
- 유죄판결, 무죄판결, 공소기각, 면소

### 기타
- 무죄추정원칙, 검증, 증거, 자백, 진술
- 약식절차, 약식명령, 즉시항고, 항소, 상고
- 공소시효, 형의 집행, 집행유예, 선고유예
