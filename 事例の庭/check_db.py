import sqlite3

 

conn = sqlite3.connect("cases.db")

cur = conn.cursor()

 

for row in cur.execute("SELECT id, title FROM cases"):

    print(row)

 

conn.close()

 