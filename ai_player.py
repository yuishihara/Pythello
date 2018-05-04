from othello.player import Player
from othello import utilities


class AiPlayer(Player):
    def __init__(self, search_algorithm, evaluator):
        super(AiPlayer, self).__init__()
        self._search_algorithm = search_algorithm
        self._state_evaluator = evaluator

    def select_move(self, board_state):
        player_color = self.color()
        opponent_color = utilities.opponent_color(player_color)
        return self._search_algorithm.search_optimal_move(board_state,
                                                          self._state_evaluator,
                                                          player_color,
                                                          opponent_color)
