import sqlite3

conn = sqlite3.connect("db/legal_terms.db")
cursor = conn.cursor()

# 중복 조문 확인
cursor.execute("SELECT article_no, COUNT(*) as cnt FROM law_articles WHERE law_name LIKE '%형사소송%' GROUP BY article_no HAVING cnt > 1 ORDER BY cnt DESC")
dups = cursor.fetchall()

with open("dup_check.txt", "w", encoding="utf-8") as f:
    f.write("총 조문 수: 643개\n")
    f.write(f"고유 조문 수: {643 - sum(c-1 for _, c in dups)}개\n")
    f.write(f"중복된 조문: {len(dups)}개\n\n")

    f.write("[중복 조문 목록]\n")
    for no, cnt in dups[:20]:
        f.write(f"  {no}: {cnt}개\n")

    # 조문별 항 확인
    f.write("\n\n[조문별 항 수 예시]\n")
    cursor.execute("SELECT article_no, title, content FROM law_articles WHERE article_no = '제200조' AND law_name LIKE '%형사소송%'")
    for no, title, content in cursor.fetchall():
        f.write(f"  {no} | {title}\n")

conn.close()
