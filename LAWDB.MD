# LAWDB.MD - 법령용어 데이터베이스 관리

## 개요
국가법령정보센터 API를 통한 법령용어 수집 및 관리 규칙

## 할루시네이션 방지 규칙
- 법령용어는 국가법령정보센터 API에서만 수집
- 임의로 법령용어를 생성하지 않음
- 수집된 데이터는 전문가 검수 후 문제 생성에 사용
- API 인증값은 `.env` 파일에 저장 (git 제외)

## API 정보
- **URL**: http://www.law.go.kr/DRF/lawSearch.do
- **target**: lstrm (법령용어)
- **인증값**: test (개발용) 또는 공공데이터포털 발급 키
- **문서**: https://open.law.go.kr/LSO/openApi/guideResult.do?htmlName=lsTrmListGuide

## 수집 스크립트
- **위치**: `scripts/collect_legal_terms.py`
- **실행**: `python scripts/collect_legal_terms.py`
- **결과**: `data/legal_terms.json`

## 데이터 구조
```json
{
  "name": "법령용어명",
  "definition": "법령용어정의",
  "category": "법령종류코드"
}
```

## 수집 대상 키워드
### 민법
- 계약, 손해배상, 소멸시효, 보증, 사무관리

### 형법
- 고의, 과실, 정당방위, 미수, 공범

### 형사소송법
- 체포, 구속, 영장, 기소, 공판심리

### 상법
- 상인, 회사, 상표, 보험, 선하증권

### 노동법
- 근로계약, 해고, 산재, 고용보험, 단결권

### 헌법
- 기본권, 헌법, 국회, 대통령, 권력분립
