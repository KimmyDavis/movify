import sqlite3

def get_list(user_id):
    conn = sqlite3.connect('movify.db')
    cur = conn.cursor()
    mov_list = cur.execute(
        "SELECT movie_id FROM watchlist WHERE user_id = ? ORDER BY sn DESC", (user_id,)
    ).fetchall()
    if not mov_list:
        return None
    return [i[0] for i in mov_list]



def remove_item(user_id, movie_id):
    conn = sqlite3.connect('movify.db')
    cur = conn.cursor()
    cur.execute(
            "DELETE FROM watchlist WHERE user_id = ? AND movie_id = ?", (user_id, movie_id)
        )
    conn.commit()

def create(user_id, movie_id):
    conn = sqlite3.connect('movify.db')
    cur = conn.cursor()
    already_exist = cur.execute(
        "SELECT * FROM watchlist WHERE user_id = ? AND movie_id = ?", 
        (user_id, movie_id)).fetchone()
    if not already_exist:
        cur.execute(
            "INSERT INTO watchlist (user_id, movie_id) "
            "VALUES (?, ?)",
            (user_id, movie_id)
        )
        conn.commit()
