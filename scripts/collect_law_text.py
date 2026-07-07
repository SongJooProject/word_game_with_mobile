import requests
import json
import sqlite3
import re
from pathlib import Path


class LawTextCollector:
    BASE_URL = "http://www.law.go.kr/DRF"
    
    def __init__(self, oc_id="skagurwn", db_path="db/legal_terms.db"):
        self.oc_id = oc_id
        self.db_path = db_path
    
    def get_law_text(self, mst):
        url = f"{self.BASE_URL}/lawService.do"
        params = {"OC": self.oc_id, "target": "law", "type": "JSON", "MST": mst}
        r = requests.get(url, params=params, timeout=30)
        r.encoding = 'utf-8'
        return r.json()
    
    def parse_articles(self, data):
        articles = []
        if "법령" not in data:
            return articles
        
        law_data = data["법령"]
        basic = law_data.get("기본정보", {})
        law_name = basic.get("법령명_한글", "")
        
        jo_data = law_data.get("조문", {})
        jo_list = jo_data.get("조문단위", [])
        
        for jo in jo_list:
            no = jo.get("조문번호", "")
            title = jo.get("조문제목", "")
            content = jo.get("조문내용", "")
            
            if no and content:
                articles.append({
                    "law_name": law_name,
                    "article_no": f"제{no}조",
                    "title": title or "",
                    "content": content[:2000]
                })
        
        return articles
    
    def save_to_db(self, articles):
        conn = sqlite3.connect(self.db_path)
        cursor = conn.cursor()
        
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS law_articles (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                law_name TEXT NOT NULL,
                article_no TEXT NOT NULL,
                title TEXT,
                content TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        
        saved = 0
        for article in articles:
            cursor.execute("""
                INSERT OR REPLACE INTO law_articles 
                (law_name, article_no, title, content) 
                VALUES (?, ?, ?, ?)
            """, (article["law_name"], article["article_no"], article["title"], article["content"]))
            saved += 1
        
        conn.commit()
        conn.close()
        return saved
    
    def collect(self, law_name, mst):
        print(f"\n{'='*50}")
        print(f"법령 수집: {law_name} (MST: {mst})")
        print(f"{'='*50}")
        
        print("1. 법령 본문 조회 중...")
        law_text = self.get_law_text(mst)
        
        print("2. 조문 파싱 중...")
        articles = self.parse_articles(law_text)
        print(f"   파싱된 조문: {len(articles)}개")
        
        print("3. DB 저장 중...")
        saved = self.save_to_db(articles)
        print(f"   저장된 조문: {saved}개")
        
        print("\n[샘플 조문]")
        for article in articles[:5]:
            print(f"  {article['article_no']}: {article['content'][:80]}...")
        
        return articles


def main():
    collector = LawTextCollector()
    collector.collect("형사소송법", "280441")


if __name__ == "__main__":
    main()
