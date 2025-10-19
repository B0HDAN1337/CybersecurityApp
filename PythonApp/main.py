import tkinter as tk
from database import setup_database, setup_admin
from LoginWindow import LoginWindow

if __name__ == "__main__":
    setup_database()
    setup_admin()
    root = tk.Tk()
    app = LoginWindow(root)
    root.mainloop()
