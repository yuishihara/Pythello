from search_algorithm import SearchAlgorithm


class AlphaBeta(SearchAlgorithm):
    def __init__(self):
        super(AlphaBeta, self).__init__()
        pass

    def search_optimal_move(self, board_state, state_evaluator, player_color, opponent_color):
        valid_moves = board_state.list_all_valid_moves(player_color)
        best_value = float('-infinity')
        best_move = valid_moves[0]
        search_depth = 4
        alpha = float('-infinity')
        beta = float('infinity')
        for move in valid_moves:
            # print('searching for move: ' + str(move))
            next_state = board_state.next_board_state(move, player_color)
            value = self.alpha_beta_search(next_state, state_evaluator,
                                           player_color, opponent_color,
                                           alpha, beta,
                                           search_depth, False)
            if best_value < value:
                best_value = value
                best_move = move
            # print('searched for move: ' + str(move) + ' best value: ' + str(best_value))
            alpha = max(alpha, best_value)
        return best_move

    def alpha_beta_search(self, board_state, state_evaluator,
                          player_color, opponent_color,
                          alpha, beta,
                          depth, maximize):
        if depth == 0 or board_state.is_end_state():
            return state_evaluator.evaluate(board_state, player_color, opponent_color)

        if not board_state.has_valid_move(player_color if maximize else opponent_color):
            return self.alpha_beta_search(
                board_state, state_evaluator, player_color, opponent_color, alpha, beta, depth - 1, not maximize)

        if maximize:
            best_value = float('-infinity')
            next_states = board_state.list_all_next_states(player_color)
            for next_state in next_states:
                best_value = max(best_value, self.alpha_beta_search(
                    next_state, state_evaluator, player_color, opponent_color, alpha, beta, depth - 1, False))
                alpha = max(alpha, best_value)
                if beta <= alpha:
                    break
            return best_value
        else:
            best_value = float('infinity')
            next_states = board_state.list_all_next_states(opponent_color)
            for next_state in next_states:
                best_value = min(best_value, self.alpha_beta_search(
                    next_state, state_evaluator, player_color, opponent_color, alpha, beta, depth - 1, True))
                beta = min(beta, best_value)
                if beta <= alpha:
                    break
            return best_value