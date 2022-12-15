from flask import Flask, request, redirect
import sqlite3
import hashlib

app = Flask(__name__)

def sqlite_get_users(dbname):
    users = dict()
    con = sqlite3.connect("users.db")
    cur = con.cursor()
    cur.execute("SELECT username,pw_hash FROM users;")
    ul = cur.fetchall()
    for u in ul:
        users[u[0]] = u[1][5:]
    con.close()
    return(users)

@app.route("/login", methods=["POST"])
def login():
    username = request.form["user"]
    password = request.form["password"]
    pw_hash = hashlib.sha1(password.encode()).hexdigest()
    if username in all_users and (all_users[username] == pw_hash):
        redirect("welcome")
    else:
        redirect("unwelcome")
    return 0

@app.route("/welcome", methods=["GET"])
def welcome():
    app.make_response("Welcome user!")

@app.route("/unwelcome", methods=["GET"])
def unwelcome():
    app.make_response("Unwelcome user!")

if __name__ == "__main__":
    all_users = sqlite_get_users("users.db")
    print(all_users)
    app.run(port=8080, debug=True)