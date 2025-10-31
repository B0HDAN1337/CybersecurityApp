import bcrypt
from database import get_connection
from datetime import datetime
from tkinter import messagebox
import tkinter as tk
from SessionManager import SessionManager
import math, hashlib

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

session = SessionManager(timeout_minutes=1)

def logout(window=None):
    session.end_session()
    if window:
        try: 
            window.destroy()
        except Exception:
            pass
    start_login_window()

def start_login_window():
    from LoginWindow import LoginWindow
    root = tk.Tk()
    app = LoginWindow(root)
    root.mainloop()

def check_session_expiry(window):
    if not session.check_session():
        messagebox.showinfo("Session expired", "Your session has expired. Please log in again.")
        logout(window)
        return
    window.after(5000, lambda: check_session_expiry(window))

def open_user_window(parent, username, user):
    from AdminWindow import AdminWindow
    from UserWindow import UserWindow
    
    if hasattr(parent, 'master'):
        parent.master.destroy()
    else:
        parent.destroy()

    if username == "ADMIN":
        AdminWindow(session)
    elif user["first_login"] == 1:
        UserWindow(username, session, on_logout=lambda: logout(), force_password_change=True)
    else:
        UserWindow(username, session, on_logout=lambda: logout())

def generate_OTP(username, secret_x, a):
    v = secret_x/ math.sin(a)
    data = f"{username}|{int(v)}|{a}"
    digest = hashlib.sha256(data.encode()).hexdigest()
    otp = int(digest, 16) % 1_000_000
    return f"{otp:06d}"