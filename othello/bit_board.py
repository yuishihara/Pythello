from board import Board
from logging import getLogger, DEBUG, basicConfig
import numpy as np
import utilities

UP_DOWN_MASK = 0x00ffffffffffff00
LEFT_RIGHT_MASK = 0x7e7e7e7e7e7e7e7e
DIAGONAL_MASK = UP_DOWN_MASK & LEFT_RIGHT_MASK


class BitBoard(Board):
    def __init__(self, rows=8, columns=8, black_bit_board=None, white_bit_board=None):
        super(BitBoard, self).__init__()
        self._logger = getLogger(__name__)
        self._rows = rows
        self._columns = columns

        if black_bit_board is not None and white_bit_board is not None:
            self._black_bit_board = black_bit_board
            self._white_bit_board = white_bit_board
        else:
            self._black_bit_board, self._white_bit_board = self.generate_initial_board(
                rows, columns)
        self.shape = (rows, columns)

    def generate_initial_board(self, rows, columns):
        x_center = rows / 2
        y_center = columns / 2
        black = self.board_with_stone_at(
            (x_center, y_center - 1)) | self.board_with_stone_at((x_center - 1, y_center))
        white = self.board_with_stone_at(
            (x_center, y_center)) | self.board_with_stone_at((x_center - 1, y_center - 1))
        return (black, white)

    def is_valid_move(self, move, player_color):
        if not self.is_empty_position(move):
            return False
        return self.generate_flip_pattern(move, player_color) != 0

    def apply_new_move(self, move, player_color):
        flip_pattern = self.generate_flip_pattern(move, player_color)
        if flip_pattern == 0:
            return
        move_bit_board = self.board_with_stone_at(move)
        if player_color == 'black':
            self._black_bit_board ^= (move_bit_board | flip_pattern)
            self._white_bit_board ^= flip_pattern
        else:
            self._white_bit_board ^= (move_bit_board | flip_pattern)
            self._black_bit_board ^= flip_pattern

    def has_valid_move(self, player_color):
        return len(self.list_all_valid_moves(player_color)) != 0

    def is_end_state(self):
        return not self.has_valid_move('black') and not self.has_valid_move('white')

    def is_empty_position(self, position):
        position_bit_board = self.board_with_stone_at(position)
        return position_bit_board & (self._black_bit_board | self._white_bit_board) == 0

    def list_all_valid_moves(self, player_color):
        moves = []
        (rows, columns) = self.shape
        for x in range(rows):
            for y in range(columns):
                move = (x, y)
                if self.is_valid_move(move, player_color):
                    moves.append(move)
        return moves

    def list_all_next_states(self, player_color):
        states = []
        (rows, columns) = self.shape
        for x in range(rows):
            for y in range(columns):
                move = (x, y)
                if not self.is_empty_position(move):
                    continue
                next_state = self.next_board_state(move, player_color)
                if self.is_same_board_state(next_state):
                    continue
                states.append(next_state)
        return states

    def list_all_empty_positions(self):
        positions = []
        (rows, columns) = self.shape
        for x in range(rows):
            for y in range(columns):
                position = (x, y)
                if self.is_empty_position(position):
                    positions.append(position)
        return positions

    def generate_flip_pattern(self, move, player_color):
        flip_pattern = 0
        if not self.is_empty_position(move):
            # Stone is already placed
            return flip_pattern
        move_bit_board = self.board_with_stone_at(move)
        flip_pattern = self.flip_pattern_vertically_up(move_bit_board, player_color) | \
            self.flip_pattern_vertically_down(move_bit_board, player_color) | \
            self.flip_pattern_horizontally_left(move_bit_board, player_color) | \
            self.flip_pattern_horizontally_right(move_bit_board, player_color) | \
            self.flip_pattern_diagonally_up_left(move_bit_board, player_color) | \
            self.flip_pattern_diagonally_up_right(move_bit_board, player_color) | \
            self.flip_pattern_diagonally_down_left(move_bit_board, player_color) | \
            self.flip_pattern_diagonally_down_right(
                move_bit_board, player_color)
        return flip_pattern

    def flip_pattern_vertically_up(self, move_bit_board, player_color):
        def shifter(bit_board):
            return (bit_board << self._columns)
        return self.flip_pattern_for_shifter_direction(move_bit_board, player_color, shifter, UP_DOWN_MASK)

    def flip_pattern_vertically_down(self, move_bit_board, player_color):
        def shifter(bit_board):
            return (bit_board >> self._columns)
        return self.flip_pattern_for_shifter_direction(move_bit_board, player_color, shifter, UP_DOWN_MASK)

    def flip_pattern_horizontally_left(self, move_bit_board, player_color):
        def shifter(bit_board):
            return (bit_board << 1)
        return self.flip_pattern_for_shifter_direction(move_bit_board, player_color, shifter, LEFT_RIGHT_MASK)

    def flip_pattern_horizontally_right(self, move_bit_board, player_color):
        def shifter(bit_board):
            return (bit_board >> 1)
        return self.flip_pattern_for_shifter_direction(move_bit_board, player_color, shifter, LEFT_RIGHT_MASK)

    def flip_pattern_diagonally_up_left(self, move_bit_board, player_color):
        def shifter(bit_board):
            return (bit_board << (self._columns + 1))
        return self.flip_pattern_for_shifter_direction(move_bit_board, player_color, shifter, DIAGONAL_MASK)

    def flip_pattern_diagonally_up_right(self, move_bit_board, player_color):
        def shifter(bit_board):
            return (bit_board << (self._columns - 1))
        return self.flip_pattern_for_shifter_direction(move_bit_board, player_color, shifter, DIAGONAL_MASK)

    def flip_pattern_diagonally_down_left(self, move_bit_board, player_color):
        def shifter(bit_board):
            return (bit_board >> (self._columns - 1))
        return self.flip_pattern_for_shifter_direction(move_bit_board, player_color, shifter, DIAGONAL_MASK)

    def flip_pattern_diagonally_down_right(self, move_bit_board, player_color):
        def shifter(bit_board):
            return (bit_board >> (self._columns + 1))
        return self.flip_pattern_for_shifter_direction(move_bit_board, player_color, shifter, DIAGONAL_MASK)

    def flip_pattern_for_shifter_direction(self, move_bit_board, player_color, shifter, mask):
        flip_pattern = 0
        shifted_move = shifter(move_bit_board)
        (player_board, opponent_board) = self.select_players_and_opponents_board(
            player_color)
        masked_opponent_board = mask & opponent_board
        while (shifted_move != 0) and (shifted_move & masked_opponent_board != 0):
            flip_pattern |= shifted_move
            shifted_move = shifter(shifted_move)
        if (player_board & shifted_move) == 0:
            return 0
        else:
            return flip_pattern

    def select_players_and_opponents_board(self, player_color):
        if player_color == 'black':
            return (self._black_bit_board, self._white_bit_board)
        else:
            return (self._white_bit_board, self._black_bit_board)

    def board_with_stone_at(self, position):
        (row, column) = position
        assert row < self._rows and column < self._columns
        board = 1 << ((self._rows - row - 1) * self._rows +
                      (self._columns - column - 1))
        return board

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
        matrix = np.zeros(self.shape)
        for x in range(self._columns):
            for y in range(self._rows):
                position = (x, y)
                matrix[position] = self.color_of(position)
        return matrix

    def color_of(self, position):
        mask = self.board_with_stone_at(position)
        if mask & self._black_bit_board != 0:
            return -1
        elif mask & self._white_bit_board != 0:
            return 1
        else:
            return 0

    def next_board_state(self, move, player_color):
        black = self._black_bit_board
        white = self._white_bit_board
        next_board = BitBoard(self._rows, self._columns, black, white)
        next_board.apply_new_move(move, player_color)
        return next_board

    def is_same_board_state(self, state_to_compare):
        current_board = self._black_bit_board | self._white_bit_board
        target_board = state_to_compare._black_bit_board | state_to_compare._white_bit_board
        return current_board == target_board


if __name__ == "__main__":
    basicConfig(level=DEBUG)
    logger = getLogger(__name__)
    bit_board = BitBoard()
    (black, white) = bit_board.generate_initial_board(8, 8)
    logger.info('black: ')
    bit_board.print_bit_board(black)

    logger.info('white: ')
    bit_board.print_bit_board(white)

    position = (5, 4)
    move = bit_board.board_with_stone_at(position)
    logger.info('move' + str(position) + ':')
    bit_board.print_bit_board(move)

    logger.info('flip pattern: ')
    flip = bit_board.generate_flip_pattern(
        position, -1)  # -1 stands for black
    bit_board.print_bit_board(flip)
