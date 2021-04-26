import sys, os
import tkinter as tk
import chess
import math
from PIL import ImageTk, Image
from stuckfishsupport import *



class ChessBoard(tk.Tk):
    def __init__(self, size=100):
        super().__init__()
        super().resizable(False, False)
        self.chess = chess.Board()
        self.fen = self.chess.fen()
        self.path = os.getcwd()
        self.rows = 8
        self.columns = 8
        self.size = size
        self.color1 = "#DDB88C"
        self.color2 = "#A66D4F"
        self.highlight_color1 = "#35C844"
        self.highlight_color2 = "#78ED84"
        self.title('Stuckfish Engine 0.001')
        self.geometry('800x800')
        
        #self.images = {}
        self.images = []
        self.piece_codes = {'b': "bblack", 'B': "bwhite", 'k': "kblack", 'K': "kwhite", 'n': "nblack", 'N': "nwhite", 'p': "pblack", 'P': "pwhite", 'q': "qblack", 'Q': "qwhite", 'r': "rblack", 'R': "rwhite"}
        self.position = [[0 for x in range(self.rows)] for y in range(self.columns)] 
        self.overlay = [[0 for x in range(self.rows)] for y in range(self.columns)] 
        self.selection = 0
        self.piece_square = ""

        self.canvas = tk.Canvas()
        self.canvas.pack(side="top", fill="both", expand=True, padx=0, pady=0)

        self.draw_board()
        self.draw_position()
        self.canvas.bind("<Button-1>", self.left_click)


    def set_fen(self, fen):
        self.fen = fen

    def get_position(self, position):
        return position[:(findnth(position, " ", 1) - 2)]

    def get_piece(self, piece_x, piece_y):
        return self.position[piece_x][piece_y]

    def get_valid_moves(self):
        moves = []
        generator_moves = list(self.chess.legal_moves)
        for move in generator_moves:
            moves.append(move.uci())
        
        return moves
        
    def get_piece_moves(self, piece_pos):
        piece_moves = []
        for move in self.get_valid_moves():
            if move.startswith(piece_pos):
                piece_moves.append(move[-2:])
        return piece_moves

    def left_click(self, event):
        click_x = (math.floor(event.x / 100))
        click_y = (math.floor(event.y / 100))
        clicked_square = convert_col(click_x + 1) + str((8 - click_y))
        if self.selection == 0:
            self.overlay = [[0 for x in range(self.rows)] for y in range(self.columns)]
            self.overlay[click_y][click_x] = 1
            for move in self.get_piece_moves(clicked_square):
                self.overlay[8 - int(move[1])][int(convert_col(move[:1])) - 1] = 2
            self.draw_board()
            self.draw_position()
            self.selection = 1
            self.piece_square = clicked_square
        else:
            if clicked_square in self.get_piece_moves(self.piece_square):
                self.chess.push(chess.Move.from_uci(self.piece_square + clicked_square))
                self.fen = self.chess.fen()
            self.piece_square = ""
            self.overlay = [[0 for x in range(self.rows)] for y in range(self.columns)]
            self.selection = 0
            self.draw_board()
            self.draw_position()


    def draw_board(self, perspective="w"):
        self.canvas.delete("all")
        color = self.color2
        for row in range(self.rows):
            color = self.color1 if color == self.color2 else self.color2
            for col in range(self.columns):
                x1 = (col * self.size)
                y1 = (row * self.size)
                x2 = x1 + self.size
                y2 = y1 + self.size
                if self.overlay[row][col] == 1:
                    self.canvas.create_rectangle(x1, y1, x2, y2, outline="black", fill=self.highlight_color1, tags="empty")
                elif self.overlay[row][col] == 2:
                    self.canvas.create_rectangle(x1, y1, x2, y2, outline="black", fill=self.highlight_color2, tags="empty")
                else:
                    self.canvas.create_rectangle(x1, y1, x2, y2, outline="black", fill=color, tags="empty")
                color = self.color1 if color == self.color2 else self.color2
        self.canvas.tag_lower("empty")
        self.canvas.tag_raise("occupied")
        #self.canvas.pack(side="top", fill="both", expand=True, padx=0, pady=0)

    def reset_position(self, perspective="w"):
        self.position = [[0 for x in range(self.rows)] for y in range(self.columns)]
         

    def draw_position(self, perspective="w"):
        #cycle through whole board

        #reset the stored position of the whole board for re-drawing of position
        self.position = [[0 for x in range(self.rows)] for y in range(self.columns)]
        
        x_value = 0
        y_value = 0
        for piece in self.get_position(self.fen):
            if piece == "/":
                x_value = -1
                y_value = y_value + 1
            elif piece.isnumeric():
                x_value = x_value + (int(piece) - 1)
            else:
                #piece_id = 1
                self.position[y_value][x_value] = piece
                cur_piece = self.piece_codes[piece]
                piece_img = tk.PhotoImage(file="pieces/" + cur_piece + ".png")
                piece_id = self.canvas.create_image((x_value * 100) + 50, (y_value * 100) + 50, image=piece_img, tags="occupied", anchor="c")
                self.images.append(piece_img)
            x_value = x_value + 1

    

  

if __name__ == "__main__":
    board = ChessBoard()
    board.mainloop()

