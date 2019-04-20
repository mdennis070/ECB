import chess
import chess.uci

from ece44x_move_val import move_validation as Validation
from ece44x_EC import Electronics_Control as EC

validation = Validation()
board_EC = EC(4)

brightness = 4 # 1 to 10
color_off = (0, 0, 0)
color_on = (0, 255, 0)
board_colors = [[color_off for i in range(0, 8)] for j in range(0, 8)]

board_1 = chess.Board('r1bqkb1r/pppp2pp/2n2n2/3Qp3/2B1P3/8/PPPP1PPP/RNB1K1NR b KQkq - 0 4')

print(board_1)
print(board_1.turn)
move_list = validation.piece_legal_moves(board_1, chess.F8)
print(move_list)
for itr in range(len(move_list)):
    move_list[itr] = move_list[itr].to_square

for row in range(0, 8):
    for col in range(0, 8):
        tile = row*8 + col
        if tile in move_list:
            board_colors[row][col] = color_on
        else:
            board_colors[row][col] = color_off
        print(board_colors[row][col])

board_EC.refresh_board(board_colors, brightness)
