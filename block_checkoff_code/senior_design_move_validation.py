import chess
import chess.uci

class move_validation:
	def __init__(self):
		pass
	#
	
	def determine_move_made(self, prev_board, white_pos, black_pos):
		print(prev_board)
		dict = prev_board.piece_map()
		print(2 in dict)
		current_turn = prev_board.turn
		
		for itr in range(64):
			if(current_turn != chess.WHITE):
				pass
				
			else:
				pass
			
			#
		#
	#
	
	def is_legal_move(self, board, move):
		is_legal_move = move in board.legal_moves;
		if(is_legal_move):
			board.push(move)
		#
		return is_legal_move;
	#
	
	def is_check(self, board):
		if(board.is_check()):
			king_pos = board.king(board.turn)
			attackers = board.attackers(chess.WHITE, king_pos)
			print(attackers)
			return [True, list(attackers)]
		#
		return [False, None]
	#
#
