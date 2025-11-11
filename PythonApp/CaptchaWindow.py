import tkinter as tk
from tkinter import messagebox
from PIL import Image, ImageTk, ImageDraw
import random

class CaptchaWindow:
    def __init__(self, parent, on_solved_callback):
        self.parent = parent
        self.on_solved_callback = on_solved_callback
        self.captcha_solved = False

        self.window = tk.Toplevel(self.parent)
        self.window.title("Puzzle CAPTCHA")

        self.img = Image.open("image.jpg")
        self.img_resized = self.img.resize((400, 400))

        piece_size = 50
        self.target_x = random.randint(0, 400 - piece_size)
        self.target_y = random.randint(0, 400 - piece_size)

        self.piece = self.img_resized.crop((self.target_x, self.target_y, self.target_x + piece_size, self.target_y + piece_size))

        self.img_with_hole = self.img_resized.copy()
        draw = ImageDraw.Draw(self.img_with_hole)
        draw.rectangle((self.target_x, self.target_y,
                        self.target_x + piece_size, self.target_y + piece_size), fill="white")

        self.tk_img = ImageTk.PhotoImage(self.img_with_hole)

        self.canvas = tk.Canvas(self.window, width=400, height=400)
        self.canvas.pack()
        self.canvas.create_image(0, 0, anchor="nw", image=self.tk_img)

        self.tk_piece = ImageTk.PhotoImage(self.piece)
        self.piece_x, self.piece_y = random.randint(0, 350), random.randint(0, 350)
        self.piece_id = self.canvas.create_image(self.piece_x, self.piece_y, anchor="nw", image=self.tk_piece)

        self.canvas.tag_bind(self.piece_id, "<Button1-Motion>", self.move_piece)
        self.canvas.tag_bind(self.piece_id, "<ButtonRelease-1>", self.check_position)

    def move_piece(self, event):
        self.canvas.coords(self.piece_id, event.x - 25, event.y - 25)

    def check_position(self, event):
        x, y = self.canvas.coords(self.piece_id)
        if abs(x - self.target_x) < 5 and abs(y - self.target_y) < 5:
            messagebox.showinfo("Success", "CAPTCHA resolved!")
            self.captcha_solved = True
            self.window.destroy()
            self.on_solved_callback()
        else:
            messagebox.showwarning("Error", "Try again!")
