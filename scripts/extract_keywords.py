"""
형사소송법 조문에서 A/B등급 키워드 추출 스크립트
"""

import sqlite3


# A등급: 조문 핵심 용어 (빈칸 필수)
A_GRADE_KEYWORDS = {
    # 일반 규칙
    "영장", "체포", "구속", "압수", "수색", "검증", "감정",
    "피의자", "피고인", "피해자", "증인", "감정인", "통역인",
    "검찰", "검사", "사법경찰관", "수사관",
    "공소", "공소제기", "공소장", "공소취소",
    "판결", "선고", "유죄", "무죄", "실형", "집행유예", "벌금",
    "구금", "석방", "보석", "구금장소",
    "증거", "증거능력", "증거조사", "자백", "진술",
    "심리", "공판", "변론", "항고", "항소", "상고",
    "정지", "취소", "철회",
    "기소", "불기소", "약식기소",
    "영장청구", "사후승인", "구속영장", "체포영장",
    "수사", "수사개시", "수사종결",
}

# B등급: 판례 용어 (빈칸 가능)
B_GRADE_KEYWORDS = {
    "위법수집증거", "위법수집증거배제", "자백강박", "묵비권",
    "진술거부권", "변호인접견", "변호인선임",
    "피의자신문", "피의자조서", "증인신문",
    "압수수색영장", "별건영장", "일반영장",
    "구속적부심사", "구속연장", "구속기간",
    "공소장일본주의", "공소장변경",
    "피고인출석", "불출석심리",
    "증거보전", "증거보전명령",
    "박탈", "권리박탈", "절차적박탈",
}


def extract_keywords():
    """DB에서 조문을 읽어 키워드를 추출"""
    conn = sqlite3.connect("db/legal_terms.db")
    cursor = conn.cursor()

    cursor.execute(
        "SELECT article_no, title, content "
        "FROM law_articles WHERE law_name LIKE '%형사소송%'"
    )
    articles = cursor.fetchall()

    results = {"A": [], "B": []}

    for article_no, title, content in articles:
        text = f"{title} {content}"

        # A등급 키워드 검출
        for keyword in A_GRADE_KEYWORDS:
            if keyword in text:
                results["A"].append({
                    "article": article_no,
                    "title": title,
                    "keyword": keyword,
                    "context": extract_context(text, keyword)
                })

        # B등급 키워드 검출
        for keyword in B_GRADE_KEYWORDS:
            if keyword in text:
                results["B"].append({
                    "article": article_no,
                    "title": title,
                    "keyword": keyword,
                    "context": extract_context(text, keyword)
                })

    conn.close()
    return results


def extract_context(text, keyword, window=50):
    """키워드 주변 문맥 추출"""
    idx = text.find(keyword)
    if idx == -1:
        return ""
    start = max(0, idx - window)
    end = min(len(text), idx + len(keyword) + window)
    return text[start:end]


def main():
    print("=" * 60)
    print("형사소송법 키워드 추출")
    print("=" * 60)

    results = extract_keywords()

    print(f"\n[A등급 키워드] ({len(results['A'])}개)")
    for r in results["A"][:20]:
        print(f"  - {r['keyword']} ({r['article']})")

    print(f"\n[B등급 키워드] ({len(results['B'])}개)")
    for r in results["B"][:20]:
        print(f"  - {r['keyword']} ({r['article']})")

    # 파일 저장
    with open("data/keywords.json", "w", encoding="utf-8") as f:
        import json
        json.dump(results, f, ensure_ascii=False, indent=2)

    print("\n결과 저장: data/keywords.json")


if __name__ == "__main__":
    main()
