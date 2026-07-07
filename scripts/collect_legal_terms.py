"""
국가법령정보센터 법령용어 수집 에이전트
API 문서: https://open.law.go.kr/LSO/openApi/guideResult.do?htmlName=lsTrmListGuide
"""

import json
import time
import requests
from typing import Optional


class LegalTermCollector:
    """법령용어 수집 클래스"""

    BASE_URL = "http://www.law.go.kr/DRF/lawSearch.do"

    def __init__(self, oc_id: str = "test"):
        """
        초기화

        Args:
            oc_id: API 인증값 (기본값: test)
        """
        self.oc_id = oc_id
        self.session = requests.Session()

    def fetch_terms(
        self,
        query: Optional[str] = None,
        display: int = 20,
        page: int = 1,
        gana: Optional[str] = None,
        dic_knd_cd: Optional[int] = None
    ) -> dict:
        """
        법령용어 목록 조회

        Args:
            query: 검색어
            display: 결과 개수 (max=100)
            page: 페이지 번호
            gana: 사전식 검색 (ga, na, da...)
            dic_knd_cd: 법령 종류 코드 (법령: 010101, 행정규칙: 010102)

        Returns:
            API 응답 데이터
        """
        params = {
            "OC": self.oc_id,
            "target": "lstrm",
            "type": "JSON",
            "display": display,
            "page": page
        }

        if query:
            params["query"] = query
        if gana:
            params["gana"] = gana
        if dic_knd_cd:
            params["dicKndCd"] = dic_knd_cd

        try:
            response = self.session.get(self.BASE_URL, params=params, timeout=10)
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            print(f"API 요청 실패: {e}")
            return {}

    def fetch_term_detail(self, query: str) -> dict:
        """
        법령용어 본문 조회

        Args:
            query: 법령용어명

        Returns:
            상세 데이터
        """
        url = "http://www.law.go.kr/DRF/lawService.do"
        params = {
            "OC": self.oc_id,
            "target": "lstrm",
            "type": "JSON",
            "query": query
        }

        try:
            response = self.session.get(url, params=params, timeout=10)
            response.raise_for_status()
            return response.json()
        except requests.RequestException as e:
            print(f"API 요청 실패: {e}")
            return {}

    def collect_all_terms(self, max_pages: int = 10) -> list:
        """
        모든 법령용어 수집

        Args:
            max_pages: 최대 페이지 수

        Returns:
            법령용어 목록
        """
        all_terms = []

        for page in range(1, max_pages + 1):
            print(f"페이지 {page} 수집 중...")
            data = self.fetch_terms(display=100, page=page)

            if not data or "LawSearch" not in data:
                break

            terms = data["LawSearch"].get("law", [])
            if not terms:
                break

            all_terms.extend(terms)
            time.sleep(0.5)  # API 부하 방지

        return all_terms

    def search_by_keyword(self, keyword: str) -> list:
        """
        키워드로 법령용어 검색

        Args:
            keyword: 검색 키워드

        Returns:
            검색 결과 목록
        """
        data = self.fetch_terms(query=keyword, display=100)

        if not data or "LawSearch" not in data:
            return []

        return data["LawSearch"].get("law", [])


def collect_for_game(keywords: list, output_file: str = "data/legal_terms.json"):
    """
    게임용 법령용어 수집

    Args:
        keywords: 검색할 키워드 목록
        output_file: 출력 파일 경로
    """
    collector = LegalTermCollector()
    all_terms = []

    for keyword in keywords:
        print(f"'{keyword}' 검색 중...")
        terms = collector.search_by_keyword(keyword)
        all_terms.extend(terms)
        time.sleep(1)

    # 중복 제거
    unique_terms = {}
    for term in all_terms:
        term_name = term.get("법령용어명", "")
        if term_name and term_name not in unique_terms:
            unique_terms[term_name] = {
                "name": term_name,
                "definition": term.get("법령용어상세검색", ""),
                "category": term.get("법령종류코드", "")
            }

    result = list(unique_terms.values())

    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(result, f, ensure_ascii=False, indent=2)

    print(f"총 {len(result)}개 법령용어 저장 완료: {output_file}")
    return result


if __name__ == "__main__":
    # 법률 주제별 키워드
    keywords = [
        "계약", "손해배상", "소멸시효", "보증",
        "고의", "과실", "정당방위", "미수",
        "체포", "구속", "영장", "기소",
        "상인", "회사", "상표", "보험",
        "근로계약", "해고", "산재", "고용보험",
        "기본권", "헌법", "국회", "대통령"
    ]

    collect_for_game(keywords)
