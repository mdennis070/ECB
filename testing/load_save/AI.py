import chess
import chess.uci

#remember to include "self." before the class variable

class AI:

    #AI Level of difficulty
    level = 1

    # Maps the level to the appropriate depth
    level_to_depth = [1,2,3,4,6,8,10,12]

    #initialize the engine
    #engine = chess.uci.popen_engine(".\stockfish-10-win\Windows\stockfish_10_x64")
    engine = chess.uci.popen_engine("stockfish") 

    def _init_(self):
        pass

    def __init__(self, level_difficulty): #Instantiate the class Just have a basic definition of the class. However, this is not needed
        #initialize the engine
        self.engine.uci()
        self.engine.ucinewgame()
        self.level = self.level_to_depth[level_difficulty-1]
        #make a board variable so that I can copy it

    #function that calls the AI move
    def AI_move(self, board):  #Could define the function outside of the spcae in the class
        #engine.ucinewgame() #Update the engine that we are in a new game. Do I pass in the "engine" object to this function?
        self.engine.position(board) #update the AI of the move history. Keeps the engine up to date with the current board. Must pass the board to this function
        print("The AI move is ")
        move = self.engine.go(movetime=2000, depth = self.level).bestmove
        #print(move, "\n") #will this just print the best move or will it also make the move? I'm trying to simply tell you the best move without printing it.
        board.push(move) #Make the best move. Synchronous
        return move
