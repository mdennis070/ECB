import chess
import chess.uci

class move_validation:
    def __init__(self):
        pass
    #

    def piece_legal_moves(self, board, piece):
        legal_moves_list = []
        all_legal_moves = list(board.legal_moves)

        for move in all_legal_moves:
            if move.from_square == piece and move.to_square != move.from_square:
                legal_moves_list.append(move)
            #
        #
        return legal_moves_list
    #

    def determine_move_made(self, prev_board, white_pos, black_pos):
        
        prev_piece_map = prev_board.piece_map()

        w_moved_from_here = []
        w_moved_to_here = []
        b_moved_from_here = []
        b_moved_to_here = []

        for itr_row in range(8):
            for itr_col in range(8):
                tile_index = itr_row * 8 + itr_col

                was_here = tile_index in prev_piece_map
                w_was_here = False
                b_was_here = False

                if was_here:
                    piece_color = prev_piece_map[tile_index].color
                    w_was_here = piece_color == chess.WHITE
                    b_was_here = piece_color == chess.BLACK 
                w_here = white_pos[itr_row][itr_col]
                b_here = black_pos[itr_row][itr_col]

                if w_was_here and not w_here:
                    w_moved_from_here.append(tile_index)
                elif not w_was_here and w_here:
                    w_moved_to_here.append(tile_index)
                #

                if b_was_here and not b_here:
                    b_moved_from_here.append(tile_index)
                elif not b_was_here and b_here:
                    b_moved_to_here.append(tile_index)	
                #
            #
        #

        """
        If white turn:
            -white piece moved and black piece removed (capture)
            -two white pieces moved (castle)
            -one white piece moved
            -one white piece remove (lifted for piece check)
        """
        current_turn = prev_board.turn

        len_w_to_here = len(w_moved_to_here)
        len_w_from_here = len(w_moved_from_here)
        len_b_to_here = len(b_moved_to_here)
        len_b_from_here = len(b_moved_from_here)
        
        w_capture_made = current_turn == chess.WHITE and len_w_to_here == 1 and len_w_from_here == 1 and len_b_from_here == 1 and len_b_to_here == 0
        b_capture_made = current_turn == chess.BLACK and len_b_to_here == 1 and len_b_from_here == 1 and len_w_from_here == 1 and len_w_to_here == 0

        w_move = current_turn == chess.WHITE and len_w_to_here == 1 and len_w_from_here == 1 and len_b_from_here == 0 and len_b_to_here == 0
        b_move = current_turn == chess.BLACK and len_b_to_here == 1 and len_b_from_here == 1 and len_w_from_here == 0 and len_w_to_here == 0

        w_castle = current_turn == chess.WHITE and len_w_to_here == 2 and len_w_from_here == 2 and len_b_from_here == 0 and len_b_to_here == 0
        b_castle = current_turn == chess.BLACK and len_b_to_here == 2 and len_b_from_here == 2 and len_w_from_here == 0 and len_w_to_here == 0

        w_hint = current_turn == chess.WHITE and len_w_to_here == 0 and len_w_from_here == 1
        b_hint = current_turn == chess.BLACK and len_b_to_here == 0 and len_b_from_here == 1

        capture_list = None
        move_list = None
        castle_list = None
        hint_list = None

        """capture to uci format"""
        if w_capture_made or b_capture_made:
            if current_turn == chess.WHITE and w_moved_to_here == b_moved_from_here:
                capture_list = chess.Move(w_moved_from_here[0], w_moved_to_here[0])
            elif b_moved_to_here == w_moved_from_here:
                capture_list = chess.Move(b_moved_from_here[0], b_moved_to_here[0])
        #
        elif w_move or b_move:
            if w_move:
                move_list = chess.Move(w_moved_from_here[0], w_moved_to_here[0])
            elif b_move:
                move_list = chess.Move(b_moved_from_here[0], b_moved_to_here[0])
        #
        elif w_castle or b_castle:
            if w_castle:
                k_kingside_castle_move = chess.E1 in w_moved_from_here and chess.G1 in w_moved_to_here
                r_kingside_castle_move = chess.H1 in w_moved_from_here and chess.F1 in w_moved_to_here
                k_queenside_castle_move = chess.E1 in w_moved_from_here and chess.C1 in w_moved_to_here
                r_queenside_castle_move = chess.A1 in w_moved_from_here and chess.D1 in w_moved_to_here

                if k_kingside_castle_move and r_kingside_castle_move:
                    castle_list = chess.Move.from_uci("e1g1")
                    print("White kingside")
                elif k_queenside_castle_move and r_queenside_castle_move:
                    castle_list = chess.Move.from_uci("e1c1")
                    print("White queenside")
            elif b_castle:
                k_kingside_castle_move = (chess.E8 in b_moved_from_here) and (chess.G8 in b_moved_to_here)
                r_kingside_castle_move = (chess.H8 in b_moved_from_here) and (chess.F8 in b_moved_to_here)
                k_queenside_castle_move = (chess.E8 in b_moved_from_here) and (chess.C8 in b_moved_to_here)
                r_queenside_castle_move = (chess.A8 in b_moved_from_here) and (chess.D8 in b_moved_to_here)

                if k_kingside_castle_move and r_kingside_castle_move:
                    castle_list = chess.Move.from_uci("e8g8")
                    print("Black kingside")
                elif k_queenside_castle_move and r_queenside_castle_move:
                    castle_list = chess.Move.from_uci("e8c8")
                    print("Black kingside")
                #
            #
        elif w_hint or b_hint:
            if w_hint:
                hint_list = w_moved_from_here[0]
            elif b_hint:
                hint_list = b_moved_from_here[0]
            #
        else:
            # illegal move made
            pass
        #
        
        if move_list != None:
            return hint_list, move_list, castle_list
        if capture_list != None:
            return hint_list, capture_list, castle_list

        return hint_list, move_list, castle_list
    #

    def is_legal_move(self, board, move):
        return (move in board.legal_moves)
    #

    def is_check(self, board):
        if(board.is_check()):
            king_pos = board.king(board.turn)
            attackers = board.attackers(not board.turn, king_pos)

            return [True, list(attackers)]
        #
        return [False, None]
    #

