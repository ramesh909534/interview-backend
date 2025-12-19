import sqlite3
from datetime import datetime

DB = "interview.db"

def init_db():
    con = sqlite3.connect(DB)
    cur = con.cursor()
    cur.execute("""
        CREATE TABLE IF NOT EXISTS history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            role TEXT,
            score INTEGER,
            date TEXT
        )
    """)
    con.commit()
    con.close()

def save_interview(role, score):
    con = sqlite3.connect(DB)
    cur = con.cursor()
    cur.execute(
        "INSERT INTO history (role, score, date) VALUES (?, ?, ?)",
        (role, score, datetime.now().strftime("%d-%m-%Y %H:%M"))
    )
    con.commit()
    con.close()

def load_history():
    con = sqlite3.connect(DB)
    cur = con.cursor()
    cur.execute("SELECT role, score, date FROM history ORDER BY id DESC")
    rows = cur.fetchall()
    con.close()
    return rows
