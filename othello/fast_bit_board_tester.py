from board import Board
from logging import getLogger, DEBUG, basicConfig
from libfastbb import FastBitBoard
import numpy as np
import utilities


class FastBitBoardTester(Board):
    def __init__(self, rows=8, columns=8):
        super(FastBitBoardTester, self).__init__()
        self._impl = FastBitBoard()
        self._rows = rows
        self._columns = columns
        self._logger = getLogger(__name__)
        self.shape = (rows, columns)

    def is_valid_move(self, move, player_color):
        return self._impl.is_valid_move(move, player_color)

    def apply_new_move(self, move, player_color):
        return self._impl.apply_valid_move(move, player_color)

    def has_valid_move(self, player_color):
        return self._impl.has_valid_move(player_color)

    def is_end_state(self):
        return self._impl.is_end_state()

    def is_empty_position(self, position):
        return self._impl.is_empty_position(position)

    def list_all_valid_moves(self, player_color):
        return self._impl.list_all_valid_moves(player_color)

    def list_all_next_states(self, player_color):
        return self._impl.list_all_next_states(player_color)

    def list_all_empty_positions(self):
        return self._impl.list_all_empty_positions()

    def print_bit_board(self, binary):
        binary_string = str(
            format(binary, '0' + str(self._rows * self._columns) + 'b'))
        board = ''
        for i in range(self._rows):
            board += str(i) + ":" + \
                binary_string[i * self._columns: (i + 1) * self._columns]
            board += '\n'
        self._logger.info("\n  ABCDEFGH\n" + board)

    def as_numpy_matrix(self):
        return self._impl.as_numpy_matrix()

    def next_board_state(self, move, player_color):
        return self._impl.next_board_state(move, player_color)


if __name__ == "__main__":
    basicConfig(level=DEBUG)
    logger = getLogger(__name__)

    fast_bb = FastBitBoardTester()
    logger.info("As numpy:\n %s", str(fast_bb.as_numpy_matrix()))

    next_states = fast_bb.list_all_next_states('black')
    for state in next_states:
        logger.info("Next state:\n %s", str(state.as_numpy_matrix()))
