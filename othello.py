from kivy.app import App
from board import Board
import numpy as np

class Othello(App):
    def build(self):
        self.board = self.setup_board()
        self._board_status = np.zeros(shape=(self.board_rows, self.board_columns), dtype='int32')
        self._board_status[(3, 4)] = -1
        self._board_status[(4, 4)] = 1
        self._board_status[(4, 3)] = -1
        self._board_status[(3, 3)] = 1
        return self.board

    def setup_board(self):
        self.board_rows = 8
        self.board_columns = 8
        board = Board(board_rows=self.board_rows, board_columns=self.board_columns)
        board.set_on_board_press_listener(self.on_board_press_listener)
        return board

    def on_board_press_listener(self, x, y):
        print('Othello!!! x: ' + str(x) + " y: " + str(y))
        self.board.update_board(self._board_status)
