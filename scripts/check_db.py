import sqlite3

conn = sqlite3.connect("db/legal_terms.db")
cursor = conn.cursor()

# 전체 조문 수
cursor.execute("SELECT COUNT(*) FROM law_articles")
total = cursor.fetchone()[0]
print(f"전체 조문 수: {total}개")

# 형사소송법 조문 수
cursor.execute("SELECT COUNT(*) FROM law_articles WHERE law_name LIKE '%형사소송%'")
crim = cursor.fetchone()[0]
print(f"형사소송법 조문 수: {crim}개")

# 샘플
cursor.execute("SELECT article_no, title FROM law_articles WHERE law_name LIKE '%형사소송%' LIMIT 10")
print("\n[샘플]")
for row in cursor.fetchall():
    print(f"  - {row[0]}: {row[1]}")

conn.close()
