from flask import Flask, render_template, request, redirect
import sqlite3
import os

app = Flask(__name__)

# Make DB path absolute so it works on Render
DB = os.path.join(os.path.dirname(__file__), "messages.db")

# Initialize database
def init_db():
    with sqlite3.connect(DB) as conn:
        conn.execute(
            "CREATE TABLE IF NOT EXISTS messages (id INTEGER PRIMARY KEY AUTOINCREMENT, name TEXT, message TEXT)"
        )

# Student form
@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        name = request.form.get("name") or "Anonymous"
        message = request.form.get("message")
        if message:
            with sqlite3.connect(DB) as conn:
                conn.execute(
                    "INSERT INTO messages (name, message) VALUES (?, ?)",
                    (name, message)
                )
            return redirect("/")
    return render_template("index.html")

# Admin view
@app.route("/admin")
def admin_view():
    with sqlite3.connect(DB) as conn:
        msgs = conn.execute("SELECT name, message FROM messages ORDER BY id DESC").fetchall()
    return render_template("admin.html", messages=msgs)

# Optional debug route
@app.route("/debug")
def debug():
    with sqlite3.connect(DB) as conn:
        data = conn.execute("SELECT * FROM messages").fetchall()
    return f"<pre>{data}</pre>"

if __name__ == "__main__":
    init_db()
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port, debug=True)
