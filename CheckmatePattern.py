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
    def is_blocked(self, square):
        if self.board.color_at(square) == (not self.winner()):
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

        if chess.square_rank(king) == 0:
            # Bottom left
            if chess.square_file(king) == 0:
                return [1, 9, 8]
            
            # Bottom right
            if chess.square_file(king) == 7:
                return [6, 14, 15]

        if chess.square_rank(king) == 7:
            # Top left
            if chess.square_file(king) == 0:
                return [57, 49, 48]

            # Top right
            if chess.square_file(king) == 7:
                return [62, 54, 55]

    def winner(self):
        if str(self.board.result()) == "1-0":
            return True
        else:
            return False

    ### Checkmate patterns

    def smothered(self, available_squares):
        # If all the squares around the king are blocked by its friendly pieces
        if all(self.is_blocked(i) for i in available_squares):
            print('Smothered mate')
    
    def suffocation_and_pillsburys(self, available_squares, square):
        # If there is 2 squares that is not blocked by the king's own pieces and those 2 squares are attacked by the same piece
        # This algorithm checks the suffocation mate (with knight) and Pillsbury's mate (with rook)
        squares_free = []
        for i in available_squares:
            if not self.is_blocked(i):
                if len(squares_free) > 2:
                # found too many free squares
                    continue
                else:
                # found the first free square
                    squares_free.append(i)
        if str(self.board.piece_at(square)).upper() == 'N':
            if len(squares_free) == 1:
                print('Suffocation mate')
            elif len(squares_free) == 2 and (self.board.attackers(self.winner(), squares_free[0]) == self.board.attackers(self.winner(), squares_free[1])):
                print('Suffocation mate')
        elif str(self.board.piece_at(square)).upper() == 'R':
            if len(squares_free) <= 2:
                print("Pillsbury's mate")
    
    def suffocation_corner(self, available_squares):
        # If there is only 1 square that is not blocked by the king's own pieces
        one_square_free = False
        for i in available_squares:
            if not self.is_blocked(i):
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
        if all(self.is_blocked(i) for i in available_squares[1:4]):
            print('Back-rank mate')
        
    def back_rank_corner(self, available_squares):
        # Thre are 4 realistic ways back ranks with losing king on corner can happen
        if all(self.is_blocked(i) for i in available_squares[1:]):
            print('Back-rank mate')

    def scholars(self, available_squares, queen_pos):
        # If the queen is on f7 or f2 and a bishop on c4 or c5 (white and black, respectively) is defending it
        if self.winner():
            if queen_pos == chess.F7 and str(self.board.piece_at(chess.C4)) == 'B':
                print("Scholar's mate")
        else:
            if queen_pos == chess.F2 and str(self.board.piece_at(chess.C5)) == 'B':
                print("Scholar's mate")

    def anastasias(self, available_squares):
        # If the king is blocked by one of his own pieces and the remaining squares are control by the knight and a rook in a particular manner
        squares_free = [available_squares[1], available_squares[3]]
        anastasias = False
        if self.board.attackers(self.winner(), squares_free[0]) == self.board.attackers(self.winner(), squares_free[0]):
            for i in squares_free:
                for attacker in self.board.attackers(self.winner(), i):
                    if str(self.board.piece_at(attacker)).upper() == 'N':
                        print("Anastasia's mate")

    def anastasias_corner(self, available_squares):
        for attacker in self.board.attackers(self.winner(), available_squares[0]):
            if self.is_blocked(available_squares[1]) and str(self.board.piece_at(attacker)).upper() == 'N':
                print("Anastasia's mate")

    def arabian(self, available_squares, rook_pos):
        for attacker in self.board.attackers(self.winner(), rook_pos):
            if str(self.board.piece_at(attacker)).upper() == 'N' and chess.square_distance(self.board.king(not self.winner()), attacker) == 2:
                print('Arabian mate')

    def epaulette(self, available_squares, queen_pos):
        # If the losing king is blocked by 2 pieces each on each side and the queen is 2 squares away from him
        distance_king_queen = chess.square_distance(self.board.king(not self.winner()), queen_pos)
        
        if self.is_blocked(available_squares[0]) and self.is_blocked(available_squares[4]) and distance_king_queen == 2:
            print('Epaulette mate')
    
    def blind_swine(self, available_squares):
        only_one_square_blocked = False
        for i in available_squares:
            if self.is_blocked(i):
                if only_one_square_blocked:
                    only_one_square_blocked = False
                else:
                    only_one_square_blocked = True
    
        if self.is_blocked(available_squares[4]) and only_one_square_blocked:
            if str(self.board.piece_at(available_squares[1])).upper() == 'R':
                print('Blind swine mate')

        elif self.is_blocked(available_squares[0]) and only_one_square_blocked:
            if str(self.board.piece_at(available_squares[3])).upper() == 'R':
                print('Blind swine mate')

    def swallows_tail(self, available_squares, square):
        if ((self.is_blocked(available_squares[0]) and self.is_blocked(available_squares[2])) or 
        (self.is_blocked(available_squares[2]) and self.is_blocked(available_squares[7])) or 
        (self.is_blocked(available_squares[7]) and self.is_blocked(available_squares[5])) or 
        (self.is_blocked(available_squares[5]) and self.is_blocked(available_squares[0])) and 
        chess.square_distance(self.board.king(not self.winner()), square)):
            print("Swallow's tail mate")

    def corner_and_morphys(self, available_squares, square):
        # This pattern takes care of the corner mate (given with knight) and Murphy's mate (given with bishop)
        if (self.is_blocked(available_squares[2])):
            for i in available_squares[1:]:
                for attacker in self.board.attackers(self.winner(), i):
                    if str(self.board.piece_at(attacker)).upper() == 'R' or str(self.board.piece_at(attacker)).upper() == 'Q':
                        if str(self.board.piece_at(square)).upper() == 'B':
                            print("Morphy's mate")
                        elif str(self.board.piece_at(square)).upper() == 'N':
                            print('Corner mate')

    def lollis(self, available_squares, square):
        for defender in self.board.attackers(self.winner(), square):
            if str(self.board.piece_at(defender)).upper() == 'P':
                if self.winner():
                    if chess.square_rank(square) == 6 and chess.square_rank(defender) == 5:
                        print("Lolli's mate")
                else:
                    if chess.square_rank(square) == 1 and chess.square_rank(defender) == 2:
                        print("Lolli's mate")

    def opera(self, available_squares, square):
        if square == available_squares[0] and self.is_blocked(available_squares[3]):
            for defender in self.board.attackers(self.winner(), available_squares[0]):
                if str(self.board.piece_at(defender)) == 'B':
                    print('Opera mate')
        elif square == available_squares[4] and self.is_blocked(available_squares[1]):
            for defender in self.board.attackers(self.winner(), available_squares[4]):
                if str(self.board.piece_at(defender)) == 'B':
                    print('Opera mate')

    def mayets(self, available_squares, square):
        if square == available_squares[0] and (self.is_blocked(available_squares[1]) or self.is_blocked(available_squares[2])):
            for defender in self.board.attackers(self.winner(), available_squares[0]):
                if str(self.board.piece_at(defender)) == 'B':
                    print("Mayet's mate")
        elif square == available_squares[4] and (self.is_blocked(available_squares[2]) or self.is_blocked(available_squares[3])):
            for defender in self.board.attackers(self.winner(), available_squares[0]):
                if str(self.board.piece_at(defender)) == 'B':
                    print("Mayet's mate")

    def mayets_corner(self, available_squares, square):
        if square == available_squares[0] and (self.is_blocked(available_squares[2]) or self.is_blocked(available_squares[1])):
            for defender in self.board.attackers(self.winner(), available_squares[0]):
                if str(self.board.piece_at(defender)) == 'B':
                    print("Mayet's mate")

    def ladder(self, available_squares, square):
        # If all the remaining squares are attacked by a queen or a rook
        ladder = False
        remaining_squares = [available_squares[0], available_squares[4]]

        for i in available_squares[1:4]:    
            for attacker in self.board.attackers(self.winner(), i):
                if (self.board.color_at(attacker) == self.winner() and square != i and 
                (str(self.board.piece_at(attacker)).upper() == 'Q' or str(self.board.piece_at(attacker)).upper() == 'R')):
                    # For some reason, it would print 'Ladder mate' 3 times. This just bypasses it.
                    ladder = True

        for i in remaining_squares:
            for attacker in self.board.attackers(self.winner(), i):
                if str(self.board.piece_at(attacker)).upper() == 'R' or str(self.board.piece_at(attacker)).upper() == 'Q':
                    ladder = True
                else:
                    ladder = False
        if ladder:
            print('Ladder mate')
    
    def ladder_corner(self, available_squares, square):
        # 8 plausible ways to get ladder mated on a corner
        ladder = False
        if chess.square_file(square) == 0 or chess.square_file(square) == 7:
            for i in available_squares[:2]:    
                for attacker in self.board.attackers(self.winner(), i):
                    if (self.board.color_at(attacker) == self.winner() and square != i and 
                    (str(self.board.piece_at(attacker)).upper() == 'Q' or str(self.board.piece_at(attacker)).upper() == 'R')):
                        ladder = True

            for attacker in self.board.attackers(self.winner(), available_squares[2]):
                if str(self.board.piece_at(attacker)).upper() == 'R' or str(self.board.piece_at(attacker)).upper() == 'Q':
                    ladder = True
                else:
                    ladder = False

        elif chess.square_rank(square) == 0 or chess.square_rank(square) == 7:
            for i in available_squares[1:]:    
                for attacker in self.board.attackers(self.winner(), i):
                    if (self.board.color_at(attacker) == self.winner() and square != i and 
                    (str(self.board.piece_at(attacker)).upper() == 'Q' or str(self.board.piece_at(attacker)).upper() == 'R')):
                        ladder = True

            for attacker in self.board.attackers(self.winner(), available_squares[0]):
                if str(self.board.piece_at(attacker)).upper() == 'R' or str(self.board.piece_at(attacker)).upper() == 'Q':
                    ladder = True
                else:
                    ladder = False

        if ladder:
            print('Ladder mate')
    
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
                            self.ladder_corner(available_squares, square)

                        elif str(self.board.piece_at(square)).upper() == 'R':
                            print(self.get_full_name('R'), 'gave checkmate')

                            self.back_rank_corner(available_squares)
                            self.anastasias_corner(available_squares)
                            self.arabian(available_squares, square)
                            self.mayets_corner(available_squares, square)
                            self.ladder_corner(available_squares, square)
            
                        elif str(self.board.piece_at(square)).upper() == 'B':
                            print(self.get_full_name('B'), 'gave checkmate')

                            self.corner_and_morphys(available_squares, square)

                        elif str(self.board.piece_at(square)).upper() == 'N':
                            print(self.get_full_name('N'), 'gave checkmate')

                            self.smothered(available_squares)
                            self.suffocation_corner(available_squares)
                            self.corner_and_morphys(available_squares, square)
                            
                        elif str(self.board.piece_at(square)).upper() == 'P':
                            print(self.get_full_name('P'), 'checkmate!')

                    elif (chess.square_file(opponent_king) != 0 and chess.square_file(opponent_king) != 7 and 
                    chess.square_rank(opponent_king) != 0 and chess.square_rank(opponent_king) != 7): # Center
                        available_squares = self.surrounding_squares(opponent_king)

                        if str(self.board.piece_at(square)).upper() == 'Q':
                            print(self.get_full_name('Q'), 'gave checkmate')

                            self.swallows_tail(available_squares, square)

                        elif str(self.board.piece_at(square)).upper() == 'R':
                            print(self.get_full_name('R'), 'gave checkmate')

                            self.blind_swine(available_squares)
            
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

                            self.lollis(available_squares, square)
                            self.scholars(available_squares, square)
                            self.back_rank(available_squares)
                            self.epaulette(available_squares, square)
                            self.ladder(available_squares, square)

                        elif str(self.board.piece_at(square)).upper() == 'R':
                            print(self.get_full_name('R'), 'gave checkmate')
                            
                            self.suffocation_and_pillsburys(available_squares, square)
                            self.blind_swine(available_squares)
                            self.back_rank(available_squares)
                            self.anastasias(available_squares)
                            self.opera(available_squares, square)
                            self.ladder(available_squares, square)
            
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

print(CheckmatePattern('4B3/8/1p6/k7/R5K1/8/8/8 b - - 1 1').find_checkmate_pattern())
print(CheckmatePattern('kR6/p7/8/8/8/6B1/K7/8 b - - 1 1').find_checkmate_pattern())
