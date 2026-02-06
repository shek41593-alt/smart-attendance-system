import sqlite3
import os
from datetime import datetime

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_PATH = os.path.join(BASE_DIR, "..", "database", "attendance.db")

def mark_attendance(student_id, subject):
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

    date = datetime.now().strftime("%Y-%m-%d")
    time = datetime.now().strftime("%H:%M:%S")

    # Prevent duplicate per day per subject
    cur.execute("""
        SELECT 1 FROM attendance
        WHERE student_id=? AND subject=? AND date=?
    """, (student_id, subject, date))

    if cur.fetchone() is None:
        cur.execute(
            "INSERT INTO attendance VALUES (?,?,?,?)",
            (student_id, subject, date, time)
        )
        print(f"[ATTENDANCE MARKED] {student_id} - {subject}")

    conn.commit()
    conn.close()
