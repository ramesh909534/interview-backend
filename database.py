import sqlite3

def init_db():
    con = sqlite3.connect("interviews.db")
    cur = con.cursor()
    cur.execute("""
    CREATE TABLE IF NOT EXISTS interviews(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        role TEXT,
        score INTEGER,
        created_at TEXT
    )
    """)
    con.commit()
    con.close()

def save_interview(role, score):
    con = sqlite3.connect("interviews.db")
    cur = con.cursor()
    cur.execute(
        "INSERT INTO interviews (role, score, created_at) VALUES (?, ?, datetime('now'))",
        (role, score)
    )
    con.commit()
    con.close()

def load_history():
    con = sqlite3.connect("interviews.db")
    cur = con.cursor()
    cur.execute("SELECT role, score, created_at FROM interviews")
    rows = cur.fetchall()
    con.close()
    return rows
