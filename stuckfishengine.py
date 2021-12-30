from sqlite3.dbapi2 import Error
import sys, os
import chess
import math
import random
import scipy, numpy, pandas, sklearn
import sqlite3
from sqlite3 import Error
from stuckfishsupport import * 
from alphaghetto import *

class Stuckfish(object):
    def __init__(self, perspective="b"):
        self.connection = sqlite3.connect("alphaghetto.db")
        #self.fen = ""
        self.perspective = perspective
        self.moves_list = []
        self.engine = AlphaGhetto()

    def set_moves_list(self, moves):
        self.moves_list = moves

    #first iteration test
    def pick_random(self):
        if len(self.moves_list) > 0:
            return random.choice(self.moves_list)

    #second iteration test
    def pick_simple_ag(self):
        self.engine.set_fen(self.fen)
        return self.engine.simple_selection()

    def ingest_fen(self, fen, position):
        #self.fen = fen
        self.engine.set_fen(fen)
        self.engine.set_position(position)

    def get_position(self):
        return self.fen[:(findnth(self.fen, " ", 1) - 2)]

    #Set up the database used to train chess model
    def create_connection(db_file):
        sql_connection = None
        try: 
            sql_connection = sqlite3.connect(db_file)
        except Error as e:
            print(e)

        return sql_connection

    def set_database(db_name):
        path = os.getcwd + db_name + ".db"

    def push_to_database():
        pass

    '''
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

                ''''''
                if piece.isnumeric() or piece == "/":
                    continue
                else:
                    material_score = material_score + self.piece_values.get(piece)
                ''''''
        return material_score
    '''

    def factors(self):
        print("nah son")

    def calculate_move_score(self, move):
        move_score = 0
        #move_score = move_score + calculate_material()


    def make_move(self):
        print("yolo")