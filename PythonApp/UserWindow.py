import tkinter as tk
from tkinter import messagebox, simpledialog, Toplevel
from database import get_connection
from utils import hash_password, check_password, log_event
import re

class UserWindow:
    def __init__(self, username, force_password_change=False):
        self.username = username
        self.root = tk.Tk()
        self.root.title(f"User Panel - {username}")
        self.root.geometry("300x200")

        tk.Button(self.root, text="Change Password", command=self.change_password).pack(fill="x")
        tk.Button(self.root, text="Exit", command=self.root.destroy).pack(fill="x")

        if force_password_change:
            self.root.after(100, lambda: self.change_password(force=True))

        self.root.mainloop()

    def change_password(self, force=False):
        old_pw = simpledialog.askstring("Old Password", "Enter old password:", show="*")
        if old_pw is None:
            if force:
                messagebox.showwarning("Warning", "You must change your password!")
                return self.change_password(force=True)
            return

        conn = get_connection()
        c = conn.cursor()
        c.execute("SELECT password_hash, password_history, password_policy FROM users WHERE username=?", (self.username,))
        result = c.fetchone()

        if not check_password(old_pw, result["password_hash"]):
            messagebox.showerror("Error", "Old password incorrect")
            conn.close()
            if force:
                return self.change_password(force=True)
            return

        new_pw = simpledialog.askstring("New Password", "Enter new password:", show="*")
        if new_pw is None:
            if force:
                messagebox.showwarning("Warning", "You must set a new password!")
                return self.change_password(force=True)
            return

        new_pw2 = simpledialog.askstring("Repeat Password", "Repeat new password:", show="*")
        if new_pw != new_pw2:
            messagebox.showerror("Error", "Passwords do not match")
            conn.close()
            if force:
                return self.change_password(force=True)
            return

        if result["password_policy"] and not self.validate_password(new_pw):
            messagebox.showerror("Error", 
                "Password must contain at least one uppercase letter, one lowercase letter, and three digits.")
            conn.close()
            if force:
                return self.change_password(force=True)
            return

        history = result["password_history"].split(',') if result["password_history"] else []
        if new_pw in history:
            messagebox.showerror("Error", "Cannot reuse old password")
            conn.close()
            if force:
                return self.change_password(force=True)
            return

        new_hash = hash_password(new_pw)
        history.append(new_pw)
        history = ','.join(history[-5:])

        c.execute(
            "UPDATE users SET password_hash=?, password_history=?, first_login=0 WHERE username=?",
            (new_hash, history, self.username)
        )
        conn.commit()
        conn.close()
        messagebox.showinfo("Success", "Password changed successfully")
        log_event(self.username, "PASSWORD", f"{self.username} changed password")
            
    def validate_password(self, password) -> bool:
        if len(password) < 4: 
            return False
        if not re.search(r'[A-Z]', password):
            return False 
        if not re.search(r'[a-z]', password):
            return False 
        if len(re.findall(r'\d', password)) < 3:
            return False  
        return True 