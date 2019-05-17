import chess
import chess.uci
import chess.pgn
from electronics_ctrl import Electronics_Control
from move_validation import move_validation as move_val
from ai import AI

class Game:

    
    #Make board
    board = chess.Board() # standard board

    #board = chess.Board("rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1")
    #board =  chess.Board("r3k2r/8/8/8/8/8/8/R3K2R w KQkq - 0 1") # castling testing case
    #board = chess.Board("3r4/K7/3r4/k7/8/8/8/8 b KQkq - 0 1") # check mate case

    #Make Electronics Control Class
    Electronics_control = Electronics_Control()

    Move_validation = move_val()

    cpu_AI = AI()
    hint_AI = AI(4)
    ai_on = False
    ai_move = None
    ai_turn = False
    
    white_pos = [[False for i in range(0, 8)] for j in range(0, 8)]
    black_pos = [[False for i in range(0, 8)] for j in range(0, 8)]

    #Variables for initial placement and some for live_highlighting
    brightness = 3
    setup_array = [[None for i in range(0,6)] for j in range(0,2)]  #2D array holding the tuples of the locations for each type of piece (pawn, knight, bishop... as well as white and black)

    #Color Scheme (tuples)
    color_dict = {'red':(255,0,0), 'green':(0,255,0), 'blue':(0,0,255), 'magenta':(255,0,255), 'yellow':(255,255,0), 'cyan':(0, 255, 255), 'black':(0,0,0), 'white':(255,255,255)}

    #2D array of tuples indicating the color of each square. Initialize with all LEDs OFF
    LED_data = [[(0, 0, 0) for i in range(0, 8)] for j in range(0, 8)]
    
    ############
     #Variables for live_highlighting
    selected_piece = 0           #a square location (ex: 0 - 63)
    move_made = None        #temporarily holds moves made (in UCI format ex: g1f3)
    castle_list = None      #holds the king's castle move (i.e. 'E1G1' format)
    array_legal_moves = []  #will hold the squares for the legal moves
    king_in_check   = False #will hold true/false value that says if king is in check
    king_pos = None         #will highlight king square in red
    illegal_move    = None     #will hold true/false value that says if an illegal move was made

    #castling_state = False      #Tracks if castling happened
    #castling_state_array = [False, False, False, False]   # loc 1 - w_kingside, loc 2 - w_queenside, loc 3 - b_kingside, loc 4 - b_queenside
    end_turn = False            #Only true if user hits clock or time runs out

    #highlight arrays
    highlight_legal = True
    highlight_illegal = True
    highlight_king = True
    highlight_last = True
    highlight_hint = True
    highlight_wrong_move = False

    legal_move_highlight = []   #holds locations to highlight for legal move highilighting
    last_move_highlight = []    #holds locations to highlight for last move highlighting
    illegal_array = []          #will hold array of two positions to show move from and move to square and highlight them yellow
    wrong_move_array = []
    king_check_highlight = []   #holds locations to highlight for king check highlighting
    castle_move_highlight = []  #holds locations to highlight for castle (if castling was done)
    hint_highlight = []
    ai_move_highlight = []
    #piece_danger_highlight = []
    
    chess_w = None
    chess_b = None

    rotate_board = 90

    #movement
    move_buffer = None
    warning_message = "Illegal Move"

    def __init__(self, settings=None):
        print("New 'Game' class object created")
        self.board = chess.Board() # this line clears board correctly
                                   # now can open new game without old board existing
        print(self.board)

        if settings != None:
            if settings["p1 color"]: # P1 is white
                self.chess_w = "P1"
                self.chess_b = "P2"
            else:
                self.chess_w = "P2"
                self.chess_b = "P1"

            if settings["num players"] == 1:
                # make AI
                level = settings["ai diff"]
                self.cpu_AI.set_level(level)
                if settings["p2 color"]: # P2 is white
                    self.chess_w = "AI{}".format(level)
                    self.cpu_AI.set_color(True)
                    self.ai_make_move()
                else:
                    self.cpu_AI.set_color(False)
                    self.chess_b = "AI{}".format(level)

            #rotate board based on p1 color
            if settings["p1 color"]:
                self.rotate_board = 90
            else:
                self.rotate_board = 270


            hint_on = settings["tutor on"]
            #settings["game timer"]
            #settings["move timer"]
            self.start_list_LED_array()


    def __del__(self):
        print("deleted")

    def update_settings(self, h_hint, h_legal, h_illegal, h_king, h_last):
        self.highlight_hint = h_hint
        self.highlight_legal = h_legal
        self.highlight_illegal = h_illegal
        self.highlight_king = h_king
        self.highlight_last = h_last

    #Initial Board setup functions
    def start_list_LED_array(self):
        #row = 0 - white, 1 - black
        #col = 0 - Pawn, 1 - Knight, 2 - Bishop, ... , 6 - King
        self.setup_array = [[None for i in range(0,6)] for j in range(0,2)]  
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
        
        self.clear_board_LED()

        for x_1 in range(0,len(self.setup_array[0][which_piece-1])):
            #setup white pieces
            tile_val = self.setup_array[0][which_piece-1][x_1]
            row = tile_val // 8
            col = tile_val % 8
            if self.white_pos[row][col] == False:
                self.LED_data[row][col] = self.color_dict["magenta"]   #white pieces


        for x_2 in range(0,len(self.setup_array[1][which_piece-1])):
            #setup black pieces
            tile_val = self.setup_array[1][which_piece-1][x_2]
            row = tile_val // 8
            col = tile_val % 8
            if self.black_pos[row][col] == False:
                self.LED_data[row][col] = self.color_dict["cyan"]   #black pieces

    #Check if all of the pieces of that specific type is placed on the board. If so, it will move onto the next type of piece after this function
    def check_start_up_state(self, which_piece):
        [self.white_pos, self.black_pos] = self.Electronics_control.refresh_board(self.LED_data, self.brightness, self.rotate_board)

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
        
        settings_str = ""
        settings_str = settings_str + str(self.highlight_hint)[0]
        settings_str = settings_str + str(self.highlight_legal)[0]
        settings_str = settings_str + str(self.highlight_illegal)[0]
        settings_str = settings_str + str(self.highlight_king)[0]
        settings_str = settings_str + str(self.highlight_last)[0]
        
        game.headers["Event"] = settings_str
        game.headers["Date"] = date
        game.headers["White"] = self.chess_w
        game.headers["Black"] = self.chess_b
        game.headers["Round"] = self.board.turn
        game.headers["Result"] = self.board.result() #saves it to the pgn
        new_pgn = open("./saves/{}.pgn".format(filename), "w", encoding="utf-8") #Open/Save it to a file called test.pgn
        exporter = chess.pgn.FileExporter(new_pgn)
        game.accept(exporter)
        
    def load_game(self, filename):
        self.board = chess.Board()
        pgn = open("./saves/{}.pgn".format(filename))
        loaded_game = chess.pgn.read_game(pgn)
        self.chess_w = loaded_game.headers["White"]
        self.chess_b = loaded_game.headers["Black"]
        self.result = loaded_game.headers["Result"]

        settings_str = loaded_game.headers["Event"]
        self.highlight_hint = settings_str[0] == 'T'
        self.highlight_legal = settings_str[1] == 'T' and self.highlight_hint
        self.highlight_illegal = settings_str[2] == 'T' and self.highlight_hint
        self.highlight_king = settings_str[3] == 'T' and self.highlight_hint
        self.highlight_last = settings_str[4] == 'T' and self.highlight_hint
        
        for move in loaded_game.mainline_moves():
            self.board.push(move)

        self.start_list_LED_array()

        if self.chess_w[0:2] == "AI":
            self.cpu_AI.set_level(int(self.chess_w[-1]))
            self.cpu_AI.set_color(True)
            if self.board.turn == chess.WHITE:
                self.ai_make_move()
        elif self.chess_b[0:2] == "AI":
            self.cpu_AI.set_level(int(self.chess_b[-1]))
            self.cpu_AI.set_color(False)
            if self.board.turn == chess.BLACK:
                self.ai_make_move()
        
        if self.chess_w == "P1":
            self.rotate_board = 90
        else:
            self.rotate_board = 270
 
    def hint(self):
        self.hint_highlight = []

        move = self.hint_AI.hint(self.board)

        row = move.to_square // 8
        col = move.to_square % 8
        self.hint_highlight.append([row, col])

        row = move.from_square // 8
        col = move.from_square % 8
        self.hint_highlight.append([row, col])

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
        self.legal_move_highlight.append( [row, col, self.color_dict["white"]])  #Add the lifted piece's location to the lifted piece's LED highlighting

        #show legal moves (green)
        self.array_legal_moves = self.Move_validation.piece_legal_moves(self.board, self.selected_piece)
        #print("ARRAY_LEGAL_MOVES is ", self.array_legal_moves)
        #convert UCI to square number
        for x in range(0, len(self.array_legal_moves)):
            row = self.array_legal_moves[x].to_square // 8
            col = self.array_legal_moves[x].to_square % 8
            self.legal_move_highlight.append( [row, col, self.color_dict["green"] ])


    #pushes the move when the turn has ended
    #NEED TO CHANGE THIS CODE FOR THE NEW REVISION. IT WILL ALSO ASSIGN THE HIGHLIGHTING IN HERE.
    def end_turn_move(self):

        self.ai_on = self.chess_w[0:2] == "AI" or self.chess_b[0:2] == "AI"
        self.ai_turn = (self.chess_w[0:2] == "AI" and self.board.turn) or (self.chess_b[0:2] == "AI" and not self.board.turn)
        

        end_turn_ai = self.ai_on and self.ai_turn and self.move_buffer == self.ai_move
        end_turn_ai = (self.ai_on and not self.ai_turn and self.move_buffer != None) or end_turn_ai
        end_turn_2p = not self.ai_on and self.move_buffer != None
        if end_turn_2p or end_turn_ai:
            self.board.push(self.move_buffer)
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

            self.hint_highlight = []

            if self.ai_on and not self.ai_turn:
                self.ai_make_move() 

            print(self.board)
            print("")

            if self.board.turn:
                return ["White", None]
            else:
                return ["Black", None]

        return ["illegal", self.warning_message]

    def ai_make_move(self):
        self.ai_move_highlight = []
        self.ai_move = self.cpu_AI.AI_move(self.board)

        row = self.ai_move.to_square // 8
        col = self.ai_move.to_square % 8
        self.ai_move_highlight.append([row, col])

        row = self.ai_move.from_square // 8
        col = self.ai_move.from_square % 8
        self.ai_move_highlight.append([row, col])

        print("ai move: {}".format(self.ai_move))

    def assign_highlight(self):
        self.clear_board_LED()
        
        self.ai_turn = (self.chess_w[0:2] == "AI" and self.board.turn) or (self.chess_b[0:2] == "AI" and not self.board.turn)

        #Last Move
        if self.highlight_last:
            for x in range(0, len(self.last_move_highlight)):   #Only 2 squares are higlighted
                self.LED_data[self.last_move_highlight[x][0]][self.last_move_highlight[x][1]] = self.color_dict["blue"]

        #King Check
        if self.highlight_king:
            for x in range(0, len(self.king_check_highlight)):
                self.LED_data[self.king_check_highlight[x][0]][self.king_check_highlight[x][1]] = self.color_dict["red"]

        #Castle Check
        # Highlight the rook that needs to move
        for x in range(0, len(self.castle_move_highlight)):
            self.LED_data[self.castle_move_highlight[x][0]][self.castle_move_highlight[x][1]]  = self.color_dict["magenta"]
        
        #Legal Moves 
        if self.highlight_legal and not self.ai_turn:
            for x in range(0, len(self.legal_move_highlight)):
                row = self.legal_move_highlight[x][0]
                col = self.legal_move_highlight[x][1]
                self.LED_data[row][col] = self.legal_move_highlight[x][2]
        
        #Hint
        if self.highlight_hint and not self.ai_turn:
            for x in range(0, len(self.hint_highlight)):
                row = self.hint_highlight[x][0]
                col = self.hint_highlight[x][1]
                self.LED_data[row][col] = self.color_dict["magenta"]
        
        #AI Move
        if self.ai_turn:
            for x in range(0, len(self.ai_move_highlight)):
                row = self.ai_move_highlight[x][0]
                col = self.ai_move_highlight[x][1]
                self.LED_data[row][col] = self.color_dict["magenta"]

        #Illegal Move (Technically this is already processed)
        if self.highlight_illegal: 
            for x in range(0, len(self.illegal_array)):
                self.LED_data[self.illegal_array[x][0]][self.illegal_array[x][1]] = self.color_dict["yellow"]

        #Wrong move made
        if self.highlight_wrong_move:
            for x in range(0, len(self.wrong_move_array)):
                tile_val = self.wrong_move_array[x]
                row = tile_val // 8
                col = tile_val % 8

                my_color = self.color_dict["yellow"]
                if self.board.turn and not self.black_pos[row][col]: # whites turn
                    self.LED_data[row][col] = my_color
                elif not self.board.turn and not self.white_pos[row][col]: # blacks turn
                    self.LED_data[row][col] = my_color

        [self.white_pos, self.black_pos] = self.Electronics_control.refresh_board(self.LED_data, self.brightness, self.rotate_board)

    def wrong_color_moved(self):
        not_turn = not self.board.turn

        self.wrong_move_array = []
        self.wrong_move_array.extend(list(self.board.pieces(chess.PAWN, not_turn)))
        self.wrong_move_array.extend(list(self.board.pieces(chess.KNIGHT, not_turn)))
        self.wrong_move_array.extend(list(self.board.pieces(chess.BISHOP, not_turn)))
        self.wrong_move_array.extend(list(self.board.pieces(chess.ROOK, not_turn)))
        self.wrong_move_array.extend(list(self.board.pieces(chess.QUEEN, not_turn)))
        self.wrong_move_array.extend(list(self.board.pieces(chess.KING, not_turn)))

    def live_move_highlight(self):
        [self.selected_piece, self.move_made, self.castle_list] = self.Move_validation.determine_move_made(self.board, self.white_pos, self.black_pos)
        #print("Selected piece/square: ",self.selected_piece)
        #print("Move made: ", self.move_made)
        #print("castle_list: ", self.castle_list)

        #if no move was made (just lifted a piece or nothing happens) then move_made = None. Will have to make a condition for that so that nothing on the board is highlighted unless if a piece is lifted
        #self.castle_state_check()  #checks if there's castling in progress
        self.legal_move_highlight = [] #reset the array to add new legal moves into legal_move_highlight array
        self.illegal_array = []
        
        
        self.wrong_color_moved()

        self.remove_rook_highlight() # remove rook highlight from castling

        if (self.selected_piece != None and self.castle_list == None):    #piece is lifted    (When swapping or killing a piece no square will be highlighted; the physical process of replacing and removing a piece on the board)

            self.piece_lifted() #logic to load legal_move highlight squares

        if(self.move_made != None): #a move was made 
            #and self.castle_list == None): #a move was made
            
            self.illegal_move = self.Move_validation.is_legal_move(self.board, self.move_made)  #check if move was illegal
            if(self.illegal_move == False or (self.ai_on and self.ai_turn and self.move_made != self.ai_move)):  #It is an illegal move
                self.warning_message = "Illegal Move Made"
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
                # castling is in progress. king has moved but rook has not moved yet.
                # don't add the move to the buffer yet.
                if not (self.castle_highlight_check() ):
                    self.move_buffer = self.move_made   #save the move for the move buffer


        elif self.castle_list != None:
            # castling happened (both a king and rook have been moved)
            print("Castle has happened already: ", self.castle_list)
            # castle_list can be 'e1c1', 'e1g1', 'e8c8', 'e8g8'
            # push the castle_list to the move_buffer
            self.move_buffer = self.castle_list 
            self.castle_move_highlight = [] # castling is now DONE, remove rook highlight
            
        else:
            # if no move was made
            self.move_buffer = None
            self.warning_message = "No Move Made"
       
    def check_end_game(self):
        return self.board.is_game_over()

    # highlights the position that the rook should move to to complete the castle
    # returns true if castling in progress (king has moved but not rook)
    # returns false if castling not in progress
    def castle_highlight_check(self):
        self.board.push(self.move_made) # have to push move to check the king location
                                        # kind of a hack

        if(self.board.turn == chess.BLACK):
            print("white's turn")
            if (self.move_made.uci() == "e1g1" and self.board.piece_at(chess.G1).symbol() == "K"):
                print("white kingside castle")
                self.castle_move_highlight.append([0, 7])
                self.castle_move_highlight.append([0, 5])
                self.board.pop()

                return True
            elif (self.move_made.uci() == "e1c1" and self.board.piece_at(chess.C1).symbol() == "K"):
                print("white queenside castle")
                self.castle_move_highlight.append([0, 0])
                self.castle_move_highlight.append([0, 3])
                self.board.pop()

                return True
            else:
                print("no white castle")
                self.board.pop()

                return False
            #
        #
        elif(self.board.turn == chess.WHITE):
            print("black's turn")
            if (self.move_made.uci() == "e8g8" and self.board.piece_at(chess.G8).symbol() == "k"):
                print("black kingside castle")
                self.castle_move_highlight.append([7, 7])
                self.castle_move_highlight.append([7, 5])
                self.board.pop()

                return True
            elif (self.move_made.uci() == "e8c8" and self.board.piece_at(chess.C8).symbol() == "k"):
                print("black queenside castle")
                self.castle_move_highlight.append([7, 0])
                self.castle_move_highlight.append([7, 3])
                self.board.pop()

                return True
            else:
                print("no black castle")   
                self.board.pop()

                return False
            #
        #

    def remove_rook_highlight(self):
        # this SHOULD only remove the rook highlighting if you undo the king's move
        # right now this removes highlight if you lift rook (not intentional) 
        # TODO: fix this
        if (self.move_made == None):
            self.castle_move_highlight = []

        # this section does not work because move_buffer is none if castling is not complete yet
        # if only moved the king, the move_buffer is empty
        '''
        if (self.move_buffer != None):
            self.board.push(self.move_made)

            no_longer_w_king_castle  = (self.move_buffer.uci() == "e1g1" and self.board.piece_at(chess.G1).symbol() != "K")
            no_longer_w_queen_castle = (self.move_buffer.uci() == "e1c1" and self.board.piece_at(chess.C1).symbol() != "K")
            no_longer_b_king_castle  = (self.move_buffer.uci() == "e8g8" and self.board.piece_at(chess.G8).symbol() != "k")
            no_longer_b_queen_castle = (self.move_buffer.uci() == "e8c8" and self.board.piece_at(chess.C8).symbol() != "k")
         
            if (no_longer_w_king_castle) or (no_longer_w_queen_castle):
                #remove rook highlight
                self.castle_move_highlight = []
            if (no_longer_b_king_castle) or (no_longer_b_queen_castle):
                #remove rook highlight
                self.castle_move_highlight = []
            self.board.pop()
        '''
    
    def reset_board(self):
        self.board = None
        self.board = chess.Board()

    def toggle_info(self):
        self.highlight_wrong_move = not self.highlight_wrong_move
