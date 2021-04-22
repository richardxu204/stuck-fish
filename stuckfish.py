import sys, os
import tkinter as tk
import chess
import math
from PIL import ImageTk, Image
from stuckfishsupport import *



class ChessBoard(tk.Frame):
    def __init__(self, parent, size=100):
        '''initialize chess board assuming normal chessboard dimensions'''
        self.rows = 8
        self.columns = 8
        self.color1 = "white"
        self.color2 = "black"
        self.size = size
        self.board = chess.Board()
        self.position = self.board.fen()[:(findnth(self.board.fen(), " ", 1) - 2)]
        self.path = os.getcwd()

        canvas_height = self.columns * self.size
        canvas_width = self.rows * self.size

        tk.Frame.__init__(self, parent)
        self.canvas = tk.Canvas(self, borderwidth=0, highlightthickness=0,
                                width=canvas_width, height=canvas_height, background="bisque")
        self.canvas.pack(side="top", fill="both", expand=True, padx=0, pady=0)

        # re-trigger refresh of the board
        self.canvas.bind("<Configure>", self.refresh_board)
        self.canvas.bind("<Button-1>", self.left_click)

        test_piece = tk.PhotoImage(file= self.path + "/pieces/testpiece.png")
        self.canvas.create_image(50, 50, anchor="c", image=test_piece)
        self.canvas.pack(side="top", fill="both", expand=True, padx=0, pady=0)

    def add_piece(self, name, image, row=0, column=0):
        #Add a piece to the playing board
        self.canvas.create_image(10 , 10, image=image, tags=(name, "piece"), anchor="c")
        
        
        #self.place_piece(name, row, column)


    def draw_position(self, fen_position):
        #cycle through whole board
        x_value = 0
        y_value = 0
        for piece in self.position:
            if piece == "/":
                x_value = -1
                y_value = y_value + 1
            elif piece.isnumeric():
                x_value = x_value + (int(piece) - 1)
            else:
                test_piece = PhotoImage(file= self.path + "/pieces/testpiece.ppm")
                #print(piece, x_value, y_value)
                #self.add_piece("test_piece", test_piece, x_value, y_value)
                test = canvas.create_image(50, 50, anchor=NE, image=test_piece)
                #self.canvas.update()
                #self.canvas.after(50, self.refresh_board)
            x_value = x_value + 1
        #self.canvas.update_idletasks()
        print("test")
        #tk.update()

    def left_click(self, event):
        print( "clicked at", (math.floor(event.x / 100)), (math.floor(event.y / 100)))
        #self.canvas.create_oval(1, 1, 1, 1, fill="#476042", outline="#476042", width=10)

    
    def refresh_board(self, event):
        #Redraw the board, possibly in response to window being resized
        xsize = int((event.width-1) / self.columns)
        ysize = int((event.height-1) / self.rows)
        self.size = min(xsize, ysize)
        self.canvas.delete("square")
        color = self.color2
        for row in range(self.rows):
            color = self.color1 if color == self.color2 else self.color2
            for col in range(self.columns):
                x1 = (col * self.size)
                y1 = (row * self.size)
                x2 = x1 + self.size
                y2 = y1 + self.size
                self.canvas.create_rectangle(x1, y1, x2, y2, outline="black", fill=color, tags="square")
                color = self.color1 if color == self.color2 else self.color2
        self.canvas.pack(side="top", fill="both", expand=True, padx=0, pady=0)


# driver code
if __name__ == "__main__":
    root = tk.Tk()
    board = ChessBoard(root)
    board.pack(side="top", fill="both", expand="true", padx=4, pady=4)
    #print(board.path)
    #player1 = tk.PhotoImage(data=imagedata)
    #board.addpiece("player1", player1, 0,0)
    #print(board.position)
    root.mainloop()


