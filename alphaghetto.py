import sys
import os
import chess
import math
import random
import scipy
import numpy
import pandas
import sklearn
import torch
import sqlite3
from stuckfishsupport import *

'''
AlphaGhetto v001

Conceptually simple, first iteration of chess bot. Clones the game from stuckfish to run analysis on states of the game.
'''

class AlphaGhetto(object):
    def __init__(self, perspective="b"):
        self.connection = sqlite3.connect("alphaghetto.db")
        self.fen = ""
        self.rows = 8
        self.columns = 8
        self.perspective = perspective
        self.position = [[0 for x in range(self.rows)] for y in range(self.columns)]
        self.moves_list = []
        self.piece_values = {'K': 10000, 'k': 10000, 'Q': 90, 'q': 90, 'R': 50, 'r': 50, 'B': 35, 'b': 35, 'N': 33, 'n': 33, 'P': 10, 'p': 10}
        self.chess = chess
        self.board = self.chess.Board()
        self.move_spread = 20
        self.move_depth = 3
        
    '''
    Initialization functions
    
    There is some measure of difference between the names of objects in AlphaGhetto and Stuckfish, as there was some additional depth needed in AlphaGhetto. 
    The most obvious being self.chess no longer is related to Board() but rather the chess module (needs to access chess.SQUARES), and self.board is the Board()
    '''
    def get_fen_position(self):
        return self.fen[:(findnth(self.fen, " ", 1) - 2)]

    def set_fen(self, fen):
        self.fen = fen
        self.board.set_fen(fen)

    def set_position(self, position):
        self.position = position

    def set_moves_list(self, moves):
        self.moves_list = moves

    def get_valid_moves(self):
        moves = []
        generator_moves = list(self.board.legal_moves)
        for move in generator_moves:
            moves.append(move.uci())
        return moves

    def get_piece(self, piece_x, piece_y):
        return self.position[piece_y][piece_x]

    def get_piece_at(self, location):
        self.file = convert_col(location[:1])
        self.rank = location[1:]
        return self.position[8-int(self.rank)][int(self.file - 1)]

    def get_square_name(self, piece_x, piece_y):
        square_name = convert_col(piece_x + 1) + str(8 - piece_y)
        return square_name
    
    '''
    Re-plots the array representation of the game position (state) based on the ingested fen
    '''

    def refresh_position(self):
        self.position = [[0 for x in range(self.rows)] for y in range(self.columns)]
        x_value = 0
        y_value = 0
        for piece in self.get_fen_position():
            if piece == "/":
                x_value = -1
                y_value = y_value + 1
            elif piece.isnumeric():
                x_value = x_value + (int(piece) - 1)
            else:
                self.position[y_value][x_value] = piece
            x_value = x_value + 1

    '''
    One of the primary methods of calculating scores of moves
    This method calculates piece values by perspective and adds/subtracts any positional bonus points to the piece values
    '''
    def calculate_total_material(self, perspective):
        material_score = 0

        for piece_rank in range(len(self.position)):
            for piece_file in range(len(self.position[piece_rank])):

                if perspective == "b":
                    if self.get_piece(piece_file, piece_rank) in ['q', 'r', 'b', 'n', 'p']:
                        material_score = material_score + self.calculate_piece_value(piece_file, piece_rank, perspective)
                elif perspective == "w":
                    if self.get_piece(piece_file, piece_rank) in ['Q', 'R', 'B', 'N', 'P']:
                        material_score = material_score + self.calculate_piece_value(piece_file, piece_rank, perspective)
        return material_score




    def calculate_piece_value(self, piece_x, piece_y, perspective):
        piece_value = self.piece_values.get(self.get_piece(piece_x, piece_y))
        #piece_value = piece_value + self.calculate_piece_bonus(piece_x, piece_y) + self.calculate_capture_prospects(piece_x, piece_y, perspective)
        piece_value = piece_value + self.calculate_piece_bonus(piece_x, piece_y)
        return piece_value

    def calculate_piece_bonus(self, piece_x, piece_y):
        bonus = 0
        defender_points = 0
        attacker_points = 0
        if self.get_piece(piece_x, piece_y) == 'P':
            bonus = bonus + ((7 - piece_y) * 2)
            for attacker in self.get_attacker_locations(self.get_square_name(piece_x, piece_y).capitalize(), 'w'):
                if self.get_piece_at(attacker) == 'P':
                    bonus = bonus + 2
               
                #defender_points = defender_points + int(self.piece_values.get(self.get_piece_at(attacker)))
            for attacker in self.get_attacker_locations(self.get_square_name(piece_x, piece_y).capitalize(), 'b'):
                defender_points = defender_points + int(self.piece_values.get(self.get_piece_at(attacker)))
            if piece_x == 3 or piece_x == 4:
                if piece_y == 3 or piece_y == 4:
                    bonus = bonus + 3
                bonus = bonus + 5
            elif piece_x == 2 or piece_x == 5:
                bonus = bonus + 1
            if attacker_points >= defender_points:
                bonus = bonus - 10
        elif self.get_piece(piece_x, piece_y) == 'p':
            bonus = bonus + ((piece_y - 1) * 2)
            for attacker in self.get_attacker_locations(self.get_square_name(piece_x, piece_y).capitalize(), 'b'):
                if self.get_piece_at(attacker) == 'p':
                    bonus = bonus + 2
                #defender_points = defender_points + int(self.piece_values.get(self.get_piece_at(attacker)))
            for attacker in self.get_attacker_locations(self.get_square_name(piece_x, piece_y).capitalize(), 'w'):
                defender_points = defender_points + int(self.piece_values.get(self.get_piece_at(attacker)))
            if piece_x == 3 or piece_x == 4:
                if piece_y == 3 or piece_y == 4:
                    bonus = bonus + 3
                bonus = bonus + 5
            elif piece_x == 2 or piece_x == 5:
                bonus = bonus + 1
            if attacker_points >= defender_points:
                bonus = bonus - 10
        elif self.get_piece(piece_x, piece_y) == 'N':
            if piece_x == 0 or piece_x == 7 or piece_y == 0 or piece_y == 7:
                bonus = bonus - 10
            elif piece_x == 5 and piece_y == 3:
                bonus = bonus + 5
        elif self.get_piece(piece_x, piece_y) == 'n':
            if piece_x == 0 or piece_x == 7 or piece_y == 0 or piece_y == 7:
                bonus = bonus - 10
            elif piece_x == 5 and piece_y == 3:
                bonus = bonus + 5
        elif self.get_piece(piece_x, piece_y) == 'R':
            for attacker in self.get_attacker_locations(self.get_square_name(piece_x, piece_y).capitalize(), 'w'):
                if self.get_piece_at(attacker) == 'R':
                    bonus = bonus + 10
        elif self.get_piece(piece_x, piece_y) == 'r':
            for attacker in self.get_attacker_locations(self.get_square_name(piece_x, piece_y).capitalize(), 'b'):
                if self.get_piece_at(attacker) == 'r':
                    bonus = bonus + 10
        
        return bonus

    '''
    Independently evaluates the payoff of capturing an opponent's piece, based on the value of the attackers and the defenders
    '''
    def calculate_capture_prospects(self, piece_x, piece_y, perspective):
        captures = {}
        if len(self.get_attacking_locations(self.get_square_name(piece_x, piece_y).capitalize(), 'w')) > 0:
            for attack in self.get_attacking_locations(self.get_square_name(piece_x, piece_y).capitalize(), 'w'):
                attacked_piece = self.chess.square_name(attack)
                number_defenders = 0
                number_attackers = 0
                if perspective == 'b':
                    for defender in self.get_attacker_locations(attacked_piece, 'b'):
                        
                        defender_points = 0
                        bonus = 0
                        
                        defender_points = defender_points + self.piece_values[self.get_piece_at(defender)]
                    for attacker in self.get_attacker_locations(attacked_piece, 'b'):
                        attacker_points = attacker_points + self.piece_values[self.get_piece_at(attacker)]
        return bonus

    def simple_selection(self, perspective):
        considered_moves = {}
        self.current_depth = 0
        if len(self.get_valid_moves()) > self.move_spread:
            selected_moves = random.sample(self.get_valid_moves(), self.move_spread)
        else:
            selected_moves = self.get_valid_moves()
        for move in selected_moves:
            '''
            while current_depth < self.move_depth:
                scan_position(self.current_depth, self.position)
            '''
            self.board.push(chess.Move.from_uci(move))
            self.fen = self.board.fen()
            self.refresh_position()
            considered_moves[move] = self.calculate_total_material(perspective)
            self.board.pop()
        print(considered_moves)
        return max(considered_moves, key=considered_moves.get)
                


    def scan_position(self, depth, position):
        depth = depth + 1
        

    def get_attacker_locations(self, square_name, perspective):
        self.square_name = square_name
        attackers = []
        if perspective == 'b':
            for square in self.chess.SQUARES:
                if square in self.board.attackers(chess.BLACK, getattr(chess, self.square_name)):
                    attackers.append(chess.square_name(square))
        if perspective == 'w':
            for square in self.chess.SQUARES:
                if square in self.board.attackers(chess.WHITE, getattr(chess, self.square_name)):
                    attackers.append(chess.square_name(square))
        return attackers

    def get_attacking_locations(self, square_name, perspective):
        self.square_name = square_name
        attacking = []
        if perspective == 'b':
            for square in self.chess.SQUARES:
                if square in self.board.attacks(chess.BLACK, getattr(chess, self.square_name)):
                    attacking.append(chess.square_name(square))
        if perspective == 'w':
            for square in self.chess.SQUARES:
                if square in self.board.attacks(chess.WHITE, getattr(chess, self.square_name)):
                    attacking.append(chess.square_name(square))
        return attacking

    def initialize_tensors(self):
        print("test")

