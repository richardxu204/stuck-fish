import tkinter as tk
import chess
from stuckfishsupport import *


class ChessBoard(tk.Frame):
    def __init__(self, parent, size=100):
        self.rows = 8
        self.columns = 8
        self.color1 = "white"
        self.color2 = "black"
        self.size = size
        self.board = chess.Board()
        self.position = self.board.fen()[:(findnth(self.board.fen(), " ", 1) - 2)]

        canvas_height = self.columns * self.size
        canvas_width = self.rows * self.size

        tk.Frame.__init__(self, parent)
        self.canvas = tk.Canvas(self, borderwidth=5, highlightthickness=5,
                                width=canvas_width, height=canvas_height, background="bisque")
        self.canvas.pack(side="top", fill="both", expand=True, padx=2, pady=2)

        # re-trigger refresh of the board
        self.canvas.bind("<Configure>", self.refresh_board)

    def refresh_board(self, event):
        '''Redraw the board, possibly in response to window being resized'''
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
        #for name in self.position:
            #self.placepiece(name, self.position[name][0], self.position[name][1])
        self.canvas.tag_raise("piece")
        self.canvas.tag_lower("square")


# driver code
if __name__ == "__main__":
    root = tk.Tk()
    board = ChessBoard(root)
    board.pack(side="top", fill="both", expand="true", padx=4, pady=4)
    #player1 = tk.PhotoImage(data=imagedata)
    #board.addpiece("player1", player1, 0,0)
    print(board.position)
    root.mainloop()


