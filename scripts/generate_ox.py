"""
형사소송법 OX 문제 생성 스크립트
각 조문/항의 실제 내용을 활용
"""

import sqlite3
import json
import random
import re


def load_articles():
    conn = sqlite3.connect("db/legal_terms.db")
    cursor = conn.cursor()
    cursor.execute("""
        SELECT article_no, title, content 
        FROM law_articles 
        WHERE law_name LIKE '%형사소송%' 
        AND length(content) > 50
    """)
    articles = cursor.fetchall()
    conn.close()
    return articles


def clean_content(content):
    """조문 내용 정리"""
    # HTML 태그 제거
    content = re.sub(r'<[^>]+>', '', content)
    # 불필요한 공백 제거
    content = re.sub(r'\s+', ' ', content).strip()
    return content


def extract_key_info(content):
    """조문에서 핵심 정보 추출"""
    info = {
        "has_time": bool(re.search(r'\d+일|\d+시간|\d+개월|\d+년', content)),
        "has_person": any(p in content for p in ["검사", "사법경찰관", "피의자", "피고인", "법원", "변호인"]),
        "has_action": any(a in content for a in ["할 수 있다", "하여야 한다", "하지 아니한다", "할 수 없다"]),
        "has_condition": any(c in content for c in ["경우", "때에는", "할 때", "条件"]),
    }
    return info


def create_ox_from_article(article_no, title, content):
    """조문 내용에서 OX 문제 생성"""
    questions = []
    content = clean_content(content)
    
    if len(content) < 30:
        return questions
    
    # 패턴 1: 제목 확인 문제
    if title:
        questions.append({
            "question": f"형사소송법 {article_no}는 '{title}'에 관한 규정이다.",
            "answer": "O",
            "explanation": f"{article_no}의 제목은 '{title}'입니다.",
            "article": article_no,
            "type": "title"
        })
    
    # 패턴 2: "~한다" 문장 → O 문제
    if "한다" in content:
        sentences = content.split(".")
        for sent in sentences:
            if "한다" in sent and len(sent) > 30:
                questions.append({
                    "question": f"형사소송법 {article_no}에 따르면 {sent.strip()[:80]}.",
                    "answer": "O",
                    "explanation": "조문 원문에 명시된 내용입니다.",
                    "article": article_no,
                    "type": "content_o"
                })
                break
    
    # 패턴 3: "~할 수 없다" 문장 → X 문제
    if "할 수 없다" in content or "하지 아니한다" in content:
        questions.append({
            "question": f"형사소송법 {article_no}에 따르면, 수사기관은 이를 위반할 수 있다.",
            "answer": "X",
            "explanation": "조문에서 금지하고 있는 행위입니다.",
            "article": article_no,
            "type": "content_x"
        })
    
    # 패턴 4: 시간/기간 정보 → O 문제
    time_match = re.search(r'(\d+일|\d+시간|\d+개월|\d+년)', content)
    if time_match:
        time_info = time_match.group(1)
        questions.append({
            "question": f"형사소송법 {article_no}에 따르면 이는 {time_info} 이내에 이루어져야 한다.",
            "answer": "O",
            "explanation": f"조문에 {time_info} 기간이 명시되어 있습니다.",
            "article": article_no,
            "type": "time_o"
        })
    
    return questions


def main():
    print("=" * 60)
    print("형사소송법 OX 문제 생성")
    print("=" * 60)
    
    articles = load_articles()
    print(f"\n조문 수: {len(articles)}개")
    
    all_questions = []
    
    for article_no, title, content in articles:
        qs = create_ox_from_article(article_no, title, content)
        all_questions.extend(qs)
    
    # 랜덤 셔플
    random.shuffle(all_questions)
    
    # 30개로 제한
    questions = all_questions[:30]
    
    print(f"생성된 문제: {len(questions)}개")
    
    output = {
        "subject": "형사소송법",
        "type": "ox",
        "questions": questions
    }
    
    with open("data/ox_questions.json", "w", encoding="utf-8") as f:
        json.dump(output, f, ensure_ascii=False, indent=2)
    
    print(f"\n저장 완료: data/ox_questions.json")
    
    print("\n[샘플 문제]")
    for q in questions[:5]:
        print(f"  Q: {q['question'][:80]}...")
        print(f"  A: {q['answer']}")
        print()


if __name__ == "__main__":
    main()
