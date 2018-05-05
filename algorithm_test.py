import time
import numpy as np
from logging import getLogger, INFO, basicConfig 
from othello.ai.alpha_beta import AlphaBeta
from othello.ai.minimax import MiniMax
from othello.ai.evaluator import Evaluator
from othello.bit_board import BitBoard
from othello.matrix_board import MatrixBoard


def algorithm_sanity_check(board_state, evaluator, player_color, opponent_color, depth):
    # Check that algorithms return same result
    alpha_beta = AlphaBeta()
    alpha_beta_best_move = alpha_beta.search_optimal_move(
        board_state, evaluator, player_color, opponent_color, depth)
    minimax = MiniMax()
    minimax_best_move = minimax.search_optimal_move(
        board_state, evaluator, player_color, opponent_color, depth)

    assert alpha_beta_best_move == minimax_best_move


def algorithm_performance_test(board_state, evaluator, player_color, opponent_color, depth):
    logger = getLogger(__name__)
    def run_alpha_beta():
        alpha_beta = AlphaBeta()
        alpha_beta.search_optimal_move(
            board_state, evaluator, player_color, opponent_color, depth)
    alpha_beta_time = measure_performance(run_alpha_beta)
    logger.info('AlphaBeta algorithm took(depth = ' +
          str(depth) + '): ' + str(alpha_beta_time) + 's')

    def run_minimax():
        minimax = MiniMax()
        minimax.search_optimal_move(
            board_state, evaluator, player_color, opponent_color, depth)
    minimax_time = measure_performance(run_minimax)
    logger.info('MiniMax algorithm took(depth = ' +
          str(depth) + '): ' + str(minimax_time) + 's')

    logger.info('AlphaBeta is faster than Minimax algorithm for(depth = ' + str(depth) + '): ' +
          str((minimax_time/alpha_beta_time) * 100) + '%')
    return (alpha_beta_time, minimax_time)


def board_performance_test():
    logger = getLogger(__name__)
    bit_board = BitBoard()
    evaluator = Evaluator()
    player_color = 'black'
    opponent_color = 'white'
    depth = 4

    def run_bit_board_alpha_beta():
        alpha_beta = AlphaBeta()
        alpha_beta.search_optimal_move(
            bit_board, evaluator, player_color, opponent_color, depth)
    bit_board_time = measure_performance(run_bit_board_alpha_beta)
    logger.info('AlphaBeta with bitboard took(depth = ' +
          str(depth) + '): ' + str(bit_board_time) + 's')

    matrix_board = MatrixBoard()
    def run_matrix_board_alpha_beta():
        alpha_beta = AlphaBeta()
        alpha_beta.search_optimal_move(
            matrix_board, evaluator, player_color, opponent_color, depth)
    matrix_board_time = measure_performance(run_matrix_board_alpha_beta)
    logger.info('AlphaBeta with matrixboard took(depth = ' +
          str(depth) + '): ' + str(matrix_board_time) + 's')

    return (bit_board_time, matrix_board_time)


def measure_performance(target_function):
    results = []
    for _ in range(10):
        before = time.time()
        target_function()
        after = time.time()
        results.append(after - before)
    return np.average(results)


if __name__ == '__main__':
    basicConfig(level=INFO)
    board_state = BitBoard()
    evaluator = Evaluator()
    player_color = 'black'
    opponent_color = 'white'

    algorithm_sanity_check(board_state, evaluator,
                           player_color, opponent_color, depth=4)
    
    board_performance_result = board_performance_test()

    algorithm_performance_results = []
    for depth in range(1, 6):
        result = algorithm_performance_test(board_state, evaluator,
                                            player_color, opponent_color, depth=depth)
        algorithm_performance_results.append(result)
    
