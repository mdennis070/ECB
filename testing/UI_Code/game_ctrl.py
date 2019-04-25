import chess
import chess.uci
import chess.pgn
from electronics_ctrl import Electronics_Control
from move_validation import move_validation as move_val

class Game:

    #Make board
    #board = chess.Board()
    #board = chess.Board("rnbqkbn1/4pppp/pppp4/7r/N7/5PPP/PPPPP3/R1BQKBNR w KQkq - 0 1")
    board = chess.Board("r7/8/k7/8/8/8/7N/7K w KQkq - 0 1")

    #Make Electronics Control Class
    Electronics_control = Electronics_Control()

    Move_validation = move_val()
    
    #Variables for initial placement and some for live_highlighting
    brightness = 3
    setup_array = [[None for i in range(0,6)] for j in range(0,2)]  #2D array holding the tuples of the locations for each type of piece (pawn, knight, bishop... as well as white and black)

    #Color Scheme (tuples)
    color_dict = {'red':(255,0,0), 'green':(0,255,0), 'blue':(0,0,255), 'majenta':(255,0,255), 'yellow':(255,255,0), 'cyan':(0, 255, 255), 'black':(0,0,0), 'white':(255,255,255)}

    #2D array of tuples indicating the color of each square. Initialize with all LEDs OFF
    LED_data = [[(0, 0, 0) for i in range(0, 8)] for j in range(0, 8)]
    
    ############
     #Variables for live_highlighting
    selected_piece = 0           #a square location (ex: 0 - 63)
    last_selected_piece = None   #Holds the last selected_piece if it exists. It will be reset to None at the end of a turn
    move_made = None           #temporarily holds moves made (in UCI format ex: g1f3)
    array_legal_moves = []    #will hold the squares for the legal moves
    king_in_check   = False     #will hold true/false value that says if king is in check
    king_pos = None    #will highlight king square in red
    illegal_array   = []      #will hold array of two positions to show move from and move to square and highlight them yellow
    illegal_move    = None     #will hold true/false value that says if an illegal move was made

    castling_state = False      #Tracks if castling happened
    castling_state_array = [False, False, False, False]   # loc 1 - w_kingside, loc 2 - w_queenside, loc 3 - b_kingside, loc 4 - b_queenside
    end_turn = False            #Only true if user hits clock or time runs out

    #highlight arrays
    legal_move_highlight = []   #holds locations to highlight for legal move highilighting
    last_move_highlight = []    #holds locations to highlight for last move highlighting
    #illegal_move_highlight = [] #holds locations to highlight for illegal move highlighting #REPLACED BY "illegal_array = []"
    king_check_highlight = []   #holds locations to highlight for king check highlighting
    castle_move_highlight = []  #holds locations to highlight for castle (if castling was done)
    #piece_danger_highlight = []

    #movement
    move_buffer = None


    def __init__(self, settings=None):
        if settings != None:
            if settings["num players"] == 1:
                # make AI
                settings["ai diff"]
            else:
                settings["p2 color"]
            #rotate board based on p1 color
            settings["p1 color"]
            settings["tutor on"]
            settings["game timer"]
            settings["move timer"]
        self.start_list_LED_array()

    #Initial Board setup functions
    def start_list_LED_array(self):
        #row = 0 - white, 1 - black
        #col = 0 - Pawn, 1 - Knight, 2 - Bishop, ... , 6 - King
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
        [self.white_pos, self.black_pos] = self.Electronics_control.refresh_board(self.LED_data, self.brightness, 90)

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
        # In event header save
        # - tutor T/F
        # - four other setting options T/F
        # - move timer 04
        # - time left white 00004
        # - time left black 00010
        game = chess.pgn.Game()
        game = chess.pgn.Game.from_board(self.board) #updates the board with the moves made
        game.headers["Event"] = "Chess Game"
        game.headers["Date"] = date
        game.headers["White"] = "P1w"
        game.headers["Black"] = "AIb3"
        game.headers["Round"] = self.board.turn
        game.headers["Result"] = self.board.result() #saves it to the pgn
        new_pgn = open("./saves/{}.pgn".format(filename), "w", encoding="utf-8") #Open/Save it to a file called test.pgn
        exporter = chess.pgn.FileExporter(new_pgn)
        game.accept(exporter)
        
    def load_game(self, filename):
        pgn = open("./saves/{}.pgn".format(filename))
        loaded_game = chess.pgn.read_game(pgn)
        P1 = loaded_game.headers["White"]
        P2 = loaded_game.headers["Black"]
        self.turn = loaded_game.headers["Round"]
        self.result = loaded_game.headers["Result"]
        
        for move in loaded_game.mainline_moves():
            self.board.push(move)
        print(self.board)
        self.start_list_LED_array()
            
    def clear_board_LED(self):
        self.LED_data = [[(0, 0, 0) for i in range(0, 8)] for j in range(0, 8)] #2D array of tuples indicating the color of each square. Initialize with all LEDs OFF
        #repopulate past move and check if applicable
        
    def checking_king_check(self):

        self.king_check_highlight = []
        [self.king_in_check, attackers_array] = self.Move_validation.is_check(self.board)
        
        if(self.king_in_check == True):
            #print("A KING IS IN CHECK")
            #highlight king in red
            self.king_pos = self.board.king(self.board.turn)
            row = self.king_pos // 8
            col = self.king_pos % 8
            self.king_check_highlight.append([row, col])

            #highlight attackers in red
            for x in range(0, len(attackers_array)):
                row = attackers_array[x] // 8
                col = attackers_array[x] % 8
                self.king_check_highlight.append([row, col])

    #adds highlighting squares to array if a piece is lifted
    def piece_lifted(self):
        #highlight square that's lifted (blue)
        row = self.selected_piece // 8
        col = self.selected_piece % 8
        self.legal_move_highlight.append( [row, col, self.color_dict["blue"]])  #Add the lifted piece's location to the lifted piece's LED highlighting

        #show legal moves (green)
        self.array_legal_moves = self.Move_validation.piece_legal_moves(self.board, self.selected_piece)
        #print("ARRAY_LEGAL_MOVES is ", self.array_legal_moves)
        #convert UCI to square number
        for x in range(0, len(self.array_legal_moves)):
            row = self.array_legal_moves[x].to_square // 8
            col = self.array_legal_moves[x].to_square % 8
            self.legal_move_highlight.append( [row, col, self.color_dict["green"] ])

    #checks where the piece is currently placed. Used to determine which LEDs to highlight. Only does something if an illegal move was made but was then corrected
    def placement_check(self):  #Only for illegal move highlighting
        print("\n", "Placement Check", "\n")
        if (self.illegal_move == True and len(self.illegal_array) !=0):    #remove illegal move highlighting if illegal moves were corrected. No illegal moves (were corrected) but highlighting is still on the board
            if (self.LED_data[ self.illegal_array[0][0] ][ self.illegal_array[0][1] ] == self.color_dict["yellow"]):  #Check for the first array index in the illegal_array to see if there are any illegal moves (if yellow then none of the highlights were removed)
                for y in range(0, len(self.illegal_array)): #could perform more than 1 illegal move in a row so remove all illegal moves
                    for x in range(0, 1):
                        self.LED_data[ self.illegal_array[y][x] ][ self.illegal_array[y][x+1] ] == self.color_dict["black"]
                self.illegal_array = []  #Remove all illegal moves from the array because they were corrected
        pass


    #pushes the move when the turn has ended
    #NEED TO CHANGE THIS CODE FOR THE NEW REVISION. IT WILL ALSO ASSIGN THE HIGHLIGHTING IN HERE.
    def end_turn_move(self):
        #Functions before this need to check if the last move the user made was a legal move before they end the turn
        #SHOULD I MAKE A CONDITION TO ALSO SEE IF illegal_move == false? (means and illegal move was last made)
        if self.move_buffer != None:
            self.board.push(self.move_buffer)
            #print("PUSHED THE MOVE@@@@@@@@@@@@@@@@@@@@@@@@@")
            #print(self.move_buffer)
            self.clear_board_LED()

            #Move was made. Highlight prev_player_move cyan or other color (from and to square)
            self.last_move_highlight = []    #Reset it before appending new last move
            row_1 = self.move_buffer.from_square // 8
            col_1 = self.move_buffer.from_square % 8
            self.last_move_highlight.append([row_1, col_1])
            row_2 = self.move_buffer.to_square // 8
            col_2 = self.move_buffer.to_square % 8
            self.last_move_highlight.append([row_2, col_2])

            #Reset variables for the next player
            self.move_made = None    #clear because it's a new player's turn
            self.selected_piece = None
            self.array_legal_moves = []  #new player turn so no move should be listed
            self.illegal_array = []  #should be cleared by the end of the turn
            self.illegal_move = False #should already be false. NOT SURE IF THIS IS NEEDED TO BE STATED HERE

            #self.castling_state = False      #Tracks if castling happened
            #self.castling_state_array = [False, False, False, False]   # loc 1 - w_kingside, loc 2 - w_queenside, loc 3 - b_kingside, loc 4 - b_queenside
            
            self.checking_king_check()

            print(self.board)
            print("")

            if self.board.turn:
                return "White"
            else:
                return "Black"

        return "illegal"

    def assign_highlight(self):
        self.clear_board_LED()
        
        #Last Move
        for x in range(0, len(self.last_move_highlight)):   #Only 2 squares are higlighted
            self.LED_data[self.last_move_highlight[x][0]][self.last_move_highlight[x][1]] = self.color_dict["blue"]
        #Already cleared in "end_turn()"

        #Illegal Move (Technically this is already processed)
        for x in range(0, len(self.illegal_array)):
            self.LED_data[self.illegal_array[x][0]][self.illegal_array[x][1]] = self.color_dict["yellow"]

        #King Check
        for x in range(0, len(self.king_check_highlight)):
            self.LED_data[self.king_check_highlight[x][0]][self.king_check_highlight[x][1]] = self.color_dict["red"]

        #Castle Check
        for x in range(0, len(self.castle_move_highlight)):
            self.LED_data[self.castle_move_highlight[x][0]][self.castle_move_highlight[x][1]]  = self.color_dict["cyan"]
        #Reset the array
        self.castle_move_highlight = []
        
        #Legal Moves (THIS WILL HAVE A PROBLEM BECAUSE LEGAL_MOVES WILL ALWAYS BE APPENDED EACH TIME )
        for x in range(0, len(self.legal_move_highlight)):
            row = self.legal_move_highlight[x][0]
            col = self.legal_move_highlight[x][1]
            self.LED_data[row][col] = self.legal_move_highlight[x][2]

        [self.white_pos, self.black_pos] = self.Electronics_control.refresh_board(self.LED_data, self.brightness, 90)


    def live_move_highlight(self):
        [self.selected_piece, self.move_made, castle] = self.Move_validation.determine_move_made(self.board, self.white_pos, self.black_pos)
        #print("Selected piece/square: ",self.selected_piece)
        #print("Move made: ", self.move_made)
        #print("")
        #self.placement_check() #check if the player corrected an illegal move if an illegal move was done.
        #if no move was made (just lifted a piece or nothing happens) then move_made = None. Will have to make a condition for that so that nothing on the board is highlighted unless if a piece is lifted
        #self.castle_state_check()  #checks if there's castling in progress
        self.legal_move_highlight = [] #reset the array to add new legal moves into legal_move_highlight array
        self.illegal_array = []
        if (self.selected_piece != None and self.castling_state == False):    #piece is lifted    (When swapping or killing a piece no square will be highlighted; the physical process of replacing and removing a piece on the board)

            self.piece_lifted() #logic to load legal_move highlight squares

        if(self.move_made != None and self.castling_state == False): #a move was made

            self.illegal_move = self.Move_validation.is_legal_move(self.board, self.move_made)  #check if move was illegal
            if(self.illegal_move == False):  #It is an illegal move
                self.move_buffer = None
                #Do not push the move (don't update the board with the illegal move)
                #highlight yellow (from and to squares)
                row_1 = self.move_made.from_square //8   #assuming that it is actually from UCI and not just a regular string to make it have the appearance of UCI. If just a regular string with the look of UCI, then perform the code found at (***!!!)
                col_1 = self.move_made.from_square % 8
                self.illegal_array.append([row_1, col_1]) #add the from and to squares to the illegal move array
                row_2 =  self.move_made.to_square //8
                col_2 =  self.move_made.to_square % 8
                self.illegal_array.append([row_2, col_2])

                #touchscreen will need to make an if condition that stops other moves/highlighting/reading if an illegal move was made
                #if (self.illegal_move != False): #no illegal move was made
                    #call game reading funtions

            else:    #legal move was made (King check condition done elsewhere)
                self.move_buffer = self.move_made   #save the move for the move buffer
                #self.castle_highlight_check()    #checks if a castle was done
                #Will need a checking_promotion()
                #touchscreen can call checking_king_check to see if the king is in check at the beginning of a new turn
        else:
            # if no move was made
            self.move_buffer = None
        
