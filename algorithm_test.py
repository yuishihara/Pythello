import time
import numpy as np
from othello.ai.alpha_beta import AlphaBeta
from othello.ai.minimax import MiniMax
from othello.ai.evaluator import Evaluator
from othello.bit_board import BitBoard


def algorithm_sanity_check(board_state, evaluator, player_color, opponent_color, depth):
    # Check that algorithms return same result
    alpha_beta = AlphaBeta()
    alpha_beta_best_move = alpha_beta.search_optimal_move(
        board_state, evaluator, player_color, opponent_color, depth)
    minimax = MiniMax()
    minimax_best_move = minimax.search_optimal_move(
        board_state, evaluator, player_color, opponent_color, depth)

    assert alpha_beta_best_move == minimax_best_move


def speed_test(board_state, evaluator, player_color, opponent_color, depth):
    def run_alpha_beta():
        alpha_beta = AlphaBeta()
        alpha_beta.search_optimal_move(
            board_state, evaluator, player_color, opponent_color, depth)
    alpha_beta_time = measure_performance(run_alpha_beta)
    print('AlphaBeta algorithm took(depth = ' +
          str(depth) + '): ' + str(alpha_beta_time) + 's')

    def run_minimax():
        minimax = MiniMax()
        minimax.search_optimal_move(
            board_state, evaluator, player_color, opponent_color, depth)
    minimax_time = measure_performance(run_minimax)
    print('MiniMax algorithm took(depth = ' +
          str(depth) + '): ' + str(minimax_time) + 's')

    print('AlphaBeta is faster than Minimax algorithm for(depth = ' + str(depth) + '): ' +
          str((minimax_time/alpha_beta_time) * 100) + '%')
    return (alpha_beta_time, minimax_time)


def measure_performance(target_function):
    results = []
    for _ in range(10):
        before = time.time()
        target_function()
        after = time.time()
        results.append(after - before)
    return np.average(results)


if __name__ == '__main__':
    board_state = BitBoard()
    evaluator = Evaluator()
    player_color = 'black'
    opponent_color = 'white'

    algorithm_sanity_check(board_state, evaluator,
                           player_color, opponent_color, depth=4)

    results = []
    for depth in range(1, 6):
        result = speed_test(board_state, evaluator,
                            player_color, opponent_color, depth=depth)
        results.append(result)
