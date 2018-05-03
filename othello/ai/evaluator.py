import numpy as np

POSITION_VALUES = np.array([[ 30, -12,  0, -1, -1,  0, -12,  30],
                            [-12, -15, -3, -3, -3, -3, -15, -12],
                            [  0,  -3,  0, -1, -1,  0,  -3,   0],
                            [ -1,  -3, -1, -1, -1, -1,  -3,  -1],
                            [ -1,  -3, -1, -1, -1, -1,  -3,  -1],
                            [  0,  -3,  0, -1, -1,  0,  -3,   0],
                            [-12, -15, -3, -3, -3, -3, -15, -12],
                            [ 30, -12 , 0, -1, -1,  0, -12,  30]])


class Evaluator(object):
    def __init__(self):
        pass

    def evaluate(self, board_state, player_color):
        player_move_num = len(board_state.list_all_valid_moves(player_color))
        opponent_move_num = len(board_state.list_all_valid_moves(player_color * -1))
        matrix_form = board_state.as_numpy_matrix()
        board_value = np.sum(np.multiply(POSITION_VALUES, matrix_form)) * player_color
#        print("player color: " + str(player_color))
#        print("position values: \n" + str(POSITION_VALUES))
#        print("state values: \n" + str(matrix_form))
#        print("value: " + str(board_value))
        return (player_move_num - opponent_move_num) * 0.1 + board_value


if __name__ == "__main__":
    print("values: " + str(POSITION_VALUES))
    print("values(0, 0): " + str(POSITION_VALUES[(0, 0)]))
    print("values(4, 0): " + str(POSITION_VALUES[(4, 0)]))