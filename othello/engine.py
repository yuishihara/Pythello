import numpy as np
import utilities
import threading
import time
from logging import getLogger
from matrix_board import MatrixBoard
from bit_board import BitBoard
from libfastbb import FastBitBoard

class Engine(object):
    def __init__(self, player_black, player_white, board_rows, board_columns):
        self._board_rows = board_rows
        self._board_columns = board_columns
        self._player_black = player_black
        self._player_black.set_color('black')
        self._player_white = player_white
        self._player_white.set_color('white')
        self._is_playing = False
        self._logger = getLogger(__name__)
        self._board_state_change_listener = None

    def reset(self):
        self._board_state = FastBitBoard(self._board_rows, self._board_columns) 
        self._is_playing = False

    def board_size(self):
        return (self._board_rows, self._board_columns)

    def board_state(self):
        return self._board_state

    def start_game(self):
        if self._is_playing:
            return
        #self._board_state = MatrixBoard(self._board_rows, self._board_columns)
        self._board_state = FastBitBoard(self._board_rows, self._board_columns) 
        self.notify_new_board_state(self._board_state.as_numpy_matrix())
        self._game_thread = threading.Thread(
            target=self.run_one_game, name='game_thread')
        self._game_thread.start()

    def run_one_game(self):
        transitions = [self._board_state.as_numpy_matrix()]
        self._is_playing = True
        while self._is_playing:
            stone_num = utilities.count_stone_num(self._board_state)
            self._logger.info('playing!! (black, white): %s', str(stone_num))
            if self._board_state.is_end_state():
                self._logger.info("No valid moves for both players. End of game: (black, white): %s", str(stone_num))
                break
            self.wait_player_move(self._player_black, self._board_state)
            transitions.append(self._board_state.as_numpy_matrix())
            if not self._is_playing:
                break
            before = time.time()
            self.wait_player_move(self._player_white, self._board_state)
            transitions.append(self._board_state.as_numpy_matrix())
            after = time.time()
            self._logger.debug("Time took for searching next move: %s", str(after - before))
        (black_stone, white_stone) = utilities.count_stone_num(self._board_state)
        winner = 'black' if black_stone > white_stone else 'white'
        return transitions, winner

    def wait_player_move(self, player, board_state):
        if not self.has_valid_move(player, board_state):
            self._logger.info("No valid moves for: " + player.color())
            return
        move = player.select_move(board_state)
        while not board_state.is_valid_move(move, player.color()) and self._is_playing:
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
        board_state = self._board_state
        board_state.apply_new_move(move, player.color())
        self.notify_new_board_state(self._board_state.as_numpy_matrix())

    def has_valid_move(self, player, board_state):
        return board_state.has_valid_move(player.color())

    def set_board_state_change_listener(self, listener):
        self._board_state_change_listener = listener

    def notify_new_board_state(self, state):
        if self._board_state_change_listener is not None:
            self._board_state_change_listener(state)
