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
        self.move_spread = 10
        self.move_depth = 3
        

    def set_fen(self, fen):
        self.fen = fen
        self.board.set_fen(fen)

    def set_position(self, position):
        self.position = position

    def set_moves_list(self, moves):
        self.moves_list = moves

    def get_piece_at(self, location):
        self.file = convert_col(location[:1])
        self.rank = location[1:]
        return self.position[8-int(self.rank)][int(self.file)]

    def calculate_total_material(self, perspective):
        material_score = 0
        if perspective == "b":
            for piece in self.fen.get_position():
                if piece in ['q', 'r', 'b', 'n', 'p']:
                    material_score = material_score + self.piece_values.get(piece)
        elif perspective == "w":
            for piece in self.fen.get_position():
                if piece in ['Q', 'R', 'B', 'N', 'P']:
                    material_score = material_score + self.piece_values.get(piece)
        return material_score

    def calculate_piece_value(self, piece):
        piece_value = self.piece_values.get(piece)
        piece_value = piece_value + calculate_piece_bonus(piece)
        return piece_value

    def calculate_piece_bonus(self, piece):
        if piece == 'p' or piece == 'P':
            print("ye")


    def simple_selection(self):
        considered_moves = {}
        self.current_depth = 0
        selected_moves = random.sample(self.chess.get_valid_moves(), self.move_depth)
        for move in selected_moves:
            while current_depth < self.move_depth:
                scan_position(self.current_depth, self.position)

    def scan_position(self, depth, position):
        depth = depth + 1
        

    def get_attacker_locations(self, square_name, perspective='b'):
        self.square_name = square_name
        attackers = []
        if perspective == 'b':
            for square in self.chess.squares:
                if square in self.board.attackers(chess.BLACK, getattr(chess, self.square_name)):
                    attackers.append(chess.square_name(square))
        if perspective == 'w':
            for square in self.chess.SQUARES:
                if square in self.board.attackers(chess.WHITE, getattr(chess, self.square_name)):
                    attackers.append(chess.square_name(square))
        return attackers

    def initialize_tensors(self):
        print("test")

