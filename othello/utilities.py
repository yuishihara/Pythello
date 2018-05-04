import numpy as np


def color_string_to_number(color_string):
    return (-1 if (color_string == 'black') else 1)

def color_number_to_string(color_number):
    return ('black' if color_string_to_number('black') == color_number else 'white')


def opponent_color(color_string):
    return 'black' if color_string == 'white' else 'white'


def count_stone_num(board_state):
    matrix = board_state.as_numpy_matrix()
    black = np.count_nonzero(
        matrix == color_string_to_number('black'))
    white = np.count_nonzero(
        matrix == color_string_to_number('white'))
    return (black, white)
