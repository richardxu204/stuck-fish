import sys, os
import chess
import math
import random

class AlphaGhetto(object):
    def __init__(self, perspective="b"):
        self.data = ""
        self.moves_list = []

    def set_moves_list(self, moves):
        self.moves_list = moves

    def pick_random(self):
        return random.choice(self.moves_list)
