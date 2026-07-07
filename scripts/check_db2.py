import sqlite3

conn = sqlite3.connect("db/legal_terms.db")
cursor = conn.cursor()

cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
tables = cursor.fetchall()
print("테이블:", tables)

for table in tables:
    cursor.execute(f"SELECT COUNT(*) FROM {table[0]}")
    count = cursor.fetchone()[0]
    print(f"  {table[0]}: {count}개")

conn.close()
