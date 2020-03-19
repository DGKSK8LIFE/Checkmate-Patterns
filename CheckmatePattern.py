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
    
    def king_on_side(self, king):

        #01     34      123     4 0     
        # 2     2       0 4     321
        #43     10

        # If the king is on the left side
        if chess.square_file(king) == 0:
            return [king + 8, king + 9, king + 1, king - 7, king - 8]

        # If king is on right
        elif chess.square_file(king) == 7:
            return [king - 8, king - 9, king - 1, king + 7, king + 8]

        # Bottom
        elif chess.square_rank(king) == 0:
            return [king - 1, king + 7, king + 8, king + 9, king + 1]
        # Top
        elif chess.square_rank(king) == 7:
            return [king + 1, king - 7, king - 8, king - 9, king - 1]

    def king_on_corner(self, king):

        #21     12      0       0
        # 0     0      21       12

        if chess.square_file(king) == 0:
            # Bottom left
            if chess.square_rank(king) == 0:
                return [1, 9, 8]
            
            # Bottom right
            if chess.square_rank(king) == 7:
                return [6, 14, 15]

        if chess.square_file(king) == 7:
            # Top left
            if chess.square_rank(king) == 0:
                return [57, 49, 48]

            # Top right
            if chess.square_rank(king) == 7:
                return [62, 54, 55]

    def winner(self):
        if str(self.board.result()) == "1-0":
            return True
        else:
            return False

    ### Checkmate patterns

    def smothered(self, available_squares):
        # If all the squares around the king are blocked by its friendly pieces
        if all(self.is_blocked(i, not self.winner()) for i in available_squares):
            print('Smothered mate')
    
    def suffocation(self, available_squares):
        # If there is 2 squares that is not blocked by the king's own pieces and those 2 squares are attacked by the same piece
        squares_free = []
        for i in available_squares:
            if not self.is_blocked(i, not self.winner()):
                if len(squares_free) > 2:
                # found too many free squares
                    continue
                else:
                # found the first free square
                    squares_free.append(i)
        if len(squares_free) == 1:
            print('Suffocation mate')
        elif len(squares_free) == 2 and (self.board.attackers(self.winner(), squares_free[0]) == self.board.attackers(self.winner(), squares_free[1])):
            print('Suffocation mate')

    
    def suffocation_corner(self, available_squares):
        # If there is only 1 square that is not blocked by the king's own pieces
        one_square_free = False
        for i in available_squares:
            if not self.is_blocked(i, not self.winner()):
                if one_square_free:
                # found too many free squares
                    one_square_free = False
                else:
                # found the first free square
                    one_square_free = True
    # found zero or one True value
        if one_square_free:
            print('Suffocation mate')
        

    def back_rank(self, available_squares):
        # On a board, there are 2 realistic ways back ranks can happen (white checkmated on his side, and vice versa)
        if all(self.is_blocked(i, not self.winner()) for i in available_squares[1:4]):
            print('Back-rank mate')
        
    def back_rank_corner(self, available_squares):
        # Thre are 4 realistic ways back ranks with losing king on corner can happen
        if all(self.is_blocked(i, not self.winner()) for i in available_squares[1:]):
            print('Back-rank mate')

    def ladder(self, available_squares, square):
        # If all the remaining squares are attacked by a queen or a rook
        ladder = False
        for i in available_squares[1:4]:    
            for attacker in self.board.attackers(self.winner(), i):
                if self.board.color_at(attacker) == self.winner() and square != i and (str(self.board.piece_at(attacker)).upper() == 'Q' or str(self.board.piece_at(attacker)).upper() == 'R'):
                    # For some reason, it would print 'Ladder mate' 3 times. This just bypasses it.
                    ladder = True
        if ladder:
            print('Ladder mate')

    def scholars(self, available_squares, queen_pos):
        # If the queen is on f7 or f2 and a bishop on c4 or c5 (white and black, respectively) is defending it
        if self.winner():
            if queen_pos == chess.F7 and str(self.board.piece_at(chess.C4)) == 'B':
                print("Scholar's mate")
        else:
            if queen_pos == chess.F2 and str(self.board.piece_at(chess.C5)) == 'B':
                print("Scholar's mate")


    def epaulette(self, available_squares, queen_pos):
        # If the losing king is blocked by 2 pieces each on each side and the queen is 2 squares away from him
        distance_king_queen = chess.square_distance(self.board.king(not self.winner()), queen_pos)
        
        if self.is_blocked(available_squares[0], not self.winner()) and self.is_blocked(available_squares[4], not self.winner()) and distance_king_queen == 2:
            print('Epaulette mate')
    
    def find_checkmate_pattern(self):
        losing_side = not self.winner()
        opponent_king = self.board.king(losing_side)

        if self.board.is_checkmate:
            print(self.board)
            for square in self.board.checkers():
                if len(self.board.checkers()) > 1:
                    print('Double checkmate')
                    break
                try:
                    if ((chess.square_file(opponent_king) == 0 or chess.square_file(opponent_king) == 7) and 
                    (chess.square_rank(opponent_king) == 0 or chess.square_rank(opponent_king) == 7)): # Corner

                        available_squares = self.king_on_corner(opponent_king)
                        
                        if str(self.board.piece_at(square)).upper() == 'Q':
                            print(self.get_full_name('Q'), 'gave checkmate')

                            self.back_rank_corner(available_squares)

                        elif str(self.board.piece_at(square)).upper() == 'R':
                            print(self.get_full_name('R'), 'gave checkmate')

                            self.back_rank_corner(available_squares)
            
                        elif str(self.board.piece_at(square)).upper() == 'B':
                            print(self.get_full_name('B'), 'gave checkmate')

                        elif str(self.board.piece_at(square)).upper() == 'N':
                            print(self.get_full_name('N'), 'gave checkmate')

                            self.smothered(available_squares)
                            self.suffocation_corner(available_squares)
                            

                        elif str(self.board.piece_at(square)).upper() == 'P':
                            print(self.get_full_name('P'), 'checkmate!')

                    elif (chess.square_file(opponent_king) != 0 and chess.square_file(opponent_king) != 7 and 
                    chess.square_rank(opponent_king) != 0 and chess.square_rank(opponent_king) != 7): # Center
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
                    
                    else: # Side
                        available_squares = self.king_on_side(opponent_king)

                        if str(self.board.piece_at(square)).upper() == 'Q':
                            print(self.get_full_name('Q'), 'gave checkmate')

                            self.scholars(available_squares, square)
                            self.back_rank(available_squares)
                            self.ladder(available_squares)
                            self.epaulette(available_squares, square)

                        elif str(self.board.piece_at(square)).upper() == 'R':
                            print(self.get_full_name('R'), 'gave checkmate')

                            self.back_rank(available_squares)
                            self.ladder(available_squares)
            
                        elif str(self.board.piece_at(square)).upper() == 'B':
                            print(self.get_full_name('B'), 'gave checkmate')

                        elif str(self.board.piece_at(square)).upper() == 'N':
                            print(self.get_full_name('N'), 'gave checkmate')

                            self.smothered(available_squares)
                            self.suffocation(available_squares)

                        elif str(self.board.piece_at(square)).upper() == 'P':
                            print(self.get_full_name('P'), 'checkmate!')

                except TypeError:
                    # 100% error proof
                    pass

print(CheckmatePattern('4r3/2k5/8/P7/8/8/PPP5/1K1r4 w - - 1 2').find_checkmate_pattern())
