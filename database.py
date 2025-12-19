import sqlite3
from datetime import datetime

DB = "interview.db"


def init_db():
    con = sqlite3.connect(DB)
    cur = con.cursor()

    # Interview history
    cur.execute("""
        CREATE TABLE IF NOT EXISTS history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            role TEXT,
            score INTEGER,
            date TEXT
        )
    """)

    # Analytics (latest interview only)
    cur.execute("""
        CREATE TABLE IF NOT EXISTS analytics (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            communication INTEGER,
            technical INTEGER,
            confidence INTEGER,
            relevance INTEGER,
            negotiation INTEGER,
            overall REAL,
            recommendation TEXT,
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


# 🔥 SAVE ANALYTICS
def save_analytics(data: dict):
    con = sqlite3.connect(DB)
    cur = con.cursor()

    cur.execute("""
        INSERT INTO analytics (
            communication,
            technical,
            confidence,
            relevance,
            negotiation,
            overall,
            recommendation,
            date
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
    """, (
        data["communication"],
        data["technical"],
        data["confidence"],
        data["relevance"],
        data["negotiation"],
        data["overall"],
        data["recommendation"],
        datetime.now().strftime("%d-%m-%Y %H:%M")
    ))

    con.commit()
    con.close()


def load_history():
    con = sqlite3.connect(DB)
    cur = con.cursor()

    cur.execute(
        "SELECT role, score, date FROM history ORDER BY id DESC"
    )
    rows = cur.fetchall()

    con.close()
    return rows


# 🔥 LOAD LATEST ANALYTICS
def load_latest_analytics():
    con = sqlite3.connect(DB)
    cur = con.cursor()

    cur.execute("""
        SELECT
            communication,
            technical,
            confidence,
            relevance,
            negotiation,
            overall,
            recommendation
        FROM analytics
        ORDER BY id DESC
        LIMIT 1
    """)

    row = cur.fetchone()
    con.close()

    if not row:
        return None

    return {
        "communication": row[0],
        "technical": row[1],
        "confidence": row[2],
        "relevance": row[3],
        "negotiation": row[4],
        "overall": row[5],
        "recommendation": row[6],
    }
