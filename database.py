import sqlite3
from datetime import datetime

DB = "interview.db"


# 🔒 HOSPITAL DOMAIN ROLES
ALLOWED_ROLES = [
    "Doctor",
    "Nurse",
    "Staff Nurse",
    "Surgeon",
    "Physician",
    "Lab Technician",
    "Radiologist",
    "Pharmacist",
    "Medical Officer",
    "Hospital Administrator",
    "Receptionist",
    "Ward Boy",
    "Physiotherapist",
    "Anesthesiologist",
    "Cardiologist",
    "Neurologist",
    "Dentist",
    "Emergency Technician"
]


# =====================================================
# DATABASE CONNECTION
# =====================================================
def get_connection():
    return sqlite3.connect(DB)


# =====================================================
# INIT DATABASE
# =====================================================
def init_db():

    con = get_connection()
    cur = con.cursor()

    # Interview history table
    cur.execute("""
        CREATE TABLE IF NOT EXISTS history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            role TEXT,
            score INTEGER,
            date TEXT
        )
    """)

    # Analytics table
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


# =====================================================
# SAVE INTERVIEW HISTORY
# =====================================================
def save_interview(role: str, score: int):

    # 🔒 Prevent non-hospital roles
    if not any(r.lower() in role.lower() for r in ALLOWED_ROLES):
        return

    try:

        con = get_connection()
        cur = con.cursor()

        cur.execute(
            "INSERT INTO history (role, score, date) VALUES (?, ?, ?)",
            (
                role,
                score,
                datetime.now().strftime("%d-%m-%Y %H:%M")
            )
        )

        con.commit()
        con.close()

    except Exception:
        pass


# =====================================================
# SAVE ANALYTICS
# =====================================================
def save_analytics(data: dict):

    try:

        con = get_connection()
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
            data.get("communication", 0),
            data.get("technical", 0),
            data.get("confidence", 0),
            data.get("relevance", 0),
            data.get("negotiation", 0),
            data.get("overall", 0),
            data.get("recommendation", "Maybe"),
            datetime.now().strftime("%d-%m-%Y %H:%M")
        ))

        con.commit()
        con.close()

    except Exception:
        pass


# =====================================================
# LOAD INTERVIEW HISTORY
# =====================================================
def load_history():

    try:

        con = get_connection()
        cur = con.cursor()

        cur.execute(
            "SELECT role, score, date FROM history ORDER BY id DESC"
        )

        rows = cur.fetchall()

        con.close()

        return rows

    except Exception:

        return []


# =====================================================
# LOAD LATEST ANALYTICS
# =====================================================
def load_latest_analytics():

    try:

        con = get_connection()
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

    except Exception:

        return None