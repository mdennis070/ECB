import chess
import chess.uci
import AI

'''
#   Notes
#   1) If more than 1 piece is lifted, then ignore and don't highlight anything on the board
#   2) Need to make periodic calls to refresh_board() -will need to make a counter/timer to determine when I do function calls to it



## TODO:
#   1) NEED TO FIND OUT HOW TO MAKE CODE TO ACCOMMODATE FOR PROMOTIONS!!!!
#   2) FINISH CASTLING_STATE_CHECK():
#   3)
'''






def clear_board_LED():
    LED_data = [[(0, 0, 0) for i in range(0, 8)] for j in range(0, 8)] #2D array of tuples indicating the color of each square. Initialize with all LEDs OFF


def determine_move_made(prev_board, white_pos, black_pos):

    #Test 1a (piece lifted)
    #hint_list = chess.D1  #White Queen at a2
    #move_list = None

    #Test 1b
    #hint_list = chess.H2  #White Pawn at H2
    #move_list = None


    #Test 2a (piece killed)
    #hint_list = None
    #g5_f6 = "g5f6"      #white bishop kills black pawn
    #move_list = chess.Move.from_uci(g5_f6)
    #print(move_list.from_square)
    #print(move_list.to_square)

    #Test 2b (piece killed and causes a check)
    #hint_list = None
    #f4_f7 = "f4f7"      #white bishop kills black pawn
    #move_list = chess.Move.from_uci(f4_f7)



    #Test 3a (piece moved (no kill))
    #hint_list = None
    #a2_a3 = "a2a3"
    #move_list = chess.Move.from_uci(a2_a3)
    #print(move_list.from_square)
    #print(move_list.to_square)

    #Test 3b (Piece moved (no kill))
    #hint_list = None
    #f1_a6 = "f1a6"
    #move_list = chess.Move.from_uci(f1_a6)
    #print(move_list.from_square)
    #print(move_list.to_square)


    #Test 4 (Castling)  #Use a special config without AI runs
    #Kingside castling
    hint_list = None
    e1_g1 = "e1g1"
    move_list = chess.Move.from_uci(e1_g1)
    print(move_list.from_square)
    print(move_list.to_square)

    '''
    #Queenside castling
    #e1_c1 =...
    '''
	#hint_list give you the square for the piece that you want to find moves for(ex: a number from 0 to 63). Move_list gives you a UCI move (ex: g1f3)
    return hint_list, move_list


def piece_legal_moves(board, piece):
	#returns an array of moves (UCI move formats ex: g1f3, g1b7)
    #piece = chess.D1    #White Queen
    legal_moves_list = []
    all_legal_moves = list(board.legal_moves)
    #print(all_legal_moves)
    for move in all_legal_moves:
        if move.from_square == piece:
            legal_moves_list.append(move)
    print("THE QUEEN'S LEGAL MOVES ARE: ", legal_moves_list)
    return legal_moves_list


def is_legal_move(board, move):
    return move in board.legal_moves;
#Boolean true or false


#Called all the time but only does something when there is a check fro the king
def is_check(board):
	if(board.is_check()):
		king_pos = board.king(board.turn)
		attackers = board.attackers(chess.WHITE, king_pos)
		#print(attackers)
		return [True, list(attackers)]
	#Returns a list of attackers in the form of which square they're coming from (ex: 0,1,4,23, 63)
	return [False, None]


def call_AI_function():
    print("AI MOVE NOW")
    #Function call to AI and it outputs the move
    piece_move = raydon_game.AI_move(board)
    print(piece_move)
    print(board)


def castle_state_check():
    #Check the state and see if the castling happened
    print("Check if castling is in progress")
    if(castling_state == True): #Enter this statement only if castling is in progress and check if it was executed
        print("CASTLING IN PROGRESS")
        x = 0
        for x in range(0,4):
            if (castling_state_array[x] == True):   #check which castling type should be checked
                break
        print(x) #check which castling type should be checked
        if(x == 0): #Check if white_kingside castling was done
            print("W Kingside")
            if(white_pos[0][5] == True):
                print("MAHO")
                castling_state_array[0] = False #castling is complete
        elif(x == 1):#Check if white_queenside castling was done
            print("W Queenside")
            if(white_pos[0][3] == True):
                print("MAHO")
                castling_state_array[1] = False #castling is complete
        elif(x == 2): #Check if black_kingside castling was done
            print("B Kingside")
            if(black_pos[7][5] == True):
                print("MAHO")
                castling_state_array[2] = False
        else:   #Check if black_kingside castling was done
            print("B Queenside")
            if(black_pos[7][3] == True):
                print("MAHO")
                castling_state_array[3] = False
    #end of castling_state if statement

    else: #No castling is in progress
        pass


def promotion_check():
    # check if last move is on row 1 or row 8. Then check if the to_square has a pawn for the move.
    # if a pawn moved, then call a function to wait for the user to choose which piece he wants to promote to
    # based on the chosen piece, edit the move_made by appending a "q", "b", "r" or "n" (ex: a7a8q)
    # Make sure to make a condition that doesn't allow the code to go through the highlighting if a promotion is in progress
    pass


#MAIN PROGRAM
brightness = 1
LED_data = [[(0, 0, 0) for i in range(0, 8)] for j in range(0, 8)] #2D array of tuples indicating the color of each square. Initialize with all LEDs OFF
#Color Scheme (tuples)
dict = {'red':(255,0,0), 'green':(0,255,0), 'blue':(0,0,255), 'majenta':(255,0,255), 'yellow':(255,255,0), 'cyan':(0, 255, 255), 'black':(0,0,0), 'white':(255,255,255)}

selected_piece = 0           #a square location (ex: 0 - 63)
move_made = None           #temporarily holds moves made (in UCI format ex: g1f3)
array_legal_moves = []    #will hold the squares for the legal moves
king_in_check   = False     #will hold true/false value that says if king is in check
king_pos = None    #will highlight king square in red
attackers_array = None      #will hold an array of the attackers if check
illegal_array   = None      #will hold array of two positions to show move from and move to square and highlight them yellow
illegal_move    = None     #will hold true/false value that says if an illegal move was made

highlight_turn = 0b0        #0 - means 1st player, 1 - means 2nd player
current_turn   = 0          #keeps track of the current turn (maybe use python-chess function to obtain time instead)
castling_state = False      #Tracks if castling happened
castling_state_array = [False, False, False, False]   # loc 1 - w_kingside, loc 2 - w_queenside, loc 3 - b_kingside, loc 4 - b_queenside
#Make board
board = chess.Board()
print("Initial Board")
print(board, "\n")









#Board setup for Testing

#raydon_game = AI.AI(3)  #For Test 1a, 1b, 2a
raydon_game = AI.AI(1)  #For Test 2b, 3a, 3b
#NO AI FOR CASTLING TEST

#for x in range(0,8):    #Only for Tests 1,2,3
#    call_AI_function()

#Castling Test Board (Special Test. Needs to be commented out when not doing Castling Test)
board.clear_board()
board.set_piece_at(chess.A1, chess.Piece.from_symbol('R')) #White ROOK
board.set_piece_at(chess.E1, chess.Piece.from_symbol('K'))
board.set_piece_at(chess.H1, chess.Piece.from_symbol('R'))
board.set_piece_at(chess.E8, chess.Piece.from_symbol('k'))
print(board)
#









print("DONE SETTING UP THE RANDOM BOARD", '\n')


#NEED TO THINK ABOUT HOW TO REMOVE HIGHLIGHTING after each turn have an array with any changes on the board based on a given round then clear the locations
white_pos = [[None for i in range(0,8)] for j in range(0,8)]
black_pos = [[None for i in range(0,8)] for j in range(0,8)]

#READ FROM ELECTRONICS Control
#CHECK IF CASTLING MOVES WERE MADE IF CASTLING_STATE == TRUE. IF CASTLING MOVES OCCURED, CHANGE CASTLING_STATE = FALSE
#THEN CALL DETERMINE_MOVE_MADE()
[selected_piece, move_made] = determine_move_made(board, white_pos, black_pos)
#if no move was made (just lifted a piece or nothing happens) then move_made = None. Will have to make a condition for that so that nothing on the board is highlighted unless if a piece is lifted
castle_state_check()  #checks if there's castling in progress
if (selected_piece != None and castling_state == False):    #piece is lifted    (When swapping or killing a piece no square will be highlighted; the physical process of replacing and removing a piece on the board)

    #highlight square that's lifted (blue)
    row = selected_piece // 8
    col = selected_piece % 8
    LED_data[row][col] = dict["blue"]

    #show legal moves (green)
    array_legal_moves = piece_legal_moves(board, selected_piece)
    print("ARRAY_LEGAL_MOVES is ", array_legal_moves)
    #convert UCI to square number
    for x in range(0, len(array_legal_moves)):
        row = array_legal_moves[x].to_square // 8
        col = array_legal_moves[x].to_square % 8
        LED_data[row][col] = dict["green"]

if(move_made != None and castling_state == False): #a move was made
    illegal_move = is_legal_move(board, move_made)
    if(illegal_move == False):  #It is an illegal move
        #Do not push the move (don't update the board with the illegal move)
        #highlight yellow (from and to squares)
        row_1 = move_made.from_square //8   #assuming that it is actually from UCI and not just a regular string to make it have the appearance of UCI. If just a regular string with the look of UCI, then perform the code found at (***!!!)
        col_1 = move_made.from_square % 8
        LED_data[row_1][col_1] = dict["yellow"]
        row_2 =  move_made.to_square //8
        col_2 =  move_made.to_square % 8
        LED_data[row_2][col_2] = dict["yellow"]

    else:   #legal move was made
        board.push(move_made)   #make the move on the board
        [king_in_check, attackers_array] = is_check(board)
        if(king_in_check == True):
            #highlight king in red
            king_pos = board.king(board.turn)
            row = king_pos // 8
            col = king_pos % 8
            LED_data[row][col] = dict["red"]
            #highlight attackers in red
            for x in range(0, len(attackers_array)):
                row = attackers_array[x] // 8
                col = attackers_array[x] % 8
                LED_data[row][col] = dict["red"]

            #Show where the piece came from
            row_1 = move_made.from_square // 8
            col_1 = move_made.from_square % 8
            LED_data[row_1][col_1] = dict["cyan"]

        else:   #a regular move, capture or castle was made
            #highlight cyan or other color (from and to square)
            row_1 = move_made.from_square // 8
            col_1 = move_made.from_square % 8
            LED_data[row_1][col_1] = dict["cyan"]
            row_2 = move_made.to_square // 8
            col_2 = move_made.to_square % 8
            LED_data[row_2][col_2] = dict["cyan"]
            #Castling highlight conditions
            if(board.turn == False):  #False means black turn. a push already happened so turn is swapped
                #Check white king moves (for Castling highlights)
                if(board.piece_at(chess.G1).symbol() == "K" and move_made.uci() == "e1g1" ):
                    castling_state = True   #MAKE CONDITION WHERE THE CASTLING IS FALSE. CHECK THE WHITE_POS ARRAY TO SEE IF H1 = FALSE AND F1 = TRUE
                    #King side castling (highlight positions for rook)
                    castling_state_array[0] = True
                    LED_data[0][7] = dict["cyan"]
                    LED_data[0][5] = dict["cyan"]
                elif(board.piece_at(chess.C1).symbol() == "K" and move_made.uci() == "e1c1" ):
                    castling_state = True   #MAKE CONDITION WHERE THE CASTLING IS FALSE. CHECK THE WHITE_POS ARRAY TO SEE IF A1 = FALSE AND D1 = TRUE
                    #Queen side castling (highlight positions for rook)
                    castling_state_array[1] = True
                    LED_data[0][0] = dict["cyan"]
                    LED_data[0][3] = dict["cyan"]


            elif(board.turn == True):   #means white turn
                #check if white black pieces are castling
                if(board.piece_at(chess.G8).symbol() == "k" and move_made.uci() == "e8g8" ):
                    castling_state = True #MAKE CONDITION WHERE THE CASTLING IS FALSE. CHECK THE WHITE_POS ARRAY TO SEE IF H8 = FALSE AND F8 = TRUE
                    #King side castling (highlight positions for rook)
                    castling_state_array[2] = True
                    LED_data[7][7] = dict["cyan"]
                    LED_data[7][5] = dict["cyan"]
                elif(board.piece_at(chess.C8).symbol() == "k" and move_made.uci() == "e8c8" ):
                    castling_state = True   #MAKE CONDITION WHERE THE CASTLING IS FALSE. CHECK THE WHITE_POS ARRAY TO SEE IF A8 = FALSE AND D8 = TRUE
                    #Queen side castling (highlight positions for rook)
                    castling_state_array[3] = True
                    LED_data[7][0] = dict["cyan"]
                    LED_data[7][3] = dict["cyan"]

            #also save this state so that even after someone lifts a piece, this will still be shown
# a1_a2 = "e1g1"      #white bishop kills black pawn
# move_made = chess.Move.from_uci(a1_a2)
# # board.push(move_made)
# print(board)

#Test if castle happened
#white_pos[0][5] = True  #User did the castle
castle_state_check()  #checks if there's castling in progress


print("PRINTING LED_DATA")
print(LED_data,'\n')
print(board,'\n')
print("DONE TEST")






'''(***!!!)
Convert a regular string to UCI string
ex:
    tempA = "g1f3"  #regular string
    Pe4 = chess.Move.from_uci(tempA)    #convert regular string into a UCI string
    print(Pe4.from_square)
    board.push(Pe4)                     #push the board
    print(board, "\n")

    board.pop()                         #pop the last move made. Did this to show that "Pe4 = chess.Move.from_uci(tempA)" is just a basic conversion and doesn't make a move
    print(board, "\n")

    tempB = "a2a4"
    Pe4 = chess.Move.from_uci(tempB)
    print(Pe4.from_square)
    board.push(Pe4)
    print(board, "\n")

'''
