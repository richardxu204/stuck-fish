import sys, os
import chess
import math
import random
from stuckfishsupport import * 

class AlphaGhetto(object):
    def __init__(self, perspective="b"):
        self.data = ""
        self.fen = ""
        self.perspective = perspective
        self.moves_list = []
        self.piece_values = {'K': 1000000, 'k': 1000000, 'Q': 90, 'q': 90, 'R': 50, 'r': 50, 'B': 33, 'b': 33, 'N': 30, 'n': 30, 'P': 10, 'p': 10}

    def set_moves_list(self, moves):
        self.moves_list = moves

    def pick_random(self):
        if len(self.moves_list) > 0:
            return random.choice(self.moves_list)

    def ingest_fen(self, fen):
        self.fen = fen

    def get_position(self):
        return self.fen[:(findnth(self.fen, " ", 1) - 2)]

    def calculate_material(self):
        material_score = 0
        if self.perspective == "b":
            for piece in self.get_position():
                if piece in ['q', 'r', 'b', 'n', 'p']:
                    material_score = material_score + self.piece_values.get(piece)
        elif self.perspective == "w":
            for piece in self.get_position():
                if piece in ['Q', 'R', 'B', 'N', 'P']:
                    material_score = material_score + self.piece_values.get(piece)

                '''
                if piece.isnumeric() or piece == "/":
                    continue
                else:
                    material_score = material_score + self.piece_values.get(piece)
                '''
        return material_score


    def make_move(self):
        print("yolo")