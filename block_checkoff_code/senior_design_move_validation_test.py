import chess
import chess.uci

from senior_design_move_validation import move_validation as Validation

board = chess.Board()
board_2 = chess.Board()
validation = Validation()

"""Test 1"""
print("Test 1\n")
print(board, "\n")
Pe5 = chess.Move.from_uci("e2e5")
print("Move e2e5 is legal:", validation.is_legal_move(board, Pe5))
Nf3 = chess.Move.from_uci("g1f3")
print("Move g1f3 is legal:", validation.is_legal_move(board, Nf3))

print("\n")
print(board, "\n")


"""Test 2"""
def func(my_str, color):
	print(my_str)
	[in_check, attack_pieces] = validation.is_check(board_2)
	print("is", color, "in check:", in_check)
	if(in_check):
		print(attack_pieces)
	print("\n")
	print(board_2, "\n")
#

print("Test 2\n")
print("Initial board")
print("is check", validation.is_check(board_2))
print("\n")
print(board_2, "\n")

board_2.push_san("e4")
func("Move 1 - WHITE", "white")

board_2.push_san("e5")
func("Move 1 - BLACK", "black")

board_2.push_san("Qh5")
func("Move 2 - WHITE", "white")

board_2.push_san("Nc6")
func("Move 2 - BLACK", "black")

board_2.push_san("Bc4")
func("Move 3 - WHITE", "white")

board_2.push_san("Nf6")
func("Move 3 - BLACK", "black")

board_2.push_san("Qxe5")
func("Move 4 - WHITE", "white")
