import sqlite3
import bcrypt
from datetime import datetime

def get_connection():
    conn = sqlite3.connect("users.db")
    conn.row_factory = sqlite3.Row
    return conn

def setup_database():
    conn = get_connection()
    c = conn.cursor()
    c.execute('''
    CREATE TABLE IF NOT EXISTS users (
        username TEXT PRIMARY KEY,
        fullname TEXT,
        password_hash BLOB,
        role TEXT,
        blocked INTEGER DEFAULT 0,
        password_expiry DATE,
        password_history TEXT,
        password_policy INTEGER DEFAULT 0,
        attempts INTEGER DEFAULT 0,
        block_time DATE,
        OTP INTEGER DEFAULT 0,
        first_login INTEGER DEFAULT 1
    )
    ''')
    
    c.execute('''CREATE TABLE IF NOT EXISTS logs (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT,
        timestamp TEXT NOT NULL,
        action TEXT NOT NULL,
        description TEXT
    )''')
    conn.commit()
    conn.close()

def setup_admin():
    conn = get_connection()
    c = conn.cursor()
    c.execute("SELECT * FROM users WHERE username='ADMIN'")
    if not c.fetchone():
        default_password = bcrypt.hashpw(b"admin123", bcrypt.gensalt())
        c.execute('''
        INSERT INTO users (username, fullname, password_hash, role, password_expiry, password_history, first_login)
        VALUES (?, ?, ?, ?, ?, ?, 0)
        ''', ('ADMIN', 'Administrator', default_password, 'admin',
              datetime.now().strftime("%Y-%m-%d"), ''))
        conn.commit()
    conn.close()
