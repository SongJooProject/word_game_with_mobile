import sqlite3

conn = sqlite3.connect("db/legal_terms.db")
cursor = conn.cursor()

cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
tables = cursor.fetchall()

result = []
for table in tables:
    cursor.execute(f"SELECT COUNT(*) FROM {table[0]}")
    count = cursor.fetchone()[0]
    result.append(f"{table[0]}: {count}")

conn.close()

with open("db_check_result.txt", "w", encoding="utf-8") as f:
    f.write("\n".join(result))
