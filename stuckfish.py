import sys, os
import tkinter as tk
import chess
import math
#from PIL import ImageTk, Image
from stuckfishsupport import *
from optiondialogue import * 
from alphaghetto import *

'''
Stuckfish Engine 0.001 - "AlphaGhetto" 
Chess engine developed on top of the python-chess library

Includes options to play against a friend or the Stuckfish bot 


Things missing/to-do:

- Implement perspective change

- Implement stuckfish bot
'''

class ChessBoard(tk.Tk):
    def __init__(self, size=100):
        '''
        This section of the code initializes the dimensions, colors, titles, piece family, and play type for the chess game.
        
        May eventually rewrite this portion so that the chessboard can be initialized using settings outside of the ChessBoard object,
        but for prototyping purposes leaving the dimensions and colors constant.
        Potentially could move settings to a separate file as well.

        The chess module automatically initializes the fen coding to be the starting position of: 
        rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1
        In essence, the code is using the chess module to perform validation and moves and wipes/refreshes/visualizes the board
        after each move.

        During testing, this fen position can be set in order to test the promotions function (contains a position where a pawn is on the 7th rank)
        self.fen = "4kbnr/Pp1npppp/1rb5/1N6/8/8/P3PPPP/R1B1KBNR b KQk - 0 12"
        '''
        super().__init__()
        super().resizable(False, False)
        self.chess = chess.Board()
        self.fen = self.chess.fen()
        self.rows = 8
        self.columns = 8
        self.size = size
        self.color1 = "#DDB88C"
        self.color2 = "#A66D4F"
        self.highlight_color1 = "#35C844"
        self.highlight_color2 = "#78ED84"
        self.title('Stuckfish Engine 0.001')
        self.geometry('800x800' + '+' + str(int((super().winfo_screenwidth()-800)/3)) + '+' + str(int((super().winfo_screenheight()-800)/4)))
        self.piece_type = "lichess"
        self.play_type = 0
        

        '''
        Critical components of the visualization portion of the chessboard.
        
        - The path is crucial for importing the correct family of chess pieces

        - The self.images array is absolutely essential due to the nature of how tkinter interacts with python's native garbage collection
          The array preserves the images needed within the ChessBoard object itself so the images won't be collected immediately upon running the program

        - The piece_codes dictionary is necessary for matching images to their respective pieces on the board

        This version of ChessBoard utilizes two separate 2d arrays in order to keep track of the different layers within the game

        - self.position tracks the location of pieces on the actual chess object chessboard

        - self.overlay keeps track of highlighted cells that should display on the board upon click

        '''
        self.path = os.getcwd()
        self.images = []
        self.piece_codes = {'b': "bblack", 'B': "bwhite", 'k': "kblack", 'K': "kwhite", 'n': "nblack", 'N': "nwhite", 'p': "pblack", 'P': "pwhite", 'q': "qblack", 'Q': "qwhite", 'r': "rblack", 'R': "rwhite"}
        self.position = [[0 for x in range(self.rows)] for y in range(self.columns)] 
        self.overlay = [[0 for x in range(self.rows)] for y in range(self.columns)]

        '''
        Additional tracking points

        - self.selection helps keep track of when the player is toggling between selecting a piece or selecting a destination

        - self.promotion_piece is used to store (temporarily) the piece returned by the promotion piece selection prompt

        - self.piece_square is meant to track the square in which the selected piece rests on

        - self.player_turn is used to determine whether it is the player's turn or the bot's turn (used only in bot play mode)
        '''
        self.selection = 0
        self.promotion_piece = ""
        self.piece_square = ""
        self.player_turn = 1


        '''
        Actual initial procedures begin

        - Initializing canvas and starting menu prompt before drawing the chessboard and listening for clicks
        '''
        self.canvas = tk.Canvas()
        self.canvas.pack(side="top", fill="both", expand=True, padx=0, pady=0)
        self.chess_popup(self.canvas, "menu")

        self.draw_board()
        self.draw_position()
        if self.play_type == 1:
            self.stuckfish = AlphaGhetto()
        self.canvas.bind("<Button-1>", self.left_click)

        
    '''
    Sometimes it's necessary to set the board position to something else or to reset the entire tracked position
    '''
    def set_fen(self, fen):
        self.fen = fen
        self.chess.set_board_fen(fen)

    def get_fen(self):
        return self.fen
    
    def reset_position(self, perspective="w"):
        self.position = [[0 for x in range(self.rows)] for y in range(self.columns)]
         

    def get_position(self, position):
        return position[:(findnth(position, " ", 1) - 2)]

    def get_piece(self, piece_x, piece_y):
        return self.position[piece_y][piece_x]

    '''
    Bot functionality
    '''
    def bot_move(self):
        if self.player_turn == 0:
            self.stuckfish.set_moves_list(self.get_valid_moves())
            self.stuckfish.ingest_fen(self.fen)
            self.chess.push(chess.Move.from_uci(self.stuckfish.pick_random()))
            print(self.stuckfish.calculate_material())
            self.fen = self.chess.fen()
            self.draw_board()
            self.draw_position()
            if self.chess.is_checkmate():
                self.chess_popup(self.canvas, "checkmate")
            elif self.chess.is_stalemate():
                self.chess_popup(self.canvas, "stalemate")
            elif self.chess.is_insufficient_material():
                self.chess_popup(self.canvas, "insufficient")
            self.player_turn = 1
        self.after(2000, self.bot_move)

    '''
    - get_valid_moves is important to return the list of valid moves in the original python-chess format

    - get_piece_moves returns only valid squares that the currently selected piece can go to
    '''
    def get_valid_moves(self):
        moves = []
        generator_moves = list(self.chess.legal_moves)
        for move in generator_moves:
            moves.append(move.uci())
        return moves
    
    def get_piece_moves(self, piece_pos):
        piece_moves = []
        for move in self.get_valid_moves():
            if move.startswith(piece_pos) and len(move) == 4:
                piece_moves.append(move[2:])
            elif move.startswith(piece_pos) and len(move) == 5:
                piece_moves.append(move[2:4])
        return piece_moves

    '''
    Chess being a primarily click-driven game means the primary functionality and user interaction is coded here
    '''
    def left_click(self, event):
        click_x = (math.floor(event.x / 100))
        click_y = (math.floor(event.y / 100))
        clicked_square = convert_col(click_x + 1) + str((8 - click_y))
        if self.player_turn == 1:
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
                '''
                Section of the code handles promotions

                - Should a piece of pawn type reach the 1st or 8th rank by any means, prompt for the type of piece to promote to
                '''
                if self.get_piece(int(convert_col(self.piece_square[0]) - 1), (8 - int(self.piece_square[1]))) == "P" and int(clicked_square[1:]) == 8:
                    self.chess_popup(self.canvas, "promotion")
                    self.chess.push(chess.Move.from_uci(self.piece_square + clicked_square + self.promotion_piece))
                    self.promotion_piece = ""
                    self.fen = self.chess.fen()
                    if self.play_type == 1:
                        self.player_turn = 0
                        #self.bot_move()
                elif self.get_piece(int(convert_col(self.piece_square[0]) - 1), (8 - int(self.piece_square[1]))) == "p" and int(clicked_square[1:]) == 1:
                    self.chess_popup(self.canvas, "promotion")
                    self.chess.push(chess.Move.from_uci(self.piece_square + clicked_square + self.promotion_piece))
                    self.promotion_piece = ""
                    self.fen = self.chess.fen()
                    if self.play_type == 1:
                        self.player_turn = 0
                        #self.bot_move()
                elif clicked_square in self.get_piece_moves(self.piece_square):
                    self.chess.push(chess.Move.from_uci(self.piece_square + clicked_square))
                    self.fen = self.chess.fen()
                    if self.play_type == 1:
                        self.player_turn = 0
                        #self.bot_move()
                elif clicked_square not in self.get_piece_moves(self.piece_square) and self.chess.is_check():
                    self.chess_popup(self.canvas, "check")
                self.piece_square = ""
                self.overlay = [[0 for x in range(self.rows)] for y in range(self.columns)]
                self.selection = 0
                self.draw_board()
                self.draw_position()
                #if self.play_type == 1:
                    #self.player_turn = 0
                    #self.bot_move()
            if self.chess.is_checkmate():
                self.chess_popup(self.canvas, "checkmate")
            elif self.chess.is_stalemate():
                self.chess_popup(self.canvas, "stalemate")
            elif self.chess.is_insufficient_material():
                self.chess_popup(self.canvas, "insufficient")


                
        '''
        else:
            self.stuckfish.set_moves_list(self.get_valid_moves())
            self.chess.push(chess.Move.from_uci(self.stuckfish.pick_random()))
            self.fen = self.chess.fen()
            self.draw_board()
            self.draw_position()
            self.player_turn = 1
        '''

    '''
    Generic function for redrawing the entire board, devoid of pieces
    '''

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

    '''
    Generic function for drawing all of the pieces onto the existing board, based on the currently stored FEN position
    '''

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
                self.position[y_value][x_value] = piece
                cur_piece = self.piece_codes[piece]
                if self.piece_type == "classic":
                    piece_img = tk.PhotoImage(file="classic/" + cur_piece + ".png")
                elif self.piece_type == "lichess":
                    piece_img = tk.PhotoImage(file="lichess/" + cur_piece + ".png")
                piece_id = self.canvas.create_image((x_value * 100) + 50, (y_value * 100) + 50, image=piece_img, tags="occupied", anchor="c")
                self.images.append(piece_img)
            x_value = x_value + 1
    
    '''
    Configured so that all popups are handled together
    '''
    def chess_popup(self, master, box_type):

        if box_type == "menu":
            self.start = OptionDialog(self.canvas, 'Play Stuckfish',"Select your opponent!", ["Play Friend", "Play Stuckfish", "Quit"])
            if self.start.result == "Quit":
                master.destroy()
                quit()
            elif self.start.result == "Play Friend":
                self.play_type = 0
            elif self.start.result == "Play Stuckfish":
                self.play_type = 1

        elif box_type == "promotion":
            self.promotions = OptionDialog(self.canvas, 'Promotion',"Select a piece", ["Queen", "Rook", "Bishop", "Knight"])
            if self.promotions.result == "Queen":
                self.promotion_piece = "q"
            elif self.promotions.result == "Rook":
                self.promotion_piece = "r"
            elif self.promotions.result == "Bishop":
                self.promotion_piece = "b"
            elif self.promotions.result == "Knight":
                self.promotion_piece = "n"

        elif box_type == "checkmate":
            self.start = OptionDialog(self.canvas, 'Game Over',"Checkmate!!!", ["Quit"])
            if self.start.result == "Quit":
                master.destroy()
                quit()
        
        elif box_type == "stalemate":
            self.start = OptionDialog(self.canvas, 'Game Over',"Stalemate!!!", ["Quit"])
            if self.start.result == "Quit":
                master.destroy()
                quit()
        
        elif box_type == "insufficient":
            self.start = OptionDialog(self.canvas, 'Game Over',"Draw: insufficient material!", ["Quit"])
            if self.start.result == "Quit":
                master.destroy()
                quit()

        elif box_type == "check":
            self.start = OptionDialog(self.canvas, 'Check',"Your king is in check", ["Ok sorry I'm dumb"])

        
        
'''
Driver code
'''
if __name__ == "__main__":
    
    board = ChessBoard()
    board.bot_move()
    board.mainloop()

