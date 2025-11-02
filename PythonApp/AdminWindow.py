import tkinter as tk
import tkinter.ttk as ttk
from tkinter import messagebox, simpledialog
from datetime import datetime, timedelta
from database import get_connection
from utils import log_event
from utils import hash_password, check_password, log_event, check_session_expiry


class AdminWindow:
    def __init__(self, session, on_logout=None):
        self.root = tk.Tk()
        self.session = session
        self.on_logout = on_logout
        self.root.title("Admin Panel")
        self.root.geometry("400x400")

        tk.Button(self.root, text="Change Admin Password", command=self.change_admin_password).pack(fill="x")
        tk.Button(self.root, text="Add User", command=self.add_user).pack(fill="x")
        tk.Button(self.root, text="View Users", command=self.view_users).pack(fill="x")
        tk.Button(self.root, text="Block/Unblock User", command=self.block_user).pack(fill="x")
        tk.Button(self.root, text="Delete User", command=self.delete_user).pack(fill="x")
        tk.Button(self.root, text="Edit User", command=self.edit_user).pack(fill="x")
        tk.Button(self.root, text="Set Password Policy", command=self.set_password_policy).pack(fill="x")
        tk.Button(self.root, text="Set Password Expiry", command=self.set_password_expiry).pack(fill="x")
        tk.Button(self.root, text="Logs", command=self.logs).pack(fill="x")
        tk.Button(self.root, text="Exit", command=self.logout_logging_admin).pack(fill="x")
        self.root.protocol("WM_DELETE_WINDOW", self.logout_logging_admin)

        self.root.after(150000, lambda: check_session_expiry(self.root))

        self.root.mainloop()

    def change_admin_password(self):
        old_pw = simpledialog.askstring("Old Password", "Enter old password:", show="*")
        conn = get_connection()
        c = conn.cursor()
        c.execute("SELECT password_hash FROM users WHERE username='ADMIN'")
        current_hash = c.fetchone()["password_hash"]

        if check_password(old_pw, current_hash):
            new_pw = simpledialog.askstring("New Password", "Enter new password:", show="*")
            new_pw2 = simpledialog.askstring("Repeat Password", "Repeat new password:", show="*")
            if new_pw == new_pw2:
                new_hash = hash_password(new_pw)
                c.execute("UPDATE users SET password_hash=? WHERE username='ADMIN'", (new_hash,))
                conn.commit()
                messagebox.showinfo("Success", "Password changed successfully")
            else:
                messagebox.showerror("Error", "Passwords do not match")
        else:
            messagebox.showerror("Error", "Old password incorrect")
        conn.close()

    def add_user(self):
        username = simpledialog.askstring("Username", "Enter username:")
        fullname = simpledialog.askstring("Full Name", "Enter full name:")
        password = simpledialog.askstring("Password", "Enter password:", show="*")
        otp = messagebox.askyesno("OTP", "Set one-time password?")
        password_hash = hash_password(password)
        expiry = (datetime.now() + timedelta(days=30)).strftime("%Y-%m-%d")

        conn = get_connection()
        c = conn.cursor()
        c.execute('''INSERT INTO users (username, fullname, password_hash, role, password_expiry, password_history, OTP)
                     VALUES (?, ?, ?, ?, ?, ?, ?)''',
                  (username, fullname, password_hash, 'user', expiry, '', 1 if otp else 0))
        conn.commit()
        conn.close()
        messagebox.showinfo("Success", f"User {username} added!")
        log_event("ADMIN", "CREATE", f"{username} Created")

    def view_users(self):
        conn = get_connection()
        c = conn.cursor()
        c.execute("SELECT username, fullname, role, blocked FROM users")
        users = c.fetchall()
        conn.close()

        info = "\n".join([f"{u['username']} - {u['fullname']} - {u['role']} - {'Blocked' if u['blocked'] else 'Active'}" for u in users])
        messagebox.showinfo("Users", info)

    def block_user(self):
        username = simpledialog.askstring("Username", "Enter username to block/unblock:")
        conn = get_connection()
        c = conn.cursor()
        c.execute("SELECT blocked FROM users WHERE username=?", (username,))
        result = c.fetchone()
        if result:
            new_state = 0 if result["blocked"] else 1
            c.execute("UPDATE users SET blocked=? WHERE username=?", (new_state, username))
            conn.commit()
            messagebox.showinfo("Success", f"User {username} {'blocked' if new_state else 'unblocked'}")
            log_event("ADMIN", "BLOCK", f"{username} changed to {new_state}")
        else:
            messagebox.showerror("Error", "User not found")
        conn.close()

    def delete_user(self):
        username = simpledialog.askstring("Username", "Enter username to delete:")
        conn = get_connection()
        c = conn.cursor()
        c.execute("DELETE FROM users WHERE username=?", (username,))
        conn.commit()
        conn.close()
        messagebox.showinfo("Success", f"User {username} deleted")
        log_event("ADMIN", "DELETE", f"{username} deleted")

    def set_password_policy(self):
        conn = get_connection()
        c = conn.cursor()
        c.execute("SELECT username, password_policy FROM users WHERE username != 'ADMIN'")
        users = c.fetchall()

        policy_window = tk.Toplevel(self.root)
        policy_window.title("Password Policy")
        policy_window.geometry("300x300")

        self.policy_vars = {}
        for i, user in enumerate(users):
            var = tk.IntVar(value=user["password_policy"])
            chk = tk.Checkbutton(policy_window, text=user["username"], variable=var)
            chk.pack(anchor="w")
            self.policy_vars[user["username"]] = var

        tk.Button(policy_window, text="Save", command=lambda: self.save_policy(policy_window)).pack(pady=10)

    def save_policy(self, window):
        conn = get_connection()
        c = conn.cursor()
        for username, var in self.policy_vars.items():
            c.execute("UPDATE users SET password_policy=? WHERE username=?", (var.get(), username))
        conn.commit()
        conn.close()
        messagebox.showinfo("Success", "Password policies updated")
        log_event("ADMIN", "PASSWORD POLICY", f"{username} changed to {var.get()}")
        window.destroy()


    def set_password_expiry(self):
        username = simpledialog.askstring("Username", "Enter username:")
        days = simpledialog.askinteger("Days", "Set password expiry in days:")
        expiry = (datetime.now() + timedelta(days=days or 0)).strftime("%Y-%m-%d")
        conn = get_connection()
        c = conn.cursor()
        c.execute("UPDATE users SET password_expiry=? WHERE username=?", (expiry, username))
        conn.commit()
        conn.close()
        messagebox.showinfo("Success", "Password expiry updated")
        log_event("ADMIN", "PASSWORD EXPIRY", f"{username} changed to {expiry}")


    def edit_user(self):
        username = simpledialog.askstring("Username", "Enter username to edit:")
        if not username:
            return

        conn = get_connection()
        c = conn.cursor()
        c.execute("SELECT * FROM users WHERE username=?", (username,))
        user = c.fetchone()
        if not user:
            messagebox.showerror("Error", "User not found")
            conn.close()
            return

        fullname = simpledialog.askstring("Full Name", "Enter full name:", initialvalue=user["fullname"])
        if fullname:
            c.execute("UPDATE users SET fullname=? WHERE username=?", (fullname, username))
            conn.commit()
            log_event("ADMIN", "USER EDITED", f"User name now changed to {fullname, username}")

        role = simpledialog.askstring("Role", "Enter role (user/admin):", initialvalue=user["role"])
        if role:
            c.execute("UPDATE users SET role=? WHERE username=?", (role, username))
            conn.commit()
            log_event("ADMIN", "USER EDITED", f"{username} role now changed to {role}")

        blocked = messagebox.askyesno("Blocked", "Should the user be blocked?")
        c.execute("UPDATE users SET blocked=? WHERE username=?", (1 if blocked else 0, username))
        conn.commit()
        log_event("ADMIN", "USER EDITED", f"{username} status now changed to {blocked}")

        if messagebox.askyesno("Change Password", "Do you want to change the password?"):
            new_pw = simpledialog.askstring("New Password", "Enter new password:", show="*")
            new_pw2 = simpledialog.askstring("Repeat Password", "Repeat new password:", show="*")
            if new_pw and new_pw == new_pw2:
                new_hash = hash_password(new_pw)
                c.execute("UPDATE users SET password_hash=?, first_login=0 WHERE username=?", (new_hash, username))
                conn.commit()
                log_event("ADMIN", "USER EDITED", f"{username} password changed by admin")
            else:
                messagebox.showerror("Error", "Passwords do not match")

        password_policy = messagebox.askyesno("Password Policy", "Enable password restrictions?")
        c.execute("UPDATE users SET password_policy=? WHERE username=?", (1 if password_policy else 0, username))
        conn.commit()
        log_event("ADMIN", "USER EDITED", f"{username} password policy changed by admin")

        days = simpledialog.askinteger("Password Expiry", "Set password expiry in days:", initialvalue=30)
        if days is not None:
            expiry = (datetime.now() + timedelta(days=days)).strftime("%Y-%m-%d")
            c.execute("UPDATE users SET password_expiry=? WHERE username=?", (expiry, username))
            conn.commit()
            log_event("ADMIN", "USER EDITED", f"{username} password expiry changed by admin")

        otp = messagebox.askyesno("OTP", "Set one-time password?")
        c.execute("UPDATE users SET OTP=? WHERE username=?", (1 if otp else 0, username))
        conn.commit()
        log_event("ADMIN", "USER EDITED", f"{username} one-time password policy changed by admin")

        conn.commit()
        conn.close()
        messagebox.showinfo("Success", f"User {username} updated successfully")

    def logs(self):
        conn = get_connection()
        c = conn.cursor()
        c.execute("SELECT username, timestamp, action, description FROM logs")
        user_logs = c.fetchall()
        conn.close()

        log_window = tk.Toplevel(self.root)
        log_window.title("Activity Logs")
        log_window.geometry("600x400")
        columns = ("username", "timestamp", "action", "description")
        tree = ttk.Treeview(log_window, columns=columns, show="headings")
        tree.heading("username", text="Username")
        tree.heading("timestamp", text="Timestamp")
        tree.heading("action", text="Action")
        tree.heading("description", text="Description")

        tree.column("username", width=100)
        tree.column("timestamp", width=150)
        tree.column("action", width=120)
        tree.column("description", width=300)

        for log in user_logs:
            tree.insert("", tk.END, values=(log["username"], log["timestamp"], log["action"], log["description"]))

        tree.pack(fill=tk.BOTH, expand=True)

        scrollbar = ttk.Scrollbar(log_window, orient=tk.VERTICAL, command=tree.yview)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

    def logout_logging_admin(self):
        log_event("ADMIN", "LOGOUT", f"Wylogowano o {datetime.now()}")
        try:
            self.session.end_session()
        except Exception:
            pass
        self.root.destroy()
