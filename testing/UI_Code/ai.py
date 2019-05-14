import chess
import chess.uci

class AI:

    color = False;

    #AI Level of difficulty
    level = 1

    # Maps the level to the appropriate depth
    level_to_depth = [1,2,3,4,6,8,10,12]

    #initialize the engine
    engine = chess.uci.popen_engine("stockfish") 

    def __init__(self, level_difficulty = 3): #Instantiate the class Just have a basic definition of the class. However, this is not needed
        #initialize the engine
        self.engine.uci()
        self.engine.ucinewgame()
        self.level = self.level_to_depth[level_difficulty-1]
        #make a board variable so that I can copy it

    #function that calls the AI move
    def AI_move(self, board):  #Could define the function outside of the spcae in the class
        self.engine.position(board) #update the AI of the move history. Keeps the engine up to date with the current board. Must pass the board to this function
        print("The AI move is ")
        move = self.engine.go(movetime=1000, depth = self.level).bestmove
        #board.push(move) #Make the best move. Synchronous
        return move

    def hint(self, board):  #Could define the function outside of the spcae in the class
        self.engine.position(board) #update the AI of the move history. Keeps the engine up to date with the current board. Must pass the board to this function
        move = self.engine.go(movetime=1000, depth = self.level).bestmove
        return move

    def set_level(self, level_diff):
        self.level = level_diff

    def set_color(self, color):
        self.color = color
