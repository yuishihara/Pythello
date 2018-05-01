from search_algorithm import SearchAlgorithm
class AlphaBeta(SearchAlgorithm):
    def __init__(self):
        super(AlphaBeta, self).__init__()
        pass

    def search_optimal_move(self, board_state, state_evaluator, player_color):
        valid_moves = board_state.list_all_valid_moves(player_color)
        best_value = float('-infinity')
        best_move = valid_moves[0]
        search_depth = 4
        alpha = float('-infinity')
        beta = float('infinity')
        for move in valid_moves:
            best_value = self.alpha_beta_search(board_state, state_evaluator,
                                                player_color, player_color * -1,
                                                alpha, beta,
                                                search_depth, True)
            if alpha < best_value: 
                alpha = max(alpha, best_value)
                best_move = move
            if beta <= alpha:
                break
        return best_move

    def alpha_beta_search(self, board_state, state_evaluator,
                          player_color, opponent_color,
                          alpha, beta,
                          depth, maximize):
        if depth == 0 or board_state.is_end_state():
            return state_evaluator.evaluate(board_state, player_color)

        if not board_state.has_valid_move(player_color if maximize else opponent_color):
            return self.alpha_beta_search(
                board_state, state_evaluator, player_color, opponent_color, alpha, beta, depth - 1, not maximize)

        if maximize:
            best_value = float('-infinity')
            valid_moves = board_state.list_all_valid_moves(player_color)
            for move in valid_moves:
                next_state = board_state.next_board_state(move, player_color)
                best_value = self.alpha_beta_search(
                    next_state, state_evaluator, player_color, opponent_color, alpha, beta, depth - 1, False)
                alpha = max(alpha, best_value)
                if beta <= alpha:
                    break
            return best_value
        else:
            best_value = float('infinity')
            valid_moves = board_state.list_all_valid_moves(opponent_color)
            for move in valid_moves:
                next_state = board_state.next_board_state(move, opponent_color)
                best_value = self.alpha_beta_search(
                    next_state, state_evaluator, player_color, opponent_color, alpha, beta, depth - 1, True)
                beta = min(beta, best_value)
                if beta <= alpha:
                    break
            return best_value
