from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.button import Button
from board import Board
from othello_engine import OthelloEngine
from human_othello_player import HumanOthelloPlayer


class Othello(App):
    def build(self):
        rows = 8
        columns = 8
        self._board = self.setup_board(rows, columns)
        self._engine = OthelloEngine(HumanOthelloPlayer(self._board),
                                     HumanOthelloPlayer(self._board),
                                     rows,
                                     columns)
        self._engine.set_board_state_change_listener(
            self.on_state_change)
        self._root = BoxLayout(orientation='vertical')
        self._start_button = Button(text="start", size_hint=(0.5, 0.2))
        self._start_button.background_color = (0.7, 0.7, 0.7, 1.0)
        self._start_button.bind(on_press=self.on_start_press_listener)
        self._stop_button = Button(text="stop", size_hint=(0.5, 0.2))
        self._stop_button.background_color = (0.7, 0.7, 0.7, 1.0)
        self._stop_button.bind(on_press=self.on_stop_press_listener)
        self._root.add_widget(self._board)
        self._buttons = BoxLayout(orientation='horizontal')
        self._buttons.add_widget(self._start_button)
        self._buttons.add_widget(self._stop_button)
        self._root.add_widget(self._buttons)
        return self._root

    def setup_board(self, rows, columns):
        board = Board(board_rows=rows, board_columns=columns)
        return board

    def on_start_press_listener(self, button):
        self._engine.start_game()

    def on_stop_press_listener(self, button):
        self._engine.stop_game()

    def on_state_change(self, state):
        self._board.update_board(state)
