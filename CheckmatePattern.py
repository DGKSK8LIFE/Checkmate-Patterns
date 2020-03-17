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

        # King is in center
        if (self.is_in_board(surround[3]) and self.is_in_board(surround[4]) and 
            self.is_in_board(surround[0]) and self.is_in_board(surround[1]) and self.is_in_board(surround[2]) and
            self.is_in_board(surround[5]) and self.is_in_board(surround[6]) and self.is_in_board(surround[7])):
            return 0
        # Corner
        elif (chess.square_file(king) == 0 or chess.square_file(king) == 7) and (chess.square_rank(king) == 0 or chess.square_rank(king) == 7):
            return 2
        # Side
        else:
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

    def winner(self):
        if str(self.board.result()) == "1-0":
            return True
        else:
            return False

    # Checkmate patterns
    def smothered(self, available_squares):
        # If all the squares around the king are blocked by its friendly pieces
        if all(self.is_blocked(i, not self.winner()) for i in available_squares):
            print('Smothered mate')

    # Back rank checkmate depends on what side the king is on
    def back_rank(self, available_squares):
        '''
        if self.winner():
            if all(self.is_blocked(i, not self.winner()) for i in available_squares[-3:]):
                print('Back-rank mate')
        else: 
            if all(self.is_blocked(i, not self.winner()) for i in available_squares[:3]):
                print('Back-rank mate')
        '''
        pass

    def back_rank_corner(self, available_squares):
        '''
        if self.winner():
            if all(self.is_blocked(i, not self.winner()) for i in available_squares[:2]):
                print('Back-rank mate')
        else: 
            if all(self.is_blocked(i, not self.winner()) for i in available_squares[-2:]):
                print('Back-rank mate')
        '''
        pass
    
    def ladder(self, available_squares):
        
        pass

    def epaulette(self, available_squares):
        pass
        

    
    def find_checkmate_pattern(self):
        losing_side = not self.winner()
        opponent_king = self.board.king(losing_side)

        if self.board.is_checkmate:
            print(self.board)
            for square in self.board.checkers():
                if len(self.board.checkers()) > 1:
                    print('Double checkmate')
                    break

                if self.king_location(opponent_king) == 2:

                    available_squares = self.king_on_corner(opponent_king)

                    if str(self.board.piece_at(square)).upper() == 'Q':
                        print(self.get_full_name('Q'), 'gave checkmate')

                    elif str(self.board.piece_at(square)).upper() == 'R':
                        print(self.get_full_name('R'), 'gave checkmate')

                        self.back_rank_corner(available_squares)
        
                    elif str(self.board.piece_at(square)).upper() == 'B':
                        print(self.get_full_name('B'), 'gave checkmate')

                    elif str(self.board.piece_at(square)).upper() == 'N':
                        print(self.get_full_name('N'), 'gave checkmate')

                        self.smothered(available_squares)

                    elif str(self.board.piece_at(square)).upper() == 'P':
                        print(self.get_full_name('P'), 'checkmate!')
                
                elif self.king_location(opponent_king) == 1:
                    available_squares = self.king_on_side(opponent_king)

                    if str(self.board.piece_at(square)).upper() == 'Q':
                        print(self.get_full_name('Q'), 'gave checkmate')

                        self.back_rank(available_squares)
                        self.ladder(available_squares)

                    elif str(self.board.piece_at(square)).upper() == 'R':
                        print(self.get_full_name('R'), 'gave checkmate')

                        self.back_rank(available_squares)
                        self.ladder(available_squares)
        
                    elif str(self.board.piece_at(square)).upper() == 'B':
                        print(self.get_full_name('B'), 'gave checkmate')

                    elif str(self.board.piece_at(square)).upper() == 'N':
                        print(self.get_full_name('N'), 'gave checkmate')

                        self.smothered(available_squares)

                    elif str(self.board.piece_at(square)).upper() == 'P':
                        print(self.get_full_name('P'), 'checkmate!')
                else:
                    available_squares = self.surrounding_squares(opponent_king)

                    if str(self.board.piece_at(square)).upper() == 'Q':
                        print(self.get_full_name('Q'), 'gave checkmate')

                    elif str(self.board.piece_at(square)).upper() == 'R':
                        print(self.get_full_name('R'), 'gave checkmate')
        
                    elif str(self.board.piece_at(square)).upper() == 'B':
                        print(self.get_full_name('B'), 'gave checkmate')

                    elif str(self.board.piece_at(square)).upper() == 'N':
                        print(self.get_full_name('N'), 'gave checkmate')

                    elif str(self.board.piece_at(square)).upper() == 'P':
                        print(self.get_full_name('P'), 'checkmate!')


'''
# board1 = CheckmatePattern('7k/p2p2bp/1p1P2p1/8/2B2pNP/P4n2/R1P2Pb1/1R1Kr3 w - - 4 29') # White is checkmated
# board2 = CheckmatePattern('7k/5B2/6K1/4B3/8/8/8/8 b - - 62 100') # Black is checkmate
# smothered = CheckmatePattern('6rk/5Npp/8/8/8/8/1K2P3/8 b - - 1 1')
# smothered2 = CheckmatePattern('rnbqkbnr/pp1ppppp/2pN4/8/8/4Q3/PPPPPPPP/RNB1KB1R b KQkq - 1 1')
black_back_ranked = CheckmatePattern('2R3k1/5ppp/8/8/8/8/8/3K4 b - - 1 1')
white_back_ranked = CheckmatePattern('1k6/8/8/8/8/8/PPP5/K2r4 w - - 2 2')
double_checkmate = CheckmatePattern('5rk1/4Np1p/8/8/3B4/8/8/1K4R1 b - - 1 1')
ladder = CheckmatePattern('8/3k4/8/8/8/8/1r6/2q2K2 w - - 2 2')

white = True
black = False

# print(board1.find_checkmate_pattern())
# print(board2.find_checkmate_pattern())
print(black_back_ranked.find_checkmate_pattern())
print(white_back_ranked.find_checkmate_pattern())
print(double_checkmate.find_checkmate_pattern())
print(ladder.find_checkmate_pattern())
'''