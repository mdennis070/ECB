import chess
import chess.uci
import chess.pgn
from electronics_ctrl import Electronics_Control

class Game:

    #Make board
    board = chess.Board("rnbqkbn1/4pppp/pppp4/7r/N7/5PPP/PPPPP3/R1BQKBNR w KQkq - 0 1")

    #Make Electronics Control Class
    Electronics_control = Electronics_Control()
    
    P1 = "P1"
    P2 = "AI"

    #Variables for initial placement and some for live_highlighting
    brightness = 3
    setup_array = [[None for i in range(0,6)] for j in range(0,2)]  #2D array holding the tuples of the locations for each type of piece (pawn, knight, bishop... as well as white and black)

    #Color Scheme (tuples)
    color_dict = {'red':(255,0,0), 'green':(0,255,0), 'blue':(0,0,255), 'majenta':(255,0,255), 'yellow':(255,255,0), 'cyan':(0, 255, 255), 'black':(0,0,0), 'white':(255,255,255)}

    #2D array of tuples indicating the color of each square. Initialize with all LEDs OFF
    LED_data = [[(0, 0, 0) for i in range(0, 8)] for j in range(0, 8)]


    def __init__(self, P1="P1", P2="AI", AI_level=3):
        self.start_list_LED_array()

    #Initial Board setup functions
    def start_list_LED_array(self):
        #row = 0 - white, 1 - black
        #col = 0 - Pawn, 1 - Knight, 2 - Bishop, ... , 6 - King
        #print(board)
        self.setup_array[0][0] =  list(self.board.pieces(chess.PAWN, chess.WHITE))
        self.setup_array[0][1] =  list(self.board.pieces(chess.KNIGHT, chess.WHITE))
        self.setup_array[0][2] =  list(self.board.pieces(chess.BISHOP, chess.WHITE))
        self.setup_array[0][3] =  list(self.board.pieces(chess.ROOK, chess.WHITE))
        self.setup_array[0][4] =  list(self.board.pieces(chess.QUEEN, chess.WHITE))
        self.setup_array[0][5] =  list(self.board.pieces(chess.KING, chess.WHITE))
        self.setup_array[1][0] =  list(self.board.pieces(chess.PAWN, chess.BLACK))
        self.setup_array[1][1] =  list(self.board.pieces(chess.KNIGHT, chess.BLACK))
        self.setup_array[1][2] =  list(self.board.pieces(chess.BISHOP, chess.BLACK))
        self.setup_array[1][3] =  list(self.board.pieces(chess.ROOK, chess.BLACK))
        self.setup_array[1][4] =  list(self.board.pieces(chess.QUEEN, chess.BLACK))
        self.setup_array[1][5] =  list(self.board.pieces(chess.KING, chess.BLACK))

    #Place the pieces according to the chess piece layout in board()
    def make_start_LED_array(self, which_piece):

        for x_1 in range(0,len(self.setup_array[0][which_piece-1])):
            #setup white pieces
            tile_val = self.setup_array[0][which_piece-1][x_1]
            row = tile_val // 8
            col = tile_val % 8
            self.LED_data[row][col] = self.color_dict["majenta"]   #white pieces

        for x_2 in range(0,len(self.setup_array[1][which_piece-1])):
            #setup black pieces
            tile_val = self.setup_array[1][which_piece-1][x_2]
            row = tile_val // 8
            col = tile_val % 8
            self.LED_data[row][col] = self.color_dict["cyan"]   #black pieces

    #Check if all of the pieces of that specific type is placed on the board. If so, it will move onto the next type of piece after this function
    def check_start_up_state(self, which_piece):
        [self.white_pos, self.black_pos] = self.Electronics_control.refresh_board(self.LED_data, self.brightness)

        #print(len(self.setup_array[0][which_piece-1]))
        for x_1 in range(0, len(self.setup_array[0][which_piece-1])):
            #check for white pieces
            tile_val = self.setup_array[0][which_piece-1][x_1]
            row_w = tile_val // 8
            col_w = tile_val % 8
            if self.white_pos[row_w][col_w] == False:
                #print("No piece at", row_w, " ", col_w)
                return False #just exit the function because at least one of the pieces are not in the list
        for x_2 in range(0, len(self.setup_array[1][which_piece-1])):
            #check for black pieces
            tile_val = self.setup_array[1][which_piece-1][x_2] 
            row_b = tile_val // 8
            col_b = tile_val % 8
            if self.black_pos[row_b][col_b] == False:
                #print("No piece at", row_b, " ", col_b)
                return False #just exit the function because at least one of the pieces are not in the list

            #only execute the following line if all of the pieces are in the correct location
        #which_piece = which_piece + 1   #move onto next piece
        #print("ALL PIECE ARE IN THE CORRECT LOCATION. LOOK AT NEXT PIECE")
        self.LED_data = [[(0,0,0) for i in range(0, 8)] for j in range(0, 8)]
        return True

    def save_game(self, filename, date):
        game = chess.pgn.Game()
        game = chess.pgn.Game.from_board(self.board) #updates the board with the moves made
        game.headers["Event"] = "Chess Game"
        game.headers["Date"] = date
        game.headers["White"] = self.P1
        game.headers["Black"] = self.P2
        game.headers["Round"] = self.board.turn
        game.headers["Result"] = self.board.result() #saves it to the pgn
        new_pgn = open("./saves/{}.pgn".format(filename), "w", encoding="utf-8") #Open/Save it to a file called test.pgn
        exporter = chess.pgn.FileExporter(new_pgn)
        game.accept(exporter)
        
    def load_game(self, filename):
        pgn = open("./saves/{}.pgn".format(filename))
        loaded_game = chess.pgn.read_game(pgn)
        self.P1 = loaded_game.headers["White"]
        self.P2 = loaded_game.headers["Black"]
        self.turn = loaded_game.headers["Round"]
        self.result = loaded_game.headers["Result"]
        
        for move in loaded_game.mainline_moves():
            self.board.push(move)
        print(self.board)
        
