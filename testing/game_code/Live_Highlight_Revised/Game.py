import chess
import chess.uci
import AI
import move_validation
from electronics_control import Electronics_Control

class Game:

    #Make board
    board = chess.Board()

    #Make AI
    AI_player = AI.AI(1)

    #Make Hint AI
    AI_hint = AI.AI(8)

    #Make Move_Validation Class
    Move_validation = move_validation.move_validation()

    #Make Electronics Control Class
    Electronics_control = Electronics_Control()

    #Variables for initial placement and some for live_highlighting
    which_piece = 1 #Start with the pawn
    brightness = 1
    continue_placing = True
    setup_array = [[None for i in range(0,6)] for j in range(0,2)]  #2D array holding the tuples of the locations for each type of piece (pawn, knight, bishop... as well as white and black)

    #Variables for live_highlighting
    selected_piece = 0           #a square location (ex: 0 - 63)
    last_selected_piece = None   #Holds the last selected_piece if it exists. It will be reset to None at the end of a turn
    move_made = None           #temporarily holds moves made (in UCI format ex: g1f3)
    array_legal_moves = []    #will hold the squares for the legal moves
    king_in_check   = False     #will hold true/false value that says if king is in check
    king_pos = None    #will highlight king square in red
    attackers_array = None      #will hold an array of the attackers if check
    illegal_array   = []      #will hold array of two positions to show move from and move to square and highlight them yellow
    illegal_move    = None     #will hold true/false value that says if an illegal move was made

    highlight_turn = 0b0        #0 - means 1st player, 1 - means 2nd player
    current_turn   = 0          #keeps track of the current turn (maybe use python-chess function to obtain time instead)
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

    #Refresh_board Variable
    white_pos = [[None for i in range(0,8)] for j in range(0,8)]
    black_pos = [[None for i in range(0,8)] for j in range(0,8)]

    #Color Scheme (tuples)
    dict = {'red':(255,0,0), 'green':(0,255,0), 'blue':(0,0,255), 'majenta':(255,0,255), 'yellow':(255,255,0), 'cyan':(0, 255, 255), 'black':(0,0,0), 'white':(255,255,255)}

    #2D array of tuples indicating the color of each square. Initialize with all LEDs OFF
    LED_data = [[(0, 0, 0) for i in range(0, 8)] for j in range(0, 8)]


    def _init_(self):   #default constructor
        pass

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
            row = (self.setup_array[0][which_piece-1][x_1] //8)
            col = (self.setup_array[0][which_piece-1][x_1] % 8)
            self.LED_data[row][col] = self.dict["majenta"]   #white pieces

        for x_2 in range(0,len(self.setup_array[1][which_piece-1])):
            #setup black pieces
            row = (self.setup_array[1][which_piece-1][x_2] //8)
            col = (self.setup_array[1][which_piece-1][x_2] % 8)
            self.LED_data[row][col] = self.dict["cyan"]   #black pieces


    #Check if all of the pieces of that specific type is placed on the board. If so, it will move onto the next type of piece after this function
    def check_start_up_state(self, which_piece):
        [self.white_pos, self.black_pos] = self.Electronics_control.refresh_board(self.LED_data, self.brightness)
        print(len(self.setup_array[0][which_piece-1]))
        for x_1 in range(0, len(self.setup_array[0][which_piece-1])):
            #check for white pieces
            row_w = (self.setup_array[0][which_piece-1][x_1] //8)
            col_w = (self.setup_array[0][which_piece-1][x_1] % 8)
            if self.white_pos[row_w][col_w] == False:
                print("No piece at", row_w, " ", col_w)
                return False #just exit the function because at least one of the pieces are not in the list
        for x_2 in range(0, len(self.setup_array[1][which_piece-1])):
            #check for black pieces
            row_b = (self.setup_array[1][which_piece-1][x_2] //8)
            col_b = (self.setup_array[1][which_piece-1][x_2] % 8)
            if self.black_pos[row_b][col_b] == False:
                print("No piece at", row_b, " ", col_b)
                return False #just exit the function because at least one of the pieces are not in the list

            #only execute the following line if all of the pieces are in the correct location
        #which_piece = which_piece + 1   #move onto next piece
        print("ALL PIECE ARE IN THE CORRECT LOCATION. LOOK AT NEXT PIECE")
        return True


##################################################################################################################
#LIVE board Highlighting functions

    #Call this somewhere. Maybe after each turn?
    def clear_board_LED(self):
        self.LED_data = [[(0, 0, 0) for i in range(0, 8)] for j in range(0, 8)] #2D array of tuples indicating the color of each square. Initialize with all LEDs OFF
        #repopulate past move and check if applicable

    #checks if the castling is complete if the move was a castle
    def castle_state_check(self):
        #Check the state and see if the castling happened
        #print("Check if castling is in progress")
        if(self.castling_state == True): #Enter this statement only if castling is in progress and check if it was executed
            print("CASTLING IN PROGRESS")
            x = 0
            for x in range(0,4):
                if (self.castling_state_array[x] == True):   #check which castling type should be checked
                    break
            print(x) #check which castling type should be checked
            if(x == 0): #Check if white_kingside castling was done
                print("W Kingside")
                if(self.white_pos[0][5] == True):
                    print("MAHO")
                    self.castling_state_array[0] = False #castling is complete
                    self.castling_state = False
            elif(x == 1):#Check if white_queenside castling was done
                print("W Queenside")
                if(self.white_pos[0][3] == True):
                    print("MAHO")
                    self.castling_state_array[1] = False #castling is complete
                    self.castling_state = False
            elif(x == 2): #Check if black_kingside castling was done
                print("B Kingside")
                if(self.black_pos[7][5] == True):
                    print("MAHO")
                    self.castling_state_array[2] = False
                    self.castling_state = False
            else:   #Check if black_kingside castling was done
                print("B Queenside")
                if(self.black_pos[7][3] == True):
                    print("MAHO")
                    self.castling_state_array[3] = False
                    self.castling_state = False
        #end of castling_state if statement

        else: #No castling is in progress
            pass

    #checks if the move made was a castle
    def castle_highlight_check():
        self.board.push(self.move_buffer)   #make the move on the board
        #Castling highlight conditions
        if(self.board.turn == chess.BLACK):  #False means black turn. a push already happened so turn is swapped
            #Check white king moves (for Castling highlights)
            if(self.move_buffer.uci() == "e1g1" and self.board.piece_at(chess.G1).symbol() == "K"):
                self.castling_state = True   #MAKE CONDITION WHERE THE CASTLING IS FALSE. CHECK THE WHITE_POS ARRAY TO SEE IF H1 = FALSE AND F1 = TRUE
                #King side castling (highlight positions for rook)
                self.castling_state_array[0] = True
                #self.LED_data[0][7] = self.dict["cyan"]
                #self.LED_data[0][5] = self.dict["cyan"]
                self.castle_move_highlight.append([0,7])
                self.castle_move_highlight.append([0,5])

            elif(self.move_buffer.uci() == "e1c1" and self.board.piece_at(chess.C1).symbol() == "K" ):
                self.castling_state = True   #MAKE CONDITION WHERE THE CASTLING IS FALSE. CHECK THE WHITE_POS ARRAY TO SEE IF A1 = FALSE AND D1 = TRUE
                #Queen side castling (highlight positions for rook)
                self.castling_state_array[1] = True
                #self.LED_data[0][0] = self.dict["cyan"]
                #self.LED_data[0][3] = self.dict["cyan"]
                self.castle_move_highlight.append([0,0])
                self.castle_move_highlight.append([0,3])

            else:   #No castling occuring during this turn
                self.castling_state = False

        elif(self.board.turn == chess.WHITE):   #means white turn
            #check if white black pieces are castling
            if(self.move_buffer.uci() == "e8g8" and self.board.piece_at(chess.G8).symbol() == "k"):
                self.castling_state = True #MAKE CONDITION WHERE THE CASTLING IS FALSE. CHECK THE WHITE_POS ARRAY TO SEE IF H8 = FALSE AND F8 = TRUE
                #King side castling (highlight positions for rook)
                self.castling_state_array[2] = True
                #self.LED_data[7][7] = self.dict["cyan"]
                #self.LED_data[7][5] = self.dict["cyan"]
                self.castle_move_highlight.append([7,7])
                self.castle_move_highlight.append([7,5])

            elif(self.move_buffer.uci() == "e8c8" and self.board.piece_at(chess.C8).symbol() == "k"):
                self.castling_state = True   #MAKE CONDITION WHERE THE CASTLING IS FALSE. CHECK THE WHITE_POS ARRAY TO SEE IF A8 = FALSE AND D8 = TRUE
                #Queen side castling (highlight positions for rook)
                self.castling_state_array[3] = True
                #self.LED_data[7][0] = self.dict["cyan"]
                #self.LED_data[7][3] = self.dict["cyan"]
                self.castle_move_highlight.append([7,0])
                self.castle_move_highlight.append([7,3])

            else:   #No castling occuring during this turn
                self.castling_state = False

        if(self.castling_state == False):
            self.castle_move_highlight = [] #reset the array because castling was not done and is not in progress

        self.board.pop(move_buffer)   #need to popoff because don't want to actually make the move. just needed it to check for castling condition

        #Test if castle happened. (ONLY DO IF scenario == 3) // Need to manually comment it out
        #white_pos[0][5] = True  #User did the castle
        #self.castle_state_check()  #checks if there's castling in progress


    def promotion_check(self):
        # check if last move is on row 1 or row 8. Then check if the to_square has a pawn for the move.
        # if a pawn moved, then call a function to wait for the user to choose which piece he wants to promote to
        # based on the chosen piece, edit the move_made by appending a "q", "b", "r" or "n" (ex: a7a8q)
        # Make sure to make a condition that doesn't allow the code to go through the highlighting if a promotion is in progress
        pass

    def checking_king_check(self):
        [self.king_in_check, self.attackers_array] = self.Move_validation.is_check(self.board)
        if(self.king_in_check == True):
            print("A KING IS IN CHECK")
            #highlight king in red
            self.king_pos = self.board.king(self.board.turn)
            row = self.king_pos // 8
            col = self.king_pos % 8
            #self.LED_data[row][col] = self.dict["red"]
            king_check_highlight.append([row, col])

            #highlight attackers in red
            for x in range(0, len(self.attackers_array)):
                row = self.attackers_array[x] // 8
                col = self.attackers_array[x] % 8
                #self.LED_data[row][col] = self.dict["red"]
                king_check_highlight.append([row, col])

    #adds highlighting squares to array if a piece is lifted
    def piece_lifted(self):
        #highlight square that's lifted (blue)
        row = self.selected_piece // 8
        col = self.selected_piece % 8
        #self.LED_data[row][col] = self.dict["blue"]
        self.legal_move_highlight.append( [row, col, self.dict["blue"]])  #Add the lifted piece's location to the lifted piece's LED highlighting

        #show legal moves (green)
        self.array_legal_moves = self.Move_validation.piece_legal_moves(self.board, self.selected_piece)
        print("ARRAY_LEGAL_MOVES is ", self.array_legal_moves)
        #convert UCI to square number
        for x in range(0, len(self.array_legal_moves)):
            row = self.array_legal_moves[x].to_square // 8
            col = self.array_legal_moves[x].to_square % 8
            #self.LED_data[row][col] = self.dict["green"]
            self.legal_move_highlight.append( [row, col, self.LED_data[row][col] ])

    #checks where the piece is currently placed. Used to determine which LEDs to highlight. Only does something if an illegal move was made but was then corrected
    def placement_check(self):  #Only for illegal move highlighting
        print("\n", "Placement Check", "\n")
        if (self.illegal_move == True and len(self.illegal_array) !=0):    #remove illegal move highlighting if illegal moves were corrected. No illegal moves (were corrected) but highlighting is still on the board
            if (self.LED_data[ self.illegal_array[0][0] ][ self.illegal_array[0][1] ] == self.dict["yellow"]):  #Check for the first array index in the illegal_array to see if there are any illegal moves (if yellow then none of the highlights were removed)
                for y in range(0, len(self.illegal_array)): #could perform more than 1 illegal move in a row so remove all illegal moves
                    for x in range(0, 1):
                        self.LED_data[ self.illegal_array[y][x] ][ self.illegal_array[y][x+1] ] == self.dict["black"]
                self.illegal_array = []  #Remove all illegal moves from the array because they were corrected
        pass


    #pushes the move when the turn has ended
    #NEED TO CHANGE THIS CODE FOR THE NEW REVISION. IT WILL ALSO ASSIGN THE HIGHLIGHTING IN HERE.
    def end_turn_move(self):
        #Functions before this need to check if the last move the user made was a legal move before they end the turn
        #SHOULD I MAKE A CONDITION TO ALSO SEE IF illegal_move == false? (means and illegal move was last made)
        print("JKLSdJALKDJLSAKBCJKSAILJKBASLKHDBALSBJDKLAHSDBKLBADLKASBKLDBASLKDBKSALBDJKSALBDLKJSBDKLJASBKLDSBKLBDJKLASB")

        self.end_turn = True #TEMPORARILY. WILL NEED TO CHANGE THIS LATER
        if(self.end_turn == True):

            self.board.push(self.move_made)
            print("PUSHED THE MOVE@@@@@@@@@@@@@@@@@@@@@@@@@")
            print(self.move_made)
            self.end_turn = False    #The turn has ended and the move has been made so end_turn is false for the next player
            #prev_player_move = move_made #(used for highlighting last move made)
            self.clear_board_LED()

            #Move was made. Highlight prev_player_move cyan or other color (from and to square)
            self.last_move_highlight = []    #Reset it before appending new last move
            row_1 = self.move_buffer.from_square // 8
            col_1 = self.move_buffer.from_square % 8
            #self.LED_data[row_1][col_1] = self.dict["cyan"]
            self.last_move_highlight.append([row_1, col_1])
            row_2 = self.move_buffer.to_square // 8
            col_2 = self.move_buffer.to_square % 8
            #self.LED_data[row_2][col_2] = self.dict["cyan"]
            self.last_move_highlight.append([row_2, col_2])
            #Reset variables for the next player
            self.move_made = None    #clear because it's a new player's turn
            #temp_move_made = None
            #edge_move = None
            self.selected_piece = None
            #temp_selected_piece = None
            self.array_legal_moves = []  #new player turn so no move should be listed
            self.illegal_array = []  #should be cleared by the end of the turn
            self.illegal_move = False #should already be false. NOT SURE IF THIS IS NEEDED TO BE STATED HERE
            #save_lift_LED_color = []    #Saves the LED colors and its location for the lifted piece and its legal move

            #NOT SURE IF THE FOLLOWING ARE NEEDED
            #current_turn   = 0          #keeps track of the current turn (maybe use python-chess function to obtain time instead)
            self.castling_state = False      #Tracks if castling happened
            self.castling_state_array = [False, False, False, False]   # loc 1 - w_kingside, loc 2 - w_queenside, loc 3 - b_kingside, loc 4 - b_queenside

    def assign_highlight(self):
        '''
        legal_move_highlight =  [ [row, col, self.LED_data[row][col] ] , [row, col, self.LED_data[row][col] ], ....]    #holds locations to highlight for legal move highilighting
        last_move_highlight = [ [row, col], [row, col] ]    #holds locations to highlight for last move highlighting    #NEED TO MAKE LOGIC FOR THIS ARRAY
        illegal_move_highlight = [ [row, col], [row, col], ... ] #holds locations to highlight for illegal move highlighting #DON'T NEED THIS ARRAY BECAUSE I HAVE "illegal_array" already in placement_check()
        king_check_highlight = [ [row, col], [row, col], ... ]   #holds locations to highlight for king check highlighting #NEED TO MAKE LOGIC FOR THIS ARRAY
        castle_move_highlight = [ [row, col], [row, col]  ]  #holds locations to highlight for castle (if castling was done)
        '''

        #Make an array that assignments for move higlights

        #Legal Moves (THIS WILL HAVE A PROBLEM BECAUSE LEGAL_MOVES WILL ALWAYS BE APPENDED EACH TIME )
        for x in range(0, len(self.legal_move_highlight)):
            self.LED_data[self.legal_move_highlight[x][0]][self.legal_move_highlight[x][1]] = self.dict["green"]
        #Reset Legal Moves Array after adding them to the LED_data because it will duplicate next time.
        self.legal_move_highlight = []

        #Last Move
        for x in range(0, len(self.last_move_highlight)):   #Only 2 squares are higlighted
            self.LED_data[self.last_move_highlight[x][0]][self.last_move_highlight[x][1]] = self.dict["blue"]
        #Already cleared in "end_turn()"

        #Illegal Move (Technically this is already processed)
        for x in range(0, len(self.illegal_array)):
            self.LED_data[self.illegal_array[x][0]][self.illegal_array[x][1]] = self.dict["yellow"]

        #King Check
        for x in range(0, len(self.king_check_highlight)):
            self.LED_data[self.king_check_highlight[x][0]][self.king_check_highlight[x][1]] = self.dict["red"]
        #Reset the array
        self.king_check_highlight = []

        #Castle Check
        for x in range(0, len(self.castle_move_highlight)):
            self.LED_data[self.castle_move_highlight[x][0]][self.castle_move_highlight[x][1]]  = self.dict["cyan"]
        #Reset the array
        self.castle_move_highlight = []

    def live_move_highlight(self):
        [self.selected_piece, self.move_made] = self.Move_validation.determine_move_made(self.board, self.white_pos, self.black_pos)
        print("Selected piece/square: ",self.selected_piece)
        print("Move made: ", self.move_made)
        #self.placement_check() #check if the player corrected an illegal move if an illegal move was done.
        #if no move was made (just lifted a piece or nothing happens) then move_made = None. Will have to make a condition for that so that nothing on the board is highlighted unless if a piece is lifted
        #self.castle_state_check()  #checks if there's castling in progress
        if (self.selected_piece != None and self.castling_state == False):    #piece is lifted    (When swapping or killing a piece no square will be highlighted; the physical process of replacing and removing a piece on the board)

            if(self.last_selected_piece == None):   #No piece has been lifted during this player's turn yet.
                self.piece_lifted() #logic to load legal_move highlight squares

            elif(self.last_selected_piece != None): #to check if same piece was lifted from a different location (not original spot) during the same turn
                if(self.last_selected_piece == self.selected_piece): #means you are looking at the same piece during the same turn because the lift location is the same
                    pass #don't change the legal_move_highlight array

                else:   #Not the same piece. User lifted a different piece during the same turn. Need to change the legal_move_highlight array
                    self.legal_move_highlight = [] #reset the array to add new legal moves into legal_move_highlight array
                    self.piece_lifted()

            self.last_selected_piece = self.selected_piece  #to prevent repeatedly adding it every time we check the same square that had a piece lifted. Will need to set last_selected_piece = None at the end of the turn

        if(self.move_made != None and self.castling_state == False): #a move was made

            self.illegal_move = self.Move_validation.is_legal_move(self.board, self.move_made)  #check if move was illegal
            if(self.illegal_move == False):  #It is an illegal move
                #Do not push the move (don't update the board with the illegal move)
                #highlight yellow (from and to squares)
                row_1 = self.move_made.from_square //8   #assuming that it is actually from UCI and not just a regular string to make it have the appearance of UCI. If just a regular string with the look of UCI, then perform the code found at (***!!!)
                col_1 = self.move_made.from_square % 8
                #self.LED_data[row_1][col_1] = self.dict["yellow"]
                illegal_array.append([row_1, col_1]) #add the from and to squares to the illegal move array
                row_2 =  self.move_made.to_square //8
                col_2 =  self.move_made.to_square % 8
                #self.LED_data[row_2][col_2] = self.dict["yellow"]
                illegal_array.append([row_2, col_2])

                #touchscreen will need to make an if condition that stops other moves/highlighting/reading if an illegal move was made
                #if (self.illegal_move != False): #no illegal move was made
                    #call game reading funtions

            else:    #legal move was made (King check condition done elsewhere)
                self.move_buffer = self.move_made   #save the move for the move buffer
                #self.castle_highlight_check()    #checks if a castle was done
                #Will need a checking_promotion()
                #touchscreen can call checking_king_check to see if the king is in check at the beginning of a new turn



############################################################################################################
