import sqlite3

conn = sqlite3.connect("db/legal_terms.db")
cursor = conn.cursor()

cursor.execute("SELECT article_no, title, content FROM law_articles WHERE law_name LIKE '%형사소송%' ORDER BY CAST(SUBSTR(article_no, 2) AS INTEGER)")
articles = cursor.fetchall()

with open("articles_list.txt", "w", encoding="utf-8") as f:
    for no, title, content in articles:
        f.write(f"{no} | {title}\n")

conn.close()
