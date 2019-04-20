import chess
import chess.uci
import AI
import Game


testGame = Game.Game()



testGame = Game.Game()



#condition for a randomly setup board
#testGame.board.set_fen('r1bqkb1r/pppp1Qpp/2n2n2/4p3/2B1P3/8/PPPP1PPP/RNB1K1NR b KQkq - 0 4')
#print("Different Board")
print(testGame.board, "\n")



which_piece = 1 #Start with the pawn

#Test if all pieces are placed in the correct location
#Fail Test condition
    #Implemented in the dummy refresh_board function in the testGame
testGame.start_list_LED_array()
testGame.make_start_LED_array(which_piece)
print("Print LED Color")
print(testGame.LED_data)
while testGame.continue_placing == True and which_piece < 7:
    testGame.continue_placing = False
    testGame.continue_placing = testGame.check_start_up_state(which_piece)
#    print("NEXT CHECKZZZZZ")
    which_piece = which_piece + 1
