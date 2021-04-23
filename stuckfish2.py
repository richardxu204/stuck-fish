import sys, os
import tkinter as tk
#from tkinter import *
import chess
import math
from PIL import ImageTk, Image
from stuckfishsupport import *


#label = tk.Label(root, text ="Hello World !").pack()

class ChessBoard(tk.Tk):
    def __init__(self, size=100):
        super().__init__()
        super().resizable(False, False)
        self.path = os.getcwd()
        self.rows = 8
        self.columns = 8
        self.size = size
        self.color1 = "#DDB88C"
        self.color2 = "#A66D4F"
        self.title('Stuckfish Engine 0.001')
        self.geometry('800x800')
        self.images = {}

        self.canvas = tk.Canvas()
        self.canvas.pack(side="top", fill="both", expand=True, padx=0, pady=0)

        self.draw_board()
        self.draw_position()

        #image = Image.open("pieces/testpiece.gif")

        #self.canvas.create_image(50,50, image=test_piece)
        #self.canvas.create_image(50, 50, anchor="c", image=test_piece)
        #self.canvas.pack()
                
        #test_piece = tk.PhotoImage(file = "pieces/testpiece.gif")
        #test = tk.Label(self.frame, image=self.image)
        #test.pack()

    def draw_board(self, perspective="w"):
        color = self.color2
        for row in range(self.rows):
            color = self.color1 if color == self.color2 else self.color2
            for col in range(self.columns):
                x1 = (col * self.size)
                y1 = (row * self.size)
                x2 = x1 + self.size
                y2 = y1 + self.size
                self.canvas.create_rectangle(x1, y1, x2, y2, outline="black", fill=color, tags="empty")
                color = self.color1 if color == self.color2 else self.color2
        self.canvas.tag_lower("empty")
        self.canvas.tag_raise("occupied")
        #self.canvas.pack(side="top", fill="both", expand=True, padx=0, pady=0)

    def draw_position(self, perspective="w"):
        filename = "pieces/bblack.png"
        self.images[filename] = tk.PhotoImage(file=filename)
        self.canvas.create_image(150,50, image=self.images[filename], tags="occupied", anchor="c")
        #image.mode = "RGBA"
        #test = self.canvas.create_image(50,50, image=image)
        #label = tk.Label(self.canvas, image=image, bg=self.canvas.master['bg'])
        #label.photo = image
        #label.tkraise()
        #label.pack()

if __name__ == "__main__":
    board = ChessBoard()



    board.mainloop()

