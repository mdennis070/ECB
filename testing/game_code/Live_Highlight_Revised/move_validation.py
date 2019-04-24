import chess
import chess.uci

class move_validation:
	def __init__(self):
		pass
	#

	def piece_legal_moves(self, board, piece):
		legal_moves_list = []
		all_legal_moves = list(board.legal_moves)
		#print(all_legal_moves)
		for move in all_legal_moves:
			if move.from_square == piece:
				legal_moves_list.append(move)
			#
		#
		#print("THE QUEEN'S LEGAL MOVES ARE: ", legal_moves_list) 	#REMOVE THIS LATER
		return legal_moves_list
	#


#Temporarily for test 2
	def determine_move_made(self, prev_board, white_pos, black_pos):
		print("\n\n\n\n")
		print("IN DETERMINE MOVE MADE")
		hint_list = None
		move_list = None

		#prompt for level of difficulty
		temp_test_case = input("Choose a test_case: ")
		print("Test_case is " + temp_test_case, "\n")

		test_case = int(temp_test_case)

		if(test_case == 1):	#Only for SCENARIO 1
			#Test 1a (piece lifted)
			print("In test_case 1")
			hint_list = chess.D1  #White Queen at a2
			move_list = None

		if(test_case == 2):	#Only for SCENARIO 1
			#Test 1b
			hint_list = chess.H2  #White Pawn at H2
			move_list = None

		if(test_case == 3): #Only for SCENARIO  1
			#Test 2a (piece killed)
			hint_list = None
			g5_f6 = "g5f6"      #white bishop kills black pawn
			move_list = chess.Move.from_uci(g5_f6)
			print(move_list.from_square)
			print(move_list.to_square)

		if(test_case == 4): #Only for SCENARIO 2
			#Test 2b (piece killed and causes a check)
			hint_list = None
			f4_f7 = "f4f7"      #white bishop kills black pawn
			move_list = chess.Move.from_uci(f4_f7)
			print("move the queen")
			print(move_list)

		if(test_case == 5): #Only for SCENARIO 2
			#Test 3a (piece moved (no kill))
			hint_list = None
			a2_a3 = "a2a3"
			move_list = chess.Move.from_uci(a2_a3)
			print(move_list.from_square)
			print(move_list.to_square)

		if(test_case == 6): #Only for SCENARIO 2
			#Test 3b (Piece moved (no kill))
			hint_list = None
			f1_a6 = "f1a6"
			move_list = chess.Move.from_uci(f1_a6)
			print(move_list.from_square)
			print(move_list.to_square)

		if(test_case == 7):	#Only for SCENARIO 3
			#Test 4 (Castling)  #Use a special config without AI runs
			#Kingside castling
			hint_list = None
			e1_g1 = "e1g1"
			move_list = chess.Move.from_uci(e1_g1)
			print(move_list.from_square)
			print(move_list.to_square)

		if(test_case == 8): #White
			#Test 5a (piece moved (no kill)). Pawn Move
			hint_list = None
			a2_a3 = "a2a3"
			move_list = chess.Move.from_uci(a2_a3)
			print(move_list.from_square)
			print(move_list.to_square)

		if(test_case == 9): #White
			#Test 5b (piece moved (no kill)). Pawn move
			hint_list = None
			a2_a4 = "a2a4"
			move_list = chess.Move.from_uci(a2_a4)
			print(move_list.from_square)
			print(move_list.to_square)

		if(test_case == 10): #White
			#Test 5c (piece moved (no kill)). Knight move
			hint_list = None
			b1_a3 = "b1a3"
			move_list = chess.Move.from_uci(b1_a3)
			print(move_list.from_square)
			print(move_list.to_square)

		if(test_case == 11): #Black
			#Test 5d(piece moved (no kill)). Knight move
			hint_list = None
			a2_a4 = "a2a4"
			move_list = chess.Move.from_uci(a2_a4)
			print(move_list.from_square)
			print(move_list.to_square)


		if(test_case == 1001): #after test_case 1a. So  1 --> 1001
			hint_list = None
			d1_a4 = "d1a4"
			move_list = chess.Move.from_uci(d1_a4)
			print(move_list.from_square)
			print(move_list.to_square)

		print("In function- Hint list:", hint_list )
		print("In function- move_made:", move_list, "\n" )
		return hint_list, move_list

		'''
	#Temporarily replacing this function with my test code
	def determine_move_made(self, prev_board, white_pos, black_pos):
		#self.AI_player = AI.AI(3)  #For Test 1a, 1b, 2a
		#self.AI_player = AI.AI(1)  #For Test 2b, 3a, 3b


		#NO AI FOR CASTLING TEST
		#{
		#for x in range(0,8):    #Only for Tests 1,2,3
		#    self.AI_player.AI_move(self.board)

		#Castling Test Board (Special Test. Needs to be commented out when not doing Castling Test)
		# board.clear_board()
		# board.set_piece_at(chess.A1, chess.Piece.from_symbol('R')) #White ROOK
		# board.set_piece_at(chess.E1, chess.Piece.from_symbol('K'))
		# board.set_piece_at(chess.H1, chess.Piece.from_symbol('R'))
		# board.set_piece_at(chess.E8, chess.Piece.from_symbol('k'))
		# print(board)
		#
		#}


		#Test 1a (piece lifted)
		#hint_list = chess.D1  #White Queen at a2
		#move_list = None

		#Test 1b
		#hint_list = chess.H2  #White Pawn at H2
		#move_list = None


		#Test 2a (piece killed)
		# hint_list = None
		# g5_f6 = "g5f6"      #white bishop kills black pawn
		# move_list = chess.Move.from_uci(g5_f6)
		# print(move_list.from_square)
		# print(move_list.to_square)

		#Test 2b (piece killed and causes a check)
		# hint_list = None
		# f4_f7 = "f4f7"      #white bishop kills black pawn
		# move_list = chess.Move.from_uci(f4_f7)
		# print("move the queen")
		# print(move_list)

		#Test 3a (piece moved (no kill))
		hint_list = None
		a2_a3 = "a2a3"
		move_list = chess.Move.from_uci(a2_a3)
		print(move_list.from_square)
		print(move_list.to_square)

		#Test 3b (Piece moved (no kill))
		# hint_list = None
		# f1_a6 = "f1a6"
		# move_list = chess.Move.from_uci(f1_a6)
		# print(move_list.from_square)
		# print(move_list.to_square)


		#Test 4 (Castling)  #Use a special config without AI runs
		#Kingside castling
		# hint_list = None
		# e1_g1 = "e1g1"
		# move_list = chess.Move.from_uci(e1_g1)
		# print(move_list.from_square)
		# print(move_list.to_square)

		'''
		#Queenside castling
		#e1_c1 =...
		'''
    	#hint_list give you the square for the piece that you want to find moves for(ex: a number from 0 to 63). Move_list gives you a UCI move (ex: g1f3)

		return hint_list, move_list
	#
	'''


	def is_legal_move(self, board, move):
		return move in board.legal_moves;
	#    #Boolean true or false

    #Called all the time but only does something when there is a check fro the king
	def is_check(self,board):
		if(board.is_check()):
			king_pos = board.king(board.turn)
			attackers = board.attackers(chess.WHITE, king_pos)
    		#print(attackers)
			return [True, list(attackers)]
    	#Returns a list of attackers in the form of which square they're coming from (ex: 0,1,4,23, 63)
		return [False, None]
	#
#
