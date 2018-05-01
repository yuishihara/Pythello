from search_algorithm import SearchAlgorithm


class MiniMax(SearchAlgorithm):
    def __init__(self):
        super(MiniMax, self).__init__()

    def search_optimal_move(self, board_state, state_evaluator, player_color):
        valid_moves = board_state.list_all_valid_moves(player_color)
        best_value = float('-infinity')
        best_move = valid_moves[0]
        search_depth = 4
        for move in valid_moves:
            value = self.minimax_search(
                board_state, state_evaluator, player_color, player_color * -1, search_depth, True)
            if best_value < value:
                best_value = value
                best_move = move
        return best_move

    def minimax_search(self, board_state, state_evaluator,
                       player_color, opponent_color, depth, maximize):
        if depth == 0 or board_state.is_end_state():
            return state_evaluator.evaluate(board_state, player_color)

        if not board_state.has_valid_move(player_color if maximize else opponent_color):
            return self.minimax_search(
                board_state, state_evaluator, player_color, opponent_color, depth - 1, not maximize)

        if maximize:
            best_value = float('-infinity')
            valid_moves = board_state.list_all_valid_moves(player_color)
            for move in valid_moves:
                next_state = board_state.next_board_state(move, player_color)
                value = self.minimax_search(
                    next_state, state_evaluator, player_color, opponent_color, depth - 1, False)
                best_value = max(best_value, value)
            return best_value
        else:
            best_value = float('infinity')
            valid_moves = board_state.list_all_valid_moves(opponent_color)
            for move in valid_moves:
                next_state = board_state.next_board_state(move, opponent_color)
                value = self.minimax_search(
                    next_state, state_evaluator, player_color, opponent_color, depth - 1, True)
                best_value = min(best_value, value)
            return best_value