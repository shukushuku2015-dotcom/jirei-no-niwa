import sqlite3

 

conn = sqlite3.connect("cases.db")

cur = conn.cursor()

 

cur.execute("SELECT COUNT(*) FROM cases")

count = cur.fetchone()[0]

 

print("cases テーブルの件数:", count)

 

conn.close()

 