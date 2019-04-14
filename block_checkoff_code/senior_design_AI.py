import chess
import chess.uci


#engine = chess.uci.popen_engine("./stockfish-10-linux/Linux/stockfish_10_x64")
#engine = chess.uci.popen_engine("./stockfish-10-linux/Linux/stockfish_10_x64")
engine = chess.uci.popen_engine("stockfish")
engine.uci()
print(engine.name,"\n" )

board = chess.Board()
print("Initial Board")
print(board, "\n")

Nf3 = chess.Move.from_uci("g1f3")
#print(Nf3 in board.legal_moves)
board.push(Nf3)
print("White Move 1")
print(board, "\n")

engine.ucinewgame()
engine.position(board)
board.push(engine.go(movetime=100).bestmove)
print("AI move 1")
print(board, "\n")

#Pe5 = chess.Move.from_uci("e2e5")
#print(Pe5 in board.legal_moves)
Pe4 = chess.Move.from_uci("e2e4")
#print(Pe4 in board.legal_moves)
board.push(Pe4)
print("White Move 2")
print(board, "\n")

engine.position(board)
board.push(engine.go(movetime=100).bestmove)
print("AI move 2")
print(board, "\n")
