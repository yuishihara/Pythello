import numpy as np
import threading


class OthelloEngine(object):
    def __init__(self, player_black, player_white, board_rows, board_columns):
        self._board_rows = board_rows
        self._board_columns = board_columns
        self._board_state = self.generate_initial_board_state()
        self._player_black = player_black
        self._player_black.set_color('black')
        self._player_white = player_white
        self._player_white.set_color('white')
        self._is_playing = False

    def reset(self):
        pass

    def board_size(self):
        return (self._board_rows, self._board_columns)

    def board_state(self):
        return self._board_state

    def start_game(self):
        if self._is_playing:
            return
        self._is_playing = True
        self._board_state = self.generate_initial_board_state()
        self.notify_new_board_state(self._board_state)
        self._game_thread = threading.Thread(
            target=self.run_game, name='game_thread')
        self._game_thread.start()

    def run_game(self):
        while self._is_playing:
            print('playing!!')
            if not self.has_valid_move(self._player_black, self._board_state) and \
                    not self.has_valid_move(self._player_white, self._board_state):
                print("No valid moves for both players. End of game")
                break
            self.wait_player_move(self._player_black, self._board_state)
            if not self._is_playing:
                return
            self.wait_player_move(self._player_white, self._board_state)

    def wait_player_move(self, player, board_state):
        if not self.has_valid_move(player, board_state):
            print("No valid moves for: " + player.color())
            return
        move = player.select_move(board_state)
        while not self.is_valid_move(move, board_state, player.color()) and self._is_playing:
            move = player.select_move(board_state)
        if move is not None:
            self.apply_new_move(move, player)

    def stop_game(self):
        if not self._is_playing:
            return
        self._is_playing = False
        self._player_black.force_kill()
        self._player_white.force_kill()
        self._game_thread.kill_received = True

    def apply_new_move(self, move, player):
        player_color = -1 if player.color() == 'black' else 1
        opponent_color = player_color * -1
        board_state = self._board_state
        if self.can_take_stones_vertically_up(move, board_state, player_color):
            self.flip_stones_vertically_up(
                move, board_state, player_color, opponent_color)
        if self.can_take_stones_vertically_down(move, board_state, player_color):
            self.flip_stones_vertically_down(
                move, board_state, player_color, opponent_color)
        if self.can_take_stones_horizontally_left(move, board_state, player_color):
            self.flip_stones_horizontally_left(
                move, board_state, player_color, opponent_color)
        if self.can_take_stones_horizontally_right(move, board_state, player_color):
            self.flip_stones_horizontally_right(
                move, board_state, player_color, opponent_color)
        if self.can_take_stones_diagonally_up_left(move, board_state, player_color):
            self.flip_stones_diagonally_up_left(
                move, board_state, player_color, opponent_color)
        if self.can_take_stones_diagonally_up_right(move, board_state, player_color):
            self.flip_stones_diagonally_up_right(
                move, board_state, player_color, opponent_color)
        if self.can_take_stones_diagonally_down_left(move, board_state, player_color):
            self.flip_stones_diagonally_down_left(
                move, board_state, player_color, opponent_color)
        if self.can_take_stones_diagonally_down_right(move, board_state, player_color):
            self.flip_stones_diagonally_down_right(
                move, board_state, player_color, opponent_color)
        board_state[move] = player_color
        self.notify_new_board_state(self._board_state)

    def is_valid_move(self, move, board_state, color):
        if move == None:
            return False
        (x, y) = move
        if board_state[(x, y)] != 0:
            # Stone is already placed
            return False
        player_color = (-1 if (color == 'black') else 1)
        if self.can_take_stones_vertically_up(move, board_state, player_color):
            return True
        if self.can_take_stones_vertically_down(move, board_state, player_color):
            return True
        if self.can_take_stones_horizontally_left(move, board_state, player_color):
            return True
        if self.can_take_stones_horizontally_right(move, board_state, player_color):
            return True
        if self.can_take_stones_diagonally_up_left(move, board_state, player_color):
            return True
        if self.can_take_stones_diagonally_up_right(move, board_state, player_color):
            return True
        if self.can_take_stones_diagonally_down_left(move, board_state, player_color):
            return True
        if self.can_take_stones_diagonally_down_right(move, board_state, player_color):
            return True
        return False

    def flip_stones_vertically_up(self, move, board_state, player_color, opponent_color):
        def accumulator(x, y, step):
            return (x, y + step)
        return self.flip_stones_in_accumulator_direction(move, board_state, player_color, opponent_color, accumulator)

    def flip_stones_vertically_down(self, move, board_state, player_color, opponent_color):
        def accumulator(x, y, step):
            return (x, y - step)
        return self.flip_stones_in_accumulator_direction(move, board_state, player_color, opponent_color, accumulator)

    def flip_stones_horizontally_left(self, move, board_state, player_color, opponent_color):
        def accumulator(x, y, step):
            return (x - step, y)
        return self.flip_stones_in_accumulator_direction(move, board_state, player_color, opponent_color, accumulator)

    def flip_stones_horizontally_right(self, move, board_state, player_color, opponent_color):
        def accumulator(x, y, step):
            return (x + step, y)
        return self.flip_stones_in_accumulator_direction(move, board_state, player_color, opponent_color, accumulator)

    def flip_stones_diagonally_up_left(self, move, board_state, player_color, opponent_color):
        def accumulator(x, y, step):
            return (x - step, y + step)
        return self.flip_stones_in_accumulator_direction(move, board_state, player_color, opponent_color, accumulator)

    def flip_stones_diagonally_up_right(self, move, board_state, player_color, opponent_color):
        def accumulator(x, y, step):
            return (x + step, y + step)
        return self.flip_stones_in_accumulator_direction(move, board_state, player_color, opponent_color, accumulator)

    def flip_stones_diagonally_down_left(self, move, board_state, player_color, opponent_color):
        def accumulator(x, y, step):
            return (x - step, y - step)
        return self.flip_stones_in_accumulator_direction(move, board_state, player_color, opponent_color, accumulator)

    def flip_stones_diagonally_down_right(self, move, board_state, player_color, opponent_color):
        def accumulator(x, y, step):
            return (x + step, y - step)
        return self.flip_stones_in_accumulator_direction(move, board_state, player_color, opponent_color, accumulator)

    def flip_stones_in_accumulator_direction(self, move, board_state, player_color, opponent_color, accumulator):
        (x, y) = move
        for i in range(1, max(self._board_rows, self._board_columns), 1):
            position = accumulator(x, y, i)
            if self.is_out_of_board(position):
                break
            if board_state[position] == opponent_color:
                board_state[position] = player_color
            else:
                break

    def can_take_stones_vertically_up(self, move, board_state, player_color):
        def accumulator(x, y, step):
            return (x, y + step)
        return self.can_take_stone_in_accumulator_direction(move, board_state, player_color, accumulator)

    def can_take_stones_vertically_down(self, move, board_state, player_color):
        def accumulator(x, y, step):
            return (x, y - step)
        return self.can_take_stone_in_accumulator_direction(move, board_state, player_color, accumulator)

    def can_take_stones_horizontally_left(self, move, board_state, player_color):
        def accumulator(x, y, step):
            return (x - step, y)
        return self.can_take_stone_in_accumulator_direction(move, board_state, player_color, accumulator)

    def can_take_stones_horizontally_right(self, move, board_state, player_color):
        def accumulator(x, y, step):
            return (x + step, y)
        return self.can_take_stone_in_accumulator_direction(move, board_state, player_color, accumulator)

    def can_take_stones_diagonally_up_left(self, move, board_state, player_color):
        def accumulator(x, y, step):
            return (x - step, y + step)
        return self.can_take_stone_in_accumulator_direction(move, board_state, player_color, accumulator)

    def can_take_stones_diagonally_up_right(self, move, board_state, player_color):
        def accumulator(x, y, step):
            return (x + step, y + step)
        return self.can_take_stone_in_accumulator_direction(move, board_state, player_color, accumulator)

    def can_take_stones_diagonally_down_left(self, move, board_state, player_color):
        def accumulator(x, y, step):
            return (x - step, y - step)
        return self.can_take_stone_in_accumulator_direction(move, board_state, player_color, accumulator)

    def can_take_stones_diagonally_down_right(self, move, board_state, player_color):
        def accumulator(x, y, step):
            return (x + step, y - step)
        return self.can_take_stone_in_accumulator_direction(move, board_state, player_color, accumulator)

    def can_take_stone_in_accumulator_direction(self, move, board_state, player_color, accumulator):
        (x, y) = move
        # check diagonal
        for i in range(1, max(self._board_rows, self._board_columns), 1):
            position = accumulator(x, y, i)
            if self.is_out_of_board(position) or board_state[position] == 0:
                break
            if (board_state[position] == player_color):
                if i != 1:
                    return True
                else:
                    return False
        return False

    def has_valid_move(self, player, board_state):
        empty_positions = self.list_all_empty_positions(board_state)
        for move in empty_positions:
            if self.is_valid_move(move, board_state, player.color()):
                return True
        return False

    def list_all_empty_positions(self, board_state):
        positions = []
        for x in range(self._board_rows):
            for y in range(self._board_columns):
                if board_state[(x, y)] == 0:
                    positions.append((x, y))
        return positions

    def is_out_of_board(self, position):
        (x, y) = position
        return (x < 0 or y < 0 or self._board_rows <= x or self._board_columns <= y)

    def set_board_state_change_listener(self, listener):
        self._board_state_change_listener = listener

    def notify_new_board_state(self, state):
        self._board_state_change_listener(state)

    def generate_initial_board_state(self):
        board_state = np.zeros(
            shape=(self._board_rows, self._board_columns), dtype='int32')
        x_center = self._board_rows / 2
        y_center = self._board_columns / 2
        board_state[(x_center - 1, y_center)] = -1
        board_state[(x_center, y_center)] = 1
        board_state[(x_center, y_center - 1)] = -1
        board_state[(x_center - 1, y_center - 1)] = 1
        return board_state
