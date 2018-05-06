from logging import getLogger, INFO, basicConfig
from othello.engine import Engine
from othello.ai.alpha_beta import AlphaBeta
from othello.ai.evaluator import Evaluator
from ai_player import AiPlayer


def play_one_episode():
    logger = getLogger(__name__)
    rows = 8
    columns = 8
    black_player = AiPlayer(AlphaBeta(depth=4), Evaluator())
    white_player = AiPlayer(AlphaBeta(depth=4), Evaluator())
    othello_engine = Engine(black_player,
                            white_player,
                            rows,
                            columns)
    othello_engine.reset()
    transitions, winner = othello_engine.run_one_game()
    logger.info("Game finished! winner was: %s", winner)
    for board in transitions:
        logger.info("Game transitions:\n%s", board)


def main():
    play_one_episode()


if __name__ == '__main__':
    basicConfig(level=INFO)
    main()
