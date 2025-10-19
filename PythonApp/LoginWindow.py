import tkinter as tk
from tkinter import messagebox
from database import get_connection
from utils import check_password
from AdminWindow import AdminWindow
from UserWindow import UserWindow

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
        conn.close()

        if not user:
            messagebox.showerror("Error", "Login lub Hasło niepoprawny")
            return

        if user["blocked"]:
            messagebox.showerror("Error", "Konto zablokowane")
            return

        if check_password(password_input, user["password_hash"]):
            self.master.after(100, lambda: self.open_user_window(username, user))
        else:
            messagebox.showerror("Error", "Login lub Hasło niepoprawny")


    def open_user_window(self, username, user):
        self.master.destroy() 
        if username == "ADMIN":
            AdminWindow()
        elif user["first_login"] == 1:
            UserWindow(username, force_password_change=True)
        else:
         UserWindow(username)