from logging import getLogger
from kivy.uix.button import Button
from kivy.uix.gridlayout import GridLayout
from kivy.graphics import Ellipse
from kivy.graphics import Color
from kivy.graphics.instructions import InstructionGroup
from othello import utilities


class Board(GridLayout):
    def __init__(self, board_rows, board_columns):
        assert board_rows == board_columns
        self._stone_name = 'stone'
        self._row_height = 80
        self._column_width = 80
        self._board_rows = board_rows
        self._board_columns = board_columns
        self._board_color = (0, 1, 0, 0.9)  # (r, g, b, a)
        self._buttons = {}
        self._board_press_listener = None
        self._logger = getLogger(__name__)
        super(Board, self).__init__(rows=self._board_rows, row_force_default=True, row_default_height=self._row_height,
                                    cols=self._board_columns, col_force_default=True, col_default_width=self._column_width)
        self.setup_board()

    def setup_board(self):
        for x in range(self._board_rows):
            for y in range(self._board_columns):
                button_id = self.position_to_id(x, y)
                button = Button(text=button_id, id=button_id)
                button.bind(on_press=self.on_press_callback)
                button.background_color = self._board_color
                self._buttons[button_id] = button
                self.add_widget(button)

    def on_press_callback(self, button):
        self._logger.debug('Button position: ' + str(button.pos))
        self._logger.debug('Pressed: ' + button.id)
        x, y = self.id_to_position(button.id)
        if self._board_press_listener is not None:
            self._board_press_listener(x, y)

    def set_on_board_press_listener(self, listener):
        self._board_press_listener = listener

    def update_board(self, matrix):
        for x in range(self._board_rows):
            for y in range(self._board_columns):
                button = self._buttons[self.position_to_id(x, y)]
                self.clear_previous_stone(button)
                status = matrix[x][y]
                if status == 0:
                    continue
                else:
                    color = utilities.color_number_to_string(status)
                    self.place_stone(x, y, color)

    def place_stone(self, x, y, color):
        button = self._buttons[self.position_to_id(x, y)]
        stone_size, stone_position = self.compute_stone_size_and_position(
            button)
        if color is 'black':
            stone = self.new_black_stone(stone_position, stone_size)
            button.canvas.add(stone)
        else:
            stone = self.new_white_stone(stone_position, stone_size)
            button.canvas.add(stone)

    def clear_previous_stone(self, button):
        button.canvas.remove_group(self._stone_name)

    def position_to_id(self, x, y):
        return str(x) + ' : ' + str(y)

    def id_to_position(self, id):
        splitted = id.split(':')
        x = int(splitted[0])
        y = int(splitted[1])
        self._logger.debug('id: ' + id + ' position: ' + str((x, y)))
        return (x, y)

    def new_white_stone(self, position, size):
        return self.new_stone(position, size, Color(1.0, 1.0, 1.0, 1))

    def new_black_stone(self, position, size):
        return self.new_stone(position, size, Color(0.0, 0.0, 0.0, 1))

    def new_stone(self, position, size, color):
        stone = InstructionGroup(group=self._stone_name)
        stone.add(color)
        stone.add(Ellipse(size=size, pos=position))
        return stone

    def compute_stone_size_and_position(self, button):
        stone_width = button.size[0] * 0.9
        stone_height = button.size[1] * 0.9
        stone_size = (stone_width, stone_height)
        stone_x = button.pos[0] + (button.size[0] - stone_width) / 2.0
        stone_y = button.pos[1] + (button.size[1] - stone_height) / 2.0
        stone_position = (stone_x, stone_y)
        return stone_size, stone_position
