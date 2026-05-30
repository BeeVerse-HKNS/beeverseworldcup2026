import sqlite3
import os
from datetime import datetime

DB_PATH = os.path.join(os.path.dirname(__file__), 'data', 'registrations.db')

def _get_conn():
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    conn = sqlite3.connect(DB_PATH)
    conn.execute('''CREATE TABLE IF NOT EXISTS registrations (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        email TEXT NOT NULL,
        phone TEXT,
        language TEXT,
        registered_at TEXT
    )''')
    conn.commit()
    return conn

def save_registration(name: str, email: str, phone: str, language: str):
    conn = _get_conn()
    conn.execute(
        'INSERT INTO registrations (name, email, phone, language, registered_at) VALUES (?, ?, ?, ?, ?)',
        (name, email, phone, language, datetime.utcnow().isoformat())
    )
    conn.commit()
    conn.close()

def get_registration_count() -> int:
    conn = _get_conn()
    count = conn.execute('SELECT COUNT(*) FROM registrations').fetchone()[0]
    conn.close()
    return count
