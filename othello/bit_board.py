from board import Board
import numpy as np
import utilities

UP_DOWN_MASK = 0x00ffffffffffff00
LEFT_RIGHT_MASK = 0x7e7e7e7e7e7e7e7e
DIAGONAL_MASK = UP_DOWN_MASK & LEFT_RIGHT_MASK


class BitBoard(Board):
    def __init__(self, rows=8, columns=8, black_bit_board=None, white_bit_board=None):
        super(BitBoard, self).__init__()
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
        return self.generate_flip_pattern(move, player_color) != 0

    def apply_new_move(self, move, player_color):
        move_bit_board = self.board_with_stone_at(move)
        flip_pattern = self.generate_flip_pattern(move, player_color)
        if player_color == -1:
            self._black_bit_board ^= (move_bit_board | flip_pattern)
            self._white_bit_board ^= flip_pattern
        else:
            self._white_bit_board ^= (move_bit_board | flip_pattern)
            self._black_bit_board ^= flip_pattern

    def has_valid_move(self, color_number):
        return len(self.list_all_valid_moves(color_number)) != 0

    def is_end_state(self):
        return not self.has_valid_move(utilities.color_string_to_number('black')) \
            and not self.has_valid_move(utilities.color_string_to_number('white'))

    def is_empty_position(self, position):
        position_bit_board = self.board_with_stone_at(position)
        return position_bit_board & (self._black_bit_board | self._white_bit_board) == 0

    def list_all_valid_moves(self, color_number):
        moves = []
        (rows, columns) = self.shape
        for x in range(rows):
            for y in range(columns):
                move = (x, y)
                if self.is_valid_move(move, color_number):
                    moves.append(move)
        return moves

    def list_all_empty_positions(self):
        positions = []
        (rows, columns)=self.shape
        for x in range(rows):
            for y in range(columns):
                position=(x, y)
                if self.is_empty_position(position):
                    positions.append(position)
        return positions

    def generate_flip_pattern(self, move, player_color):
        flip_pattern=0
        if not self.is_empty_position(move):
            # Stone is already placed
            return flip_pattern
        move_bit_board=self.board_with_stone_at(move)
        flip_pattern=self.flip_pattern_vertically_up(move_bit_board, player_color) | \
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
            return ((bit_board << self._columns) & UP_DOWN_MASK)
        return self.flip_pattern_for_shifter_direction(move_bit_board, player_color, shifter)

    def flip_pattern_vertically_down(self, move_bit_board, player_color):
        def shifter(bit_board):
            return ((bit_board >> self._columns) & UP_DOWN_MASK)
        return self.flip_pattern_for_shifter_direction(move_bit_board, player_color, shifter)

    def flip_pattern_horizontally_left(self, move_bit_board, player_color):
        def shifter(bit_board):
            return ((bit_board << 1) & LEFT_RIGHT_MASK)
        return self.flip_pattern_for_shifter_direction(move_bit_board, player_color, shifter)

    def flip_pattern_horizontally_right(self, move_bit_board, player_color):
        def shifter(bit_board):
            return ((bit_board >> 1) & LEFT_RIGHT_MASK)
        return self.flip_pattern_for_shifter_direction(move_bit_board, player_color, shifter)

    def flip_pattern_diagonally_up_left(self, move_bit_board, player_color):
        def shifter(bit_board):
            return ((bit_board << (self._columns + 1)) & DIAGONAL_MASK)
        return self.flip_pattern_for_shifter_direction(move_bit_board, player_color, shifter)

    def flip_pattern_diagonally_up_right(self, move_bit_board, player_color):
        def shifter(bit_board):
            return ((bit_board << (self._columns - 1)) & DIAGONAL_MASK)
        return self.flip_pattern_for_shifter_direction(move_bit_board, player_color, shifter)

    def flip_pattern_diagonally_down_left(self, move_bit_board, player_color):
        def shifter(bit_board):
            return ((bit_board >> (self._columns - 1)) & DIAGONAL_MASK)
        return self.flip_pattern_for_shifter_direction(move_bit_board, player_color, shifter)

    def flip_pattern_diagonally_down_right(self, move_bit_board, player_color):
        def shifter(bit_board):
            return ((bit_board >> (self._columns + 1)) & DIAGONAL_MASK)
        return self.flip_pattern_for_shifter_direction(move_bit_board, player_color, shifter)

    def flip_pattern_for_shifter_direction(self, move_bit_board, player_color, shifter):
        flip_pattern=0
        mask=shifter(move_bit_board)
        (player_board, opponent_board)=self.select_players_and_opponents_board(
            player_color)
        while (mask != 0) and (mask & opponent_board != 0):
            flip_pattern |= mask
            mask = shifter(mask)
        if (player_board & mask) == 0:
            return 0
        else:
            return flip_pattern

    def select_players_and_opponents_board(self, player_color):
        player_board = self._black_bit_board if player_color == -1 else self._white_bit_board
        opponent_board = self._white_bit_board if player_color == - \
            1 else self._black_bit_board
        return (player_board, opponent_board)

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
        print("  ABCDEFGH")
        print(board)

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
        black = self._black_bit_board if player_color == 1 else self._white_bit_board
        white = self._white_bit_board if player_color == 1 else self._black_bit_board
        next_board = BitBoard(self._rows, self._columns, black, white)
        next_board.apply_new_move(move, player_color)
        return next_board


if __name__ == "__main__":
    bit_board = BitBoard()
    (black, white) = bit_board.generate_initial_board(8, 8)
    print('black: ')
    bit_board.print_bit_board(black)

    print('white: ')
    bit_board.print_bit_board(white)

    position = (2, 3)
    move = bit_board.board_with_stone_at(position)
    print('move' + str(position) + ':')
    bit_board.print_bit_board(move)

    print('flip pattern: ')
    flip = bit_board.generate_flip_pattern(
        position, -1)  # -1 stands for black
    bit_board.print_bit_board(flip)
