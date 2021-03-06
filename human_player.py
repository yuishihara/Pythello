import threading
from logging import getLogger
from othello.player import Player

class HumanPlayer(Player):
    def __init__(self, board):
        super(HumanPlayer, self).__init__()
        self._board = board
        self._selected_move = None
        self._lock = threading.Condition()
        self._logger = getLogger(__name__)

    def select_move(self, board_state):
        self._board.set_on_board_press_listener(self.on_board_pressed)
        try:
            with self._lock:
                self._lock.wait()
        except Exception as e:
            self._logger.error("Exception occurred while waiting for player's move!")
        return self._selected_move

    def on_board_pressed(self, x, y):
        self._board.set_on_board_press_listener(None)
        self._selected_move = (x, y)
        with self._lock:
            self._lock.notify_all()

    def force_kill(self):
        with self._lock:
            self._lock.notify_all()

