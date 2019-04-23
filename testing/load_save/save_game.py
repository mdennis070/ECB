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

    #Test input
    if piece_move.uci() == "c7c5":
        print("HELLO")
    else:
        print("NOOO")

    print(board)
    print(' ')


#prompt for level of difficulty
level_difficulty = input("Choose a level: ")
print("AI level is " + level_difficulty, "\n")

#Make AI class
raydon_game = AI.AI(int(level_difficulty))

#Make board
board = chess.Board()
print("Initial Board")
print(board, "\n")

#Make a class to export game later
game = chess.pgn.Game()

#Sample user test (White move)
Nf3 = chess.Move.from_uci("g1f3")
board.push(Nf3)
print("White Move 1")
print(board, "\n")


user_black_move = chess.Move.from_uci("d7d5")
board.push(user_black_move)
print("Black Move 1")
print(board, "\n")

#call AI Function
print("AI move1")
call_AI_function()

#call AI Function
print("AI move2")
call_AI_function()

game = chess.pgn.Game.from_board(board) #updates the board with the moves made
game.headers["Event"] = "Example PGN game RAY"
game.headers["Date"] = "2/4/2019"
game.headers["White"] = "Ray"
game.headers["Black"] = "AI"
game.headers["Round"] = board.turn
game.headers["Result"] = board.result() #saves it to the pgn
new_pgn = open("./test.pgn", "w", encoding="utf-8") #Open/Save it to a file called test.pgn
exporter = chess.pgn.FileExporter(new_pgn)
game.accept(exporter)

#print(game)

'''
print("***********************Automated Testing******************************")

rounds = 2
while rounds < 10:
    print("AI Automove", rounds)
    call_AI_function()
    #print(board, "\n")
    rounds = rounds + 1
'''

