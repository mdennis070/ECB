import time
import chess
from game_ctrl import Game

chess_game = Game()

piece_types = [chess.KNIGHT, chess.BISHOP, chess.ROOK, chess.QUEEN, chess.KING]

for piece in piece_types:
    print(piece)
    chess_game.make_start_LED_array(piece)
    complete = False
    while not complete:
        complete = chess_game.check_start_up_state(piece)
        time.sleep(0.5)

