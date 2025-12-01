import tkinter as tk
from tkinter import messagebox, simpledialog, filedialog, Toplevel
from database import get_connection
from utils import hash_password, check_password, log_event, check_session_expiry
from datetime import datetime
import re
from reCaptchaWindow import ReCaptchaWindow
from LicenseManager import LicenseManager
import subprocess

class UserWindow:
    def __init__(self, username, session, on_logout=None, force_password_change=False, captcha_passed = False):
        self.username = username
        self.session = session
        self.on_logout = on_logout
        self.captcha_passed = captcha_passed
        self.license = LicenseManager()
        self.root = tk.Tk()
        self.root.title(f"User Panel - {username}")
        self.root.geometry("300x200")

        tk.Button(self.root, text="Change Password", command=self.change_password).pack(fill="x")
        tk.Button(self.root, text="Open File", command=self.open_file).pack(fill="x")
        tk.Button(self.root, text="Rate the application", command=self.open_qr).pack(fill="x")
        tk.Button(self.root, text="Exit", command=self.logout_logging_user).pack(fill="x")
        self.root.protocol("WM_DELETE_WINDOW", self.logout_logging_user)

        if force_password_change:
            self.root.after(100, lambda: self.change_password(force=True))

        self.root.after(1000, lambda: check_session_expiry(self.root, self.username))

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

        def captcha_result(success):
            if success:               
                self.root.after(0, lambda: self.save_password(new_hash, history))
            else:
                messagebox.showerror("Error", "You must pass the CAPTCHA to save password!")

        ReCaptchaWindow(captcha_result)

    def save_password(self, new_hash, history):
        conn = get_connection()
        c = conn.cursor()
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

    def logout_logging_user(self):
        log_event(self.username, "LOGOUT", f"{self.username} wylogowano o {datetime.now()}")
        try:
            self.session.end_session()
        except Exception:
            pass
        self.root.destroy()
   
    def ask_for_key(self):
        return simpledialog.askstring( "Key", "Enter the key to unlock the function (from 19:00):", show="*")

    def open_file(self):
        if self.license.is_blocked():
            key = self.ask_for_key()
            if key is None:
                return
            if not self.license.check_key(key):
                messagebox.showerror("Error", "Incorrect unlock key.")
                return

        file_path = "file_alert.docx" # select file path
        try:
            subprocess.call(["open", file_path])
        except Exception as e:
            messagebox.showerror("Error", f"The file cannot be opened:\n{e}")

    def open_qr(self):

        file_path = "QR.png"
        try: 
            subprocess.call(["open", file_path])
        except Exception as e:
            messagebox.showerror("Error", f"The QR code cannot be opened:\n{e}")
