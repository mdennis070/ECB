import time

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

board_1 = chess.Board('8/8/8/2q5/8/8/8/8 b KQkq - 0 4')
#board_1 = chess.Board('8/8/8/3q3Q/8/8/8/8 b KQkq - 0 4')
#board_1 = chess.Board('4k2r/8/8/8/8/8/8/8 b KQkq - 0 4')

print(board_1)
print(board_1.turn)

while True:
    [pos_w, pos_b] = board_EC.refresh_board(board_colors, brightness)
    [hint, move, castle] = validation.determine_move_made(board_1, pos_w, pos_b)
    print([hint, move, castle])

    if hint != None:
        move_list = validation.piece_legal_moves2(board_1, hint)
        for row in range(0, 8):
            for col in range(0, 8):
                tile = row*8 + col
                if tile in move_list:
                    board_colors[row][col] = color_on
                else:
                    board_colors[row][col] = color_off
                #print(board_colors[row][col])
    else:
        board_colors = [[color_off for i in range(0, 8)] for j in range(0, 8)]
    
    if move != None:
        print("move is legal: ", validation.is_legal_move(board_1, move))
    time.sleep(1)


"""
move_list = validation.piece_legal_moves(board_1, chess.D5)
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

for row in range(1, 8, 2):
    board_colors[row] = board_colors[row][::-1]
"""


