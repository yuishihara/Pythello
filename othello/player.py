class Player(object):
    def __init__(self):
        pass

    def set_color(self, color):
        self._color = color

    def color(self):
        return self._color

    def select_move(self, board_state):
        pass

    def force_kill(self):
        pass
