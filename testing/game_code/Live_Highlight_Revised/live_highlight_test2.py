# #prompt for level of difficulty
# level_difficulty = input("Choose a level: ")
# print("AI level is " + level_difficulty, "\n")

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

#prompt for Selecting Test Scenario for Case
temp_scenario = input("Choose a Scenario: ")
print("Scenario is " + temp_scenario, "\n")

scenario = int(temp_scenario)

#SCENARIO 0 (Clean board)
if(scenario == 0):
    #For Test 5a, 5b, 5c, 5d
    print("Setup Starting Board")
    print(testGame.board, "\n")
    pass

#SCENARIO 1
if (scenario == 1):
    testGame.AI_player = AI.AI(3)  #For Test 1a, 1b, 2a

#SCENARIO 2
elif (scenario == 2):
    testGame.AI_player = AI.AI(1)  #For Test 2b, 3a, 3b

print(scenario)

#NO AI FOR CASTLING TEST
if(scenario == 1 or scenario == 2):
    for x in range(0,8):    #Only for Tests 1,2,3, Comment out when doing castle test
        call_AI_function()
    print("DONE SETTING UP THE RANDOM BOARD", '\n')
    print(testGame.board, "\n")

#SCENARIO 3
if (scenario == 3):
# #Castling Test Board (Special Test. Needs to be commented out when not doing Castling Test)
    testGame.board.clear_board()
    testGame.board.set_piece_at(chess.A1, chess.Piece.from_symbol('R')) #White ROOK
    testGame.board.set_piece_at(chess.E1, chess.Piece.from_symbol('K'))
    testGame.board.set_piece_at(chess.H1, chess.Piece.from_symbol('R'))
    testGame.board.set_piece_at(chess.E8, chess.Piece.from_symbol('k'))
    print("DONE SETTING UP THE RANDOM BOARD", '\n')
    print(testGame.board, "\n")

# #


#NEED TO THINK ABOUT HOW TO REMOVE HIGHLIGHTING after each turn have an array with any changes on the board based on a given round then clear the locations
testGame.white_pos = [[None for i in range(0,8)] for j in range(0,8)]
testGame.black_pos = [[None for i in range(0,8)] for j in range(0,8)]

#1st rotation
print("Testing Live Highlighting")
testGame.live_move_highlight()
print(testGame.LED_data, '\n')
print(testGame.board, '\n')
#testGame.castle_state_check()

#testGame.placement_check()  #Checks for illegal moves
testGame.assign_highlight() #Makes the actual highlight array to send out
print(testGame.LED_data, '\n')
print(testGame.board, '\n')


#2nd rotation
testGame.live_move_highlight()
print(testGame.LED_data, '\n')
print(testGame.board, '\n')
#testGame.castle_state_check()

#testGame.placement_check()  #Checks for illegal moves
testGame.assign_highlight() #Makes the actual highlight array to send out
print(testGame.LED_data, '\n')
print(testGame.board, '\n')

#Need to test last move highlight
print("ENDING TURN")
testGame.end_turn_move()
print(testGame.LED_data, '\n')
print(testGame.board, '\n')

testGame.assign_highlight() #Makes the actual highlight array to send out
print(testGame.LED_data, '\n')
print(testGame.board, '\n')

#3rd rotation (Make a black move. So scenario 1 -> test case 1 -> test case 1001 -> test case 12)
