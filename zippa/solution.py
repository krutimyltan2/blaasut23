import pyzipper
import sqlite3

kakburk = "exposed/kakburk.zip"
dbfile = "exposed/users.db"
flagfile = "flagga.txt"

def get_admin_hash(db):
    con = sqlite3.connect(db)
    cur = con.cursor()
    cur.execute("SELECT pw_hash FROM users WHERE username = 'admin';")
    f = cur.fetchall()
    if len(f) == 0:
        return None
    else:
        return f[0][0]

def hash_to_pw(h):
    return bytes.fromhex(h)

with pyzipper.AESZipFile(kakburk) as zf:
    admin_hash = get_admin_hash(dbfile)
    print("admin_hash = {}".format(admin_hash))
    admin_pw = hash_to_pw(admin_hash[5:])
    print("admin_pw = {}".format(admin_pw))
    zf.setpassword(admin_pw)
    my_secrets = zf.read("flagga.txt")
    print(my_secrets)