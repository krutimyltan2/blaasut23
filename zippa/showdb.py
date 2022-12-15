import sqlite3

dbfile = "exposed/users.db"

if __name__ == "__main__":
    con = sqlite3.connect(dbfile)
    cur = con.cursor()
    cur.execute("SELECT * FROM users;")
    f = cur.fetchall()
    for r in f:
        print(r)