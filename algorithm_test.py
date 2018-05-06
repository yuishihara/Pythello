import csv
import time
import numpy as np
from logging import getLogger, INFO, basicConfig
from othello.ai.alpha_beta import AlphaBeta
from othello.ai.minimax import MiniMax
from othello.ai.evaluator import Evaluator
from othello.bit_board import BitBoard
from othello.libfastbb import FastBitBoard
from othello.matrix_board import MatrixBoard


def algorithm_sanity_check(evaluator, player_color, opponent_color, depth):
    board_state = BitBoard()
    # Check that algorithms return same result
    alpha_beta = AlphaBeta(depth=depth)
    alpha_beta_best_move = alpha_beta.search_optimal_move(
        board_state, evaluator, player_color, opponent_color)
    alpha_beta_with_fastbb = AlphaBeta(depth=depth)
    alpha_beta_fastbb_best_move = alpha_beta_with_fastbb.search_optimal_move(
        FastBitBoard(), evaluator, player_color, opponent_color)
    assert alpha_beta_best_move == alpha_beta_fastbb_best_move

    minimax = MiniMax(depth=depth)
    minimax_best_move = minimax.search_optimal_move(
        board_state, evaluator, player_color, opponent_color)

    assert alpha_beta_best_move == minimax_best_move


def algorithm_performance_test(board_state, evaluator, player_color, opponent_color, depth):
    logger = getLogger(__name__)

    def run_alpha_beta():
        alpha_beta = AlphaBeta(depth=depth)
        alpha_beta.search_optimal_move(
            board_state, evaluator, player_color, opponent_color)
    alpha_beta_time = measure_performance(run_alpha_beta)
    logger.info('AlphaBeta algorithm took(depth = ' +
                str(depth) + '): ' + str(alpha_beta_time) + 's')

    def run_minimax():
        minimax = MiniMax(depth=depth)
        minimax.search_optimal_move(
            board_state, evaluator, player_color, opponent_color)
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
    depth = 5

    def run_bit_board_alpha_beta():
        alpha_beta = AlphaBeta(depth=depth)
        alpha_beta.search_optimal_move(
            bit_board, evaluator, player_color, opponent_color)
    bit_board_time = measure_performance(run_bit_board_alpha_beta)
    logger.info('AlphaBeta with bitboard took(depth = ' +
                str(depth) + '): ' + str(bit_board_time) + 's')

    fast_bit_board = FastBitBoard()

    def run_fast_bit_board_alpha_beta():
        alpha_beta = AlphaBeta(depth=depth)
        alpha_beta.search_optimal_move(
            fast_bit_board, evaluator, player_color, opponent_color)
    fast_bit_board_time = measure_performance(run_fast_bit_board_alpha_beta)
    logger.info('AlphaBeta with fastbitboard took(depth = ' +
                str(depth) + '): ' + str(fast_bit_board_time) + 's')

    matrix_board = MatrixBoard()

    def run_matrix_board_alpha_beta():
        alpha_beta = AlphaBeta(depth=depth)
        alpha_beta.search_optimal_move(
            matrix_board, evaluator, player_color, opponent_color)
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


def output_results_to_file(file_name, results):
    with open(file_name, 'w') as file:
        csv_writer = csv.writer(file)
        for result in results:
            csv_writer.writerow(result)


if __name__ == '__main__':
    basicConfig(level=INFO)
    logger = getLogger(__name__)
    board_state = BitBoard()
    evaluator = Evaluator()
    player_color = 'black'
    opponent_color = 'white'

    logger.info("Running alogorithm sanity check")
    algorithm_sanity_check(evaluator, player_color, opponent_color, depth=4)
    logger.info("Sanity check done")

    logger.info("Running board performance check")
    board_performance_result = board_performance_test()
    output_results_to_file('board_performance_result.csv', [
                           board_performance_result])
    logger.info("Board performance check done")

    logger.info("Running algorithm performance check")
    algorithm_performance_results = []
    for depth in range(1, 7):
        result = algorithm_performance_test(board_state, evaluator,
                                            player_color, opponent_color, depth=depth)
        algorithm_performance_results.append(result)
    output_results_to_file(
        'algorithm_performance_results.csv', algorithm_performance_results)
    logger.info("Algorithm performance check done")
