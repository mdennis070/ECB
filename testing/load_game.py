import chess
import chess.uci
import AI
import chess.pgn


#Function Call to make it easy to call AI and print board out
def call_AI_function():
    #Function call to AI and it outputs the move
    piece_move = raydon_game.AI_move(board)
    #board.push(piece_move)
    print(piece_move, "\n")
    print(board, "\n")


#prompt for level of difficulty
level_difficulty = input("Choose a level: ")
print("AI level is " + level_difficulty, "\n")

#Make AI class
raydon_game = AI.AI(int(level_difficulty))

#Make board
board = chess.Board()
print("Initial Board")
print(board, "\n")


#Open a .pgn file to open a saved game
pgn = open("./test.pgn")

#access contents of the loaded game
loaded_game = chess.pgn.read_game(pgn)
print(loaded_game.headers["Event"])
print(loaded_game.headers["Date"])
print(loaded_game.headers["White"])
print(loaded_game.headers["Black"])
print(loaded_game.headers["Round"])
print(loaded_game.headers["Result"])

# Iterate through all moves and play them on a board.
#board = loaded_game.board()
for move in loaded_game.mainline_moves():
    board.push(move)

print("Loaded Board")
print(board, "\n")

'''
#Sample user test (White move)
Nf3 = chess.Move.from_uci("g1f3")
board.push(Nf3)
print("White Move 1")
print(board, "\n")


user_black_move = chess.Move.from_uci("d7d5")
board.push(user_black_move)
print("Black Move 1")
print(board, "\n")
'''

#call AI Function
print("AI move1")
call_AI_function()

#call AI Function
print("AI move2")
call_AI_function()



'''
print("***********************Automated Testing******************************")

rounds = 2
while rounds < 10:
    print("AI Automove", rounds)
    call_AI_function()
    #print(board, "\n")
    rounds = rounds + 1
'''