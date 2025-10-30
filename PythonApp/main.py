import tkinter as tk
from database import setup_database, setup_admin
from utils import start_login_window

if __name__ == "__main__":
    setup_database()
    setup_admin()
    start_login_window()