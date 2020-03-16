import chess

class CheckmatePattern:

    def __init__(self, board):
        self.board = chess.Board(board)

    def get_full_name(self, letter):
        full_piece_names = {
            'Q': 'Queen',
            'R': 'Rook',
            'B': 'Bishop',
            'N': 'Knight',
            'P': 'Pawn'
        }
        return full_piece_names[letter.upper()]

    def is_in_board(self, square):
        if (square > 0) and (square < 63):
            return True
        else:
            return False

    def valid_squares(self, valid, non_valid):
        for squares in sorted(non_valid, reverse=True):
            del valid[squares]
        return valid

    # Check if a square around the king is blocked by his own piece
    def is_blocked(self, square, side):
        if self.board.color_at(square) == side:
            return True
        else:
            return False

    def surrounding_squares(self, king):
        return [king + 7, king + 8, king + 9,
                king - 1,           king + 1,
                king - 9, king - 8, king - 7]

    def king_location(self, king):
        surround = self.surrounding_squares(king)

        if (self.is_in_board(surround[3]) and self.is_in_board(surround[4]) and 
            self.is_in_board(surround[0]) and self.is_in_board(surround[1]) and self.is_in_board(surround[2]) and
            self.is_in_board(surround[5]) and self.is_in_board(surround[6]) and self.is_in_board(surround[7])):
            print('King in center!')
            return 0
        elif (chess.square_file(king) == 0 or chess.square_file(king) == 7) and (chess.square_rank(king) == 0 or chess.square_rank(king) == 7):
            print('King on corner')
            return 2
        else:
            print('King on side')
            return 1
    
    def king_on_side(self, king):
        surround = self.surrounding_squares(king)

        # If the king is on the left side
        if chess.square_file(king) == 0:
            return valid_squares(surround, [king + 7, king - 1, king - 9])

        # If king is on right
        elif chess.square_file(king) == 7:
            return valid_squares(surround, [king + 9, king + 1, king - 7])

        # Bottom
        elif chess.square_rank(king) == 0:
            return surround[:5]
        # Top
        elif chess.square_rank(king) == 7:
            return surround[3:]

    def king_on_corner(self, king):
        surround = self.surrounding_squares(king)

        if chess.square_file(king) == 0:
            # Bottom left
            if chess.square_rank(king) == 0:
                return [1, 8, 9]
            
            # Bottom right
            if chess.square_rank(king) == 7:
                return [6, 14, 15]

        if chess.square_file(king) == 7:
            # Top left
            if chess.square_rank(king) == 0:
                return [48, 49, 57]

            # Top right
            if chess.square_rank(king) == 7:
                print('King top right!')
                return [54, 55, 62]
    
    def find_checkmate_pattern(self, victorious_side):
        opponent_king = self.board.king(not victorious_side)

        if self.board.is_checkmate:
            print(self.board)

            for square in self.board.checkers():
                if self.king_location(opponent_king) == 2:
                    available_squares = self.king_on_corner(opponent_king)

                    if str(self.board.piece_at(square)).upper() == 'Q':
                        print(get_full_name('Q'), 'gave checkmate')

                    elif str(self.board.piece_at(square)).upper() == 'R':
                        print(self.get_full_name('R'), 'gave checkmate')
        
                    elif str(self.board.piece_at(square)).upper() == 'B':
                        print(self.get_full_name('B'), 'gave checkmate')

                    
                    elif str(self.board.piece_at(square)).upper() == 'N':
                        print(self.get_full_name('N'), 'gave checkmate')
                    elif str(self.board.piece_at(square)).upper() == 'P':
                        print(self.get_full_name('P'), 'gave checkmate')
                
                elif self.king_location(opponent_king) == 1:
                    available_squares = self.king_on_side(opponent_king)

                    if str(self.board.piece_at(square)).upper() == 'Q':
                        print(get_full_name('Q'), 'gave checkmate')

                    elif str(self.board.piece_at(square)).upper() == 'R':
                        print(self.get_full_name('R'), 'gave checkmate')
        
                    elif str(self.board.piece_at(square)).upper() == 'B':
                        print(self.get_full_name('B'), 'gave checkmate')

                    elif str(self.board.piece_at(square)).upper() == 'N':
                        print(self.get_full_name('N'), 'gave checkmate')
                    elif str(self.board.piece_at(square)).upper() == 'P':
                        print(self.get_full_name('P'), 'gave checkmate')


board1 = CheckmatePattern('7k/p2p2bp/1p1P2p1/8/2B2pNP/P4n2/R1P2Pb1/1R1Kr3 w - - 4 29') # White is checkmated
board2 = CheckmatePattern('7k/5B2/6K1/4B3/8/8/8/8 b - - 62 100') # Black is checkmated

white = True
black = False

print(board1.find_checkmate_pattern(black))
print(board2.find_checkmate_pattern(white))