import numpy as np


class Board(object):
    def __init__(self):
        pass

    def is_valid_move(self, move, color_number):
        pass

    def apply_new_move(self, move, player_color):
        pass

    def has_valid_move(self, color_number):
        pass

    def is_end_state(self):
        pass

    def is_out_of_board(self, position):
        pass

    def is_empty_position(self, position):
        pass

    def list_all_valid_moves(self, color_number):
        pass

    def list_all_empty_positions(self):
        pass

    def next_board_state(self, move, player_color):
        pass

    def as_numpy_matrix(self):
        pass
