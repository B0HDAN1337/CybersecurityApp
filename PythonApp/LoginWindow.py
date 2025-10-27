import tkinter as tk
from tkinter import messagebox
from database import get_connection
from utils import check_password, log_event
from AdminWindow import AdminWindow
from UserWindow import UserWindow
from datetime import datetime, timedelta

MAX_LOGIN = 3
TIME_BLOCK = 15

class LoginWindow:
    def __init__(self, master):
        self.master = master
        master.title("Login")
        master.geometry("300x150")

        tk.Label(master, text="Username:").pack()
        self.username_entry = tk.Entry(master)
        self.username_entry.pack()

        tk.Label(master, text="Password:").pack()
        self.password_entry = tk.Entry(master, show="*")
        self.password_entry.pack()

        tk.Button(master, text="Login", command=self.login).pack()

    def login(self):
        username = self.username_entry.get()
        password_input = self.password_entry.get()

        conn = get_connection()
        c = conn.cursor()
        c.execute("SELECT * FROM users WHERE username=?", (username,))
        user = c.fetchone()

        if not user:
            messagebox.showerror("Error", "Login lub Hasło niepoprawny")
            log_event(user, "LOGIN", "Login lub Hasło niepoprawny")
            return

        if user["blocked"]:
            messagebox.showerror("Error", "Konto zablokowane")
            log_event(f"{username}", "LOGIN", "Blocked")
            return
        
        blocked_time = user["block_time"]
        now = datetime.now()
        attempts = user["attempts"] or 0

        if blocked_time:
            blocked_time = datetime.fromisoformat(blocked_time)

        # Check block
        if blocked_time and blocked_time > now:
            remaining = int((blocked_time - now).total_seconds())
            messagebox.showerror("Blocked", f"Too many attempts. Try again in {remaining} sec.")
            log_event(username, "LOGIN", f"Attempted login during block, {remaining}s left")
            return

        # Check password
        if check_password(password_input, user["password_hash"]):
            c.execute("UPDATE users SET attempts=0, block_time=NULL WHERE username=?", (username,))
            conn.commit()
            log_event(username, "LOGIN", f"{username} login to application")
            self.master.after(100, lambda: self.open_user_window(username, user))
        else:
            attempts += 1
            c.execute("UPDATE users SET attempts=? WHERE username=?", (attempts, username))
            conn.commit()
            block_time_to_set = None
        
            messagebox.showerror("Error", "Login lub Hasło niepoprawny")
            log_event(f"{username}", "LOGIN", "Login lub Hasło niepoprawny")

            if attempts >= MAX_LOGIN:
                block_time_to_set = now + timedelta(minutes=TIME_BLOCK)
                c.execute(
                "UPDATE users SET attempts=?, block_time=? WHERE username=?",
                (attempts, block_time_to_set.isoformat() if block_time_to_set else None, username)
                )
                conn.commit()
                log_event(username, "BLOCK", f"Account is blocked for {TIME_BLOCK} minut")
                messagebox.showerror("BLOCK", f"Account is blocked for {TIME_BLOCK} minut")
        
        conn.close()

    def open_user_window(self, username, user):
        self.master.destroy() 
        if username == "ADMIN":
            AdminWindow()
        elif user["first_login"] == 1:
            UserWindow(username, force_password_change=True)
        else:
         UserWindow(username)