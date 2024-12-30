import sqlite3

conn = sqlite3.connect('movify.db')
c = conn.cursor()
mov_list = c.execute("SELECT * FROM watchlist").fetchall()
print(mov_list)