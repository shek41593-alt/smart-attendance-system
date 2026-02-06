from flask import Flask, render_template
import sqlite3
import os

app = Flask(__name__)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "database", "attendance.db")

def fetch_attendance():
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)

    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    cur.execute("""
        CREATE TABLE IF NOT EXISTS attendance (
            student_id TEXT,
            subject TEXT,
            date TEXT,
            time TEXT
        )
    """)

    cur.execute("""
        SELECT student_id, subject, date, time
        FROM attendance
        ORDER BY date DESC, time DESC
    """)

    rows = cur.fetchall()
    conn.close()
    return rows

@app.route("/")
def dashboard():
    return render_template("dashboard.html", attendance=fetch_attendance())

if __name__ == "__main__":
    app.run(debug=True)
