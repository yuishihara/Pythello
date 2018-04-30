from othello.player import Player
from othello import utilities


class AiPlayer(Player):
    def __init__(self, search_algorithm, evaluator):
        super(AiPlayer, self).__init__()
        self._search_algorithm = search_algorithm
        self._state_evaluator = evaluator

    def select_move(self, board_state):
        color_number = utilities.color_string_to_number(self.color())
        return self._search_algorithm.search_optimal_move(board_state,
                                                          self._state_evaluator,
                                                          color_number)
