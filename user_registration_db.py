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
        version TEXT,
        registered_at TEXT
    )''')
    try:
        conn.execute('ALTER TABLE registrations ADD COLUMN version TEXT')
    except sqlite3.OperationalError:
        pass
    conn.commit()
    return conn

def save_registration(name: str, email: str, phone: str, language: str, version: str = 'international'):
    conn = _get_conn()
    conn.execute(
        'INSERT INTO registrations (name, email, phone, language, version, registered_at) VALUES (?, ?, ?, ?, ?, ?)',
        (name, email, phone, language, version, datetime.utcnow().isoformat())
    )
    conn.commit()
    conn.close()

def get_registration_count() -> int:
    conn = _get_conn()
    count = conn.execute('SELECT COUNT(*) FROM registrations').fetchone()[0]
    conn.close()
    return count

def get_all_registrations():
    conn = _get_conn()
    rows = conn.execute('SELECT id, name, email, phone, language, version, registered_at FROM registrations ORDER BY registered_at DESC').fetchall()
    conn.close()
    return rows

def get_registration_stats():
    conn = _get_conn()
    total = conn.execute('SELECT COUNT(*) FROM registrations').fetchone()[0]
    china_count = conn.execute("SELECT COUNT(*) FROM registrations WHERE version = 'china'").fetchone()[0]
    intl_count = conn.execute("SELECT COUNT(*) FROM registrations WHERE version = 'international'").fetchone()[0]
    today = datetime.utcnow().strftime('%Y-%m-%d')
    today_count = conn.execute("SELECT COUNT(*) FROM registrations WHERE registered_at LIKE ?", (f'{today}%',)).fetchone()[0]
    conn.close()
    return {'total': total, 'china': china_count, 'international': intl_count, 'today': today_count}
