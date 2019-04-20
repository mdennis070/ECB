import chess
import chess.uci
import AI
import Game
import move_validation

testGame = Game.Game()

def call_AI_function():
    print("AI MOVE NOW")
    #Function call to AI and it outputs the move
    piece_move = testGame.AI_player.AI_move(testGame.board)
    print(piece_move)
    print(testGame.board)


#Board setup for Testing


#testGame.AI_player = AI.AI(3)  #For Test 1a, 1b, 2a
testGame.AI_player = AI.AI(1)  #For Test 2b, 3a, 3b
#NO AI FOR CASTLING TEST

for x in range(0,8):    #Only for Tests 1,2,3, Comment out when doing castle test
    call_AI_function()

# #Castling Test Board (Special Test. Needs to be commented out when not doing Castling Test)
# testGame.board.clear_board()
# testGame.board.set_piece_at(chess.A1, chess.Piece.from_symbol('R')) #White ROOK
# testGame.board.set_piece_at(chess.E1, chess.Piece.from_symbol('K'))
# testGame.board.set_piece_at(chess.H1, chess.Piece.from_symbol('R'))
# testGame.board.set_piece_at(chess.E8, chess.Piece.from_symbol('k'))
# print(testGame.board)
# #

print("DONE SETTING UP THE RANDOM BOARD", '\n')


#NEED TO THINK ABOUT HOW TO REMOVE HIGHLIGHTING after each turn have an array with any changes on the board based on a given round then clear the locations
testGame.white_pos = [[None for i in range(0,8)] for j in range(0,8)]
testGame.black_pos = [[None for i in range(0,8)] for j in range(0,8)]

testGame.live_move_highlight()
print(testGame.LED_data, '\n')
print(testGame.board)
testGame.castle_state_check()
