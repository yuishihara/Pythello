import numpy as np
import utilities
from board import Board

# Othello board implementation based on numpy matrix(2d-array)


class MatrixBoard(Board):
    def __init__(self, rows=8, columns=8, board_state=None):
        super(MatrixBoard, self).__init__()
        if board_state is not None:
            assert board_state.shape == (rows, columns)
            self._board_state = board_state
        else:
            self._board_state = self.generate_initial_board_state(
                rows, columns)
        self.shape = self._board_state.shape

    def is_valid_move(self, move, player_color):
        if move == None:
            return False
        if not self.is_empty_position(move):
            # Stone is already placed
            return False
        if self.can_take_stones_vertically_up(move, player_color):
            return True
        if self.can_take_stones_vertically_down(move, player_color):
            return True
        if self.can_take_stones_horizontally_left(move, player_color):
            return True
        if self.can_take_stones_horizontally_right(move, player_color):
            return True
        if self.can_take_stones_diagonally_up_left(move, player_color):
            return True
        if self.can_take_stones_diagonally_up_right(move, player_color):
            return True
        if self.can_take_stones_diagonally_down_left(move, player_color):
            return True
        if self.can_take_stones_diagonally_down_right(move, player_color):
            return True
        return False

    def apply_new_move(self, move, player_color):
        if self.can_take_stones_vertically_up(move, player_color):
            self.flip_stones_vertically_up(move, player_color)
        if self.can_take_stones_vertically_down(move, player_color):
            self.flip_stones_vertically_down(move, player_color)
        if self.can_take_stones_horizontally_left(move, player_color):
            self.flip_stones_horizontally_left(move, player_color)
        if self.can_take_stones_horizontally_right(move, player_color):
            self.flip_stones_horizontally_right(move, player_color)
        if self.can_take_stones_diagonally_up_left(move, player_color):
            self.flip_stones_diagonally_up_left(move, player_color)
        if self.can_take_stones_diagonally_up_right(move, player_color):
            self.flip_stones_diagonally_up_right(move, player_color)
        if self.can_take_stones_diagonally_down_left(move, player_color):
            self.flip_stones_diagonally_down_left(move, player_color)
        if self.can_take_stones_diagonally_down_right(move, player_color):
            self.flip_stones_diagonally_down_right(move, player_color)
        self.place_stone_to(move, player_color)

    def flip_stones_vertically_up(self, move, player_color):
        def accumulator(x, y, step):
            return (x, y + step)
        return self.flip_stones_in_accumulator_direction(move, player_color, accumulator)

    def flip_stones_vertically_down(self, move, player_color):
        def accumulator(x, y, step):
            return (x, y - step)
        return self.flip_stones_in_accumulator_direction(move, player_color, accumulator)

    def flip_stones_horizontally_left(self, move, player_color):
        def accumulator(x, y, step):
            return (x - step, y)
        return self.flip_stones_in_accumulator_direction(move, player_color, accumulator)

    def flip_stones_horizontally_right(self, move, player_color):
        def accumulator(x, y, step):
            return (x + step, y)
        return self.flip_stones_in_accumulator_direction(move, player_color, accumulator)

    def flip_stones_diagonally_up_left(self, move, player_color):
        def accumulator(x, y, step):
            return (x - step, y + step)
        return self.flip_stones_in_accumulator_direction(move, player_color, accumulator)

    def flip_stones_diagonally_up_right(self, move, player_color):
        def accumulator(x, y, step):
            return (x + step, y + step)
        return self.flip_stones_in_accumulator_direction(move, player_color, accumulator)

    def flip_stones_diagonally_down_left(self, move, player_color):
        def accumulator(x, y, step):
            return (x - step, y - step)
        return self.flip_stones_in_accumulator_direction(move, player_color, accumulator)

    def flip_stones_diagonally_down_right(self, move, player_color):
        def accumulator(x, y, step):
            return (x + step, y - step)
        return self.flip_stones_in_accumulator_direction(move, player_color, accumulator)

    def flip_stones_in_accumulator_direction(self, move, player_color, accumulator):
        (x, y) = move
        (rows, columns) = self.shape
        for i in range(1, max(rows, columns), 1):
            position = accumulator(x, y, i)
            if self.is_out_of_board(position):
                break
            if not self.flip_stone_at(position, player_color):
                break

    def can_take_stones_vertically_up(self, move, player_color):
        def accumulator(x, y, step):
            return (x, y + step)
        return self.can_take_stone_in_accumulator_direction(move, player_color, accumulator)

    def can_take_stones_vertically_down(self, move, player_color):
        def accumulator(x, y, step):
            return (x, y - step)
        return self.can_take_stone_in_accumulator_direction(move, player_color, accumulator)

    def can_take_stones_horizontally_left(self, move, player_color):
        def accumulator(x, y, step):
            return (x - step, y)
        return self.can_take_stone_in_accumulator_direction(move, player_color, accumulator)

    def can_take_stones_horizontally_right(self, move, player_color):
        def accumulator(x, y, step):
            return (x + step, y)
        return self.can_take_stone_in_accumulator_direction(move, player_color, accumulator)

    def can_take_stones_diagonally_up_left(self, move, player_color):
        def accumulator(x, y, step):
            return (x - step, y + step)
        return self.can_take_stone_in_accumulator_direction(move, player_color, accumulator)

    def can_take_stones_diagonally_up_right(self, move, player_color):
        def accumulator(x, y, step):
            return (x + step, y + step)
        return self.can_take_stone_in_accumulator_direction(move, player_color, accumulator)

    def can_take_stones_diagonally_down_left(self, move, player_color):
        def accumulator(x, y, step):
            return (x - step, y - step)
        return self.can_take_stone_in_accumulator_direction(move, player_color, accumulator)

    def can_take_stones_diagonally_down_right(self, move, player_color):
        def accumulator(x, y, step):
            return (x + step, y - step)
        return self.can_take_stone_in_accumulator_direction(move, player_color, accumulator)

    def can_take_stone_in_accumulator_direction(self, move, player_color, accumulator):
        (x, y) = move
        (rows, columns) = self._board_state.shape
        color_number = utilities.color_string_to_number(player_color)
        for i in range(1, max(rows, columns), 1):
            position = accumulator(x, y, i)
            if self.is_out_of_board(position) or self.is_empty_position(position):
                break
            if (self._board_state[position] == color_number):
                if i != 1:
                    return True
                else:
                    return False
        return False

    def has_valid_move(self, player_color):
        return len(self.list_all_valid_moves(player_color)) != 0

    def is_end_state(self):
        return not self.has_valid_move('black') and not self.has_valid_move('white')

    def is_out_of_board(self, position):
        (x, y) = position
        (rows, columns) = self._board_state.shape
        return (x < 0 or y < 0 or rows <= x or columns <= y)

    def is_empty_position(self, position):
        return self._board_state[position] == 0

    def list_all_valid_moves(self, player_color):
        empty_positions = self.list_all_empty_positions()
        valid_moves = []
        for move in empty_positions:
            if self.is_valid_move(move, player_color):
                valid_moves.append(move)
        return valid_moves

    def list_all_next_states(self, player_color):
        empty_positions = self.list_all_empty_positions()
        next_states = []
        for move in empty_positions:
            if self.is_valid_move(move, player_color):
                next_states.append(self.next_board_state(move, player_color))
        return next_states

    def list_all_empty_positions(self):
        positions = []
        (rows, columns) = self._board_state.shape
        for x in range(rows):
            for y in range(columns):
                position = (x, y)
                if self.is_empty_position(position):
                    positions.append(position)
        return positions

    def next_board_state(self, move, player_color):
        color_number = utilities.color_string_to_number(player_color)
        next_state = np.copy(self._board_state)
        next_state[move] = color_number
        return MatrixBoard(board_state=next_state)

    def generate_initial_board_state(self, rows, columns):
        board_state = np.zeros(
            shape=(rows, columns), dtype='int32')
        x_center = rows / 2
        y_center = columns / 2
        board_state[(x_center - 1, y_center)] = -1
        board_state[(x_center, y_center)] = 1
        board_state[(x_center, y_center - 1)] = -1
        board_state[(x_center - 1, y_center - 1)] = 1
        return board_state

    def place_stone_to(self, position, player_color):
        self._board_state[position] = utilities.color_string_to_number(
            player_color)

    def flip_stone_at(self, position, player_color):
        color_number = utilities.color_string_to_number(player_color)
        if self._board_state[position] != color_number:
            self._board_state[position] = color_number
            return True
        else:
            return False

    def as_numpy_matrix(self):
        return self._board_state
