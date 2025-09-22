from flask import Flask, render_template, request, redirect
import sqlite3
import os

app = Flask(__name__)

DB = "messages.db"

# Initialize database
def init_db():
    if not os.path.exists(DB):
        with sqlite3.connect(DB) as conn:
            conn.execute(
                "CREATE TABLE IF NOT EXISTS messages (id INTEGER PRIMARY KEY, name TEXT, message TEXT)"
            )

# Student form
@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        name = request.form.get("name", "Anonymous")
        message = request.form.get("message")
        if message:
            with sqlite3.connect(DB) as conn:
                conn.execute("INSERT INTO messages (name, message) VALUES (?, ?)", (name, message))
            return redirect("/")
    return render_template("index.html")

# Admin view
@app.route("/admin")
def admin():
    with sqlite3.connect(DB) as conn:
        msgs = conn.execute("SELECT name, message FROM messages").fetchall()
    return render_template("admin.html", messages=msgs)

if __name__ == "__main__":
    init_db()
    app.run(debug=True)
