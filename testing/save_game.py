import chess
import chess.uci
import AI
import chess.pgn

#Array defined in _init_.py in the python chess documentation library
#https://github.com/niklasf/python-chess/blob/master/chess/__init__.py
''' Edited to make them an array of strings
SQUARES = [
    "A1", "B1", "C1", "D1", "E1", "F1", "G1", "H1",
    "A2", "B2", "C2", "D2", "E2", "F2", "G2", "H2",
    "A3", "B3", "C3", "D3", "E3", "F3", "G3", "H3",
    "A4", "B4", "C4", "D4", "E4", "F4", "G4", "H4",
    "A5", "B5", "C5", "D5", "E5", "F5", "G5", "H5",
    "A6", "B6", "C6", "D6", "E6", "F6", "G6", "H6",
    "A7", "B7", "C7", "D7", "E7", "F7", "G7", "H7",
    "A8", "B8", "C8", "D8", "E8", "F8", "G8"," H8",
]
'''

#Array defined in _init_.py in the python chess documentation library
#https://github.com/niklasf/python-chess/blob/master/chess/__init__.py
SQUARES = [
    A1, B1, C1, D1, E1, F1, G1, H1,
    A2, B2, C2, D2, E2, F2, G2, H2,
    A3, B3, C3, D3, E3, F3, G3, H3,
    A4, B4, C4, D4, E4, F4, G4, H4,
    A5, B5, C5, D5, E5, F5, G5, H5,
    A6, B6, C6, D6, E6, F6, G6, H6,
    A7, B7, C7, D7, E7, F7, G7, H7,
    A8, B8, C8, D8, E8, F8, G8, H8,
] = range(64)

#Array defined in _init_.py in the python chess documentation library
#https://github.com/niklasf/python-chess/blob/master/chess/__init__.py
FILE_NAMES = ["a", "b", "c", "d", "e", "f", "g", "h"]
RANK_NAMES = ["1", "2", "3", "4", "5", "6", "7", "8"]
SQUARE_NAMES = [f + r for r in RANK_NAMES for f in FILE_NAMES]



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


#GOOD REFERENCE FOR MAKING Board.py code
    #https://github.com/johncheetham/jcchess/blob/master/jcchess/board.py
    #https://github.com/johncheetham/jcchess/tree/master/jcchess

#https://github.com/niklasf/python-chess/issues/302
#https://github.com/niklasf/python-chess/issues/63
#https://python-chess.readthedocs.io/en/v0.25.1/pgn.html#chess.pgn.read_game

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

