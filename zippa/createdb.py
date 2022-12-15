import sqlite3
import hashlib

kakburk = "exposed/kakburk.zip"
admin_username = "admin"
dbfile = "exposed/users.db"
usersfile = "users.txt"
flagfile = "flagga.txt"

def get_tables(con):
    cur = con.cursor()
    cur.execute("SELECT name FROM sqlite_master WHERE type='table';")
    f = cur.fetchall()
    return [fx[0] for fx in f]

def clear_database(con):
    tables = get_tables(con)
    cur = con.cursor()
    for t in tables:
        cur.execute("DROP TABLE {}".format(t))
        con.commit()

def msha1(s):
    shastr = hashlib.sha1(s.encode()).hexdigest()
    return "sha1:"+("0"*((160//4)-len(shastr)))+shastr

def init_user_table(con):
    cur = con.cursor()
    cur.execute("CREATE TABLE users(username, pw_hash)")
    f = open(usersfile, "r")
    for line in f.readlines():
        if line[-1] == "\n":
            line = line[:-1]
        sline = line.split(",")
        uname = sline[0]
        pw = sline[1]
        pw_hash = msha1(pw)
        comm = "INSERT INTO users(username, pw_hash) VALUES (\"{}\", \"{}\")".format(uname, pw_hash)
        print(comm)
        cur.execute(comm)
    con.commit()

con = sqlite3.connect(dbfile)
print(get_tables(con))
clear_database(con)
print(get_tables(con))
init_user_table(con)
con.close()