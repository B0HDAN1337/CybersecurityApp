import bcrypt
from database import get_connection
from datetime import datetime

def check_password(password_input, stored_hash):
    return bcrypt.checkpw(password_input.encode(), stored_hash)

def hash_password(password):
    return bcrypt.hashpw(password.encode(), bcrypt.gensalt())

def log_event(username: str, action: str, description: str = ""):
    conn = get_connection()
    c = conn.cursor()
    timestamp = datetime.now().isoformat()
    c.execute(
        "INSERT INTO logs (username, timestamp, action, description) VALUES (?, ?, ?, ?)",
        (username, timestamp, action, description)
    )
    conn.commit()
    conn.close()