import numpy as np
import utilities
import threading
import time
from matrix_board import MatrixBoard
from bit_board import BitBoard

class Engine(object):
    def __init__(self, player_black, player_white, board_rows, board_columns):
        self._board_rows = board_rows
        self._board_columns = board_columns
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
        #self._board_state = MatrixBoard(self._board_rows, self._board_columns)
        self._board_state = BitBoard(self._board_rows, self._board_columns) 
        self.notify_new_board_state(self._board_state.as_numpy_matrix())
        self._game_thread = threading.Thread(
            target=self.run_game, name='game_thread')
        self._game_thread.start()

    def run_game(self):
        while self._is_playing:
            print('playing!!')
            if self._board_state.is_end_state():
                print("No valid moves for both players. End of game")
                break
            self.wait_player_move(self._player_black, self._board_state)
            if not self._is_playing:
                return
            before = time.time()
            self.wait_player_move(self._player_white, self._board_state)
            after = time.time()
            print("Time took for searching next move: ", str(after - before))

    def wait_player_move(self, player, board_state):
        if not self.has_valid_move(player, board_state):
            print("No valid moves for: " + player.color())
            return
        move = player.select_move(board_state)
        color_number = utilities.color_string_to_number(player.color())
        while not board_state.is_valid_move(move, color_number) and self._is_playing:
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
        player_color = utilities.color_string_to_number(player.color())
        board_state = self._board_state
        board_state.apply_new_move(move, player_color)
        self.notify_new_board_state(self._board_state.as_numpy_matrix())

    def has_valid_move(self, player, board_state):
        color_number = utilities.color_string_to_number(player.color())
        return board_state.has_valid_move(color_number)

    def set_board_state_change_listener(self, listener):
        self._board_state_change_listener = listener

    def notify_new_board_state(self, state):
        self._board_state_change_listener(state)