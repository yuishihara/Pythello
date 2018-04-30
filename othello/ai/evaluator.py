from .. import utilities

class Evaluator(object):
    def __init__(self):
        pass

    def evaluate(self, board_state, player_color):
        player_move_num = len(utilities.list_all_valid_moves(board_state, player_color))
        opponent_move_num = len(utilities.list_all_valid_moves(board_state, player_color * -1))

        return (player_move_num - opponent_move_num)