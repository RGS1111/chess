import numpy as np
import itertools

class board:
    def __init__(self):
        self.board_array = np.zeros((8,8), dtype=int)
        #flipped_array = np.flip(board_array) (not needed since i have the negative number logic
        #for opposing player)
        count_p1 = 0
        for row in range(0,2):
            for column in range (0,8):
                count_p1 = count_p1 + 1
                self.board_array[row, column] = count_p1
        count_p2 = 0
        for row in range(6,8):
            for column in range (0,8):
                count_p2 = count_p2 - 1
                self.board_array[row, column] = count_p2
    def game_view(self):
        print(self.board_array)

    def sign_check(self, piece_id):
            # sign of piece_id compared to biggefr or smaller than 0 returning true or false aka 1 or 0 
            # and then if bigger than 0, then the same piece_id is NOT smaller than 0, so 0 
            # therefore 1 - 0 = +1 or if opposite example 0 - 1 = -1, thus determining sign
            print(int(piece_id > 0), int(piece_id < 0))
            return (int(piece_id > 0) - int(piece_id < 0))
    
    # returns the piece id, for checking of piece
    def get_piece_id(self, start):
        return self.board_array[start]

    def can_capture(self, start, end):
        start_id = self.board_array[start]
        end_id = self.board_array[end]

        if end_id == 0:
            return True
        # returns true if the start piece is a different sign to the end piece 
        # aka + and - means black and white 
        return (self.sign_check(start_id) != self.sign_check(end_id))

    def path_clear(self, start, end):
        # NOT TO BE USED FOR KNIGHT AS IT JUMPS OVER PIECES, so no path to check clearing for

        ########## flipped x and y in start and end, so that coordinates dispalyed are normal, 
        # NOT INDICATIVE of how the system views x and y internally
        (x1, y1) = start
        (x2, y2) = end
        dx = x2 - x1
        dy = y2 - y1
        # Allows us to trace the direction of the move 
        stepx = 1 if dx > 0 else -1 if dx < 0 else 0 
        stepy = 1 if dy > 0 else -1 if dy < 0 else 0
        
        # current starts 1 off forward as we know there is nothing blocking us in 
        # the initial standing position
        current = (x1, y1)
        print(current)
        print("Previous Position:",start[::-1], self.board_array[current])
        print("New Position:",end[::-1], self.board_array[current])
        ################################# x and y in visual is flipped
        while current != end:
            current = (
                current[0] + stepx,
                current[1] + stepy
            )
            # makes sure that the end coordinate is never decided, 
            # so that can_capture decides the capture logic
            if current == end:
                break
            if self.board_array[current] != 0:
                return False
        return True
    # checks if king is in check or not
    def king_in_check():
        pass

    def is_empty(self, end):
        return self.board_array[end] == 0
    
    def is_enemy(self, current_piece_id, end):
        target_id = self.board_array[end]
        if target_id == 0:
            return False
        return (current_piece_id > 0) != (target_id > 0)

    def is_pawn(self, end):
        piece_id = self.board_array[end]
        return (piece_id >= -8 and piece_id <= 9)

    def move_piece(self, start, end):
        self.board_array[end] = self.board_array[start]
        self.board_array[start] = 0
        self.game_view()
    # # to decide 1 or 2 step move for 1st move on pawn
    # def increment_pawn(self, start):
    #     pawn_id = self.board_array[start]


class pieces:
    def __init__(self):
        # contains all the pieces metadata for all 32 significant pieces
        self.piece = {
        1 : rook(),
        2 : knight(),
        3 : bishop(),
        4 : queen(),
        5 : king(),
        6 : bishop(),
        7 : knight(),
        8 : rook(),
        9 : pawn(),
        10 : pawn(),
        11 : pawn(),
        12 : pawn(),
        13 : pawn(),
        14 : pawn(),
        15 : pawn(),
        16 : pawn(),
        -1 : pawn(),
        -2 : pawn(),
        -3 : pawn(),
        -4 : pawn(),
        -5 : pawn(),
        -6 : pawn(),
        -7 : pawn(),
        -8 : pawn(),
        -9 : rook(),
        -10 : knight(),
        -11 : bishop(),
        -12 : queen(),
        -13 : king(),
        -14 : bishop(),
        -15 : knight(),
        -16 : rook()
        }

    def pawn_promotion(self, id, promotion):
        self.piece[id] = promotion
        print(f"promoted to {promotion}")

##############################################################################################################
# for all chess peices the move made by the player can be determined by subtracting 
# the end position and start position giving a constant change/pattern for each piece
class pawn:
    # hardest and most feature rich func, with all the things a pawn can do
    # - pawn can either move 1 step forward at start or 2 squares forward 
    # - en passant - pawn that has moved forward 2 squares can be 
    #   captured by opposing pawn (by moving straight 1 square next to pawn 
    #   which has moved 2 squares) 
    # - pawn promotion when pawn reaches end of oppsite side board - TODO
        
    def is_valid_move(self, start, end, board, board_start, board_end, en_passant_target):
        #self.board = board()
        # user presentable x,y start and end 
        (x1, y1) = start 
        (x2, y2) = end 
        print("start and end: ", start, end)
        dx = x2 - x1
        dy = y2 - y1
        piece_id = board.get_piece_id(board_start)
        target_id = board.get_piece_id(board_end)
        # pawns initially located at y = 1 and y = 6
        direction = 1 if piece_id > 0 else -1
        pawn_start_row = 1 if piece_id > 0 else 6

        # normal forward 
        if dx == 0 and dy == direction and board.is_empty(board_end):
            return True
        # double step 
        if dx == 0 and dy == 2 * direction and y1 == pawn_start_row and board.is_empty(board_end):
            return True 
        # diagonal capture only 
        if (abs(dx) == 1 and dy == direction and board.is_enemy(piece_id, board_end)):
            return True
        # en-passant capture 
        if abs(dx) == 1 and dy == direction and end == en_passant_target:
            return True 
            
class bishop:
    def is_valid_move(self, start, end, board = None, board_start = None, board_end = None, en_passant_target = None):
        (x1, y1) = start
        (x2, y2) = end 
        return(abs((x2-x1)) == abs((y2-y1)))
    #2 pieces per side/manipulate both with one class
    #pass
class knight:
    #2 pieces per side/manipulate both with one class
    ####### this piece doesn't need to have 'check_path', as knight JUMPS in L shape, 
    # skipping the pieces in between
    def is_valid_move(self, start, end, board = None, board_start = None, board_end = None, en_passant_target = None):
        (x1, y1) = start
        (x2, y2) = end 
        print("start and end: ", start, end)
        dx = x2 - x1
        dy = y2 - y1
        # the general direction that the piece moves in 
        return((abs(dx) == 2) and (abs(dy) == 1)
               or ((abs(dy) == 2) and (abs(dx) == 1)))

class rook:
    def is_valid_move(self, start, end, board = None, board_start = None, board_end = None, en_passant_target = None):
        (x1, y1) = start
        (x2, y2) = end
        dx = x2 - x1
        dy = y2 - y1
        # Allows us to trace the direction of the move 
        stepx = 1 if dx > 0 else -1 if dx < 0 else 0 
        stepy = 1 if dy > 0 else -1 if dy < 0 else 0
        return((abs(stepx) == 1 and stepy == 0) or (stepx == 0 and abs(stepy) == 1))

class king:
    #1 piece per side/manipulate both with one class
    def is_valid_move(self, start, end, board = None, board_start = None, board_end = None, en_passant_target = None):
        (x1, y1) = start
        (x2, y2) = end 
        dx = x2 - x1
        dy = y2 - y1
        return(((abs(dx) == 1 and dy == 0)) 
               or ((dx == 0 and abs(dy) == 1)) 
               or (abs(dx) == 1 and abs(dy) == 1))
class queen:
    #1 piece per side/manipulate both with one class
    # queen can make moves from both the bishop and the rook, 
    # aka (linear and diagonal)
    def is_valid_move(self, start, end, board = None, board_start = None, board_end = None, en_passant_target = None):
            (x1, y1) = start
            (x2, y2) = end
            dx = x2 - x1
            dy = y2 - y1
            # Allows us to trace the direction of the move 
            stepx = 1 if dx > 0 else -1 if dx < 0 else 0 
            stepy = 1 if dy > 0 else -1 if dy < 0 else 0
            # rook and bishop conditions combined 
            return((abs((x2-x1)) == abs((y2-y1))) 
                   or (abs(stepx) == 1 and stepy == 0) 
                   or (stepx == 0 and abs(stepy) == 1)) 

class game:
    # logic to control and manage all classses here, below all other classes and things needed \
    # dictionary to have letter/number position identity instead of coordinates
    # dictionary or such to identify what piece each number is, from 1-16 (same for -1 to -16)
    def __init__(self):
        self.board = board()
        self.pieces = pieces()
        self.en_passant_target = (None) # store target tuple or none
        #######################################################################
        # NEED LOGIC FOR WHITE AND BLACK
    def sign_check(self, piece_id):
        # sign of piece_id compared to biggefr or smaller than 0 returning true or false aka 1 or 0 
        # and then if bigger than 0, then the same piece_id is NOT smaller than 0, so 0 
        # therefore 1 - 0 = +1 or if opposite example 0 - 1 = -1, thus determining sign
        print(int(piece_id > 0), int(piece_id < 0))
        return (int(piece_id > 0) - int(piece_id < 0))

    def king_in_check(self, king_position):
        # logic for king in check 
        # check diagonal(4) and orthogonal(4) + knight jump (8)
        # knight jump check can be calculated using a dictionary of 8 positions displaced from king
        numbers = [1, 2, -1, -2]
        pairs = itertools.permutations(numbers, 2)
        filtered_pairs = [rook_pos for rook_pos in pairs if abs(rook_pos[0]) != abs(rook_pos[1])] 
        for rook_pos in filtered_pairs:
            # for board coordinates
            y, x = rook_pos
            # 8 DIRECTIONS FOR KNIGHT 
            within_x_axis = (x >= 0) and (x <= 7)
            within_y_axis = (y >= 0) and (y <= 7)
            piece_id = self.board.get_piece_id(rook_pos)
            chess_piece = self.pieces.piece[piece_id]
            # within board confines == check for knight
            if within_x_axis and within_y_axis and chess_piece == knight:
                return False
            
            # DIAGONAL CHECK FOR BISHOP,QUEEN, PAWN

            # ORTHOGONAL CHECK FOR ROOK, QUEEN, PAWN

                
                




            
        

    def force_castle(self, board_start, board_end, rook_board_start, rook_board_end):
        # function to force rook to move for castling logic TODO 
        # moves the king by 2 pieces entere by user
        self.board.move_piece(board_start, board_end)
        # moves the closest rook next to the king 
        self.board.move_piece(rook_board_start, rook_board_end)


    def castling_condition(self, start, end, board_start, board_end, kings_moved, rooks_moved, king_id):
        # king must not have moved before
        king_side = 1 if king_id > 0 else -1

        if kings_moved[king_side] != 0:
            print("Invalid Castling: King has already moved")
            return False

        # four legal castling moves in GAME coordinates
        # rook positions are given in BOARD coordinates
        castling_moves = {
            ((4, 7), (2, 7)): ((7, 0), (7, 3)),  # White queenside
            ((4, 7), (6, 7)): ((7, 7), (7, 5)),  # White kingside
            ((4, 0), (2, 0)): ((0, 0), (0, 3)),  # Black queenside
            ((4, 0), (6, 0)): ((0, 7), (0, 5))   # Black kingside
        }

        move = (start, end)

        if move not in castling_moves:
            print("Invalid Castling")
            return False

        rook_board_start, rook_board_end = castling_moves[move]

        # Check that the correct rook exists
        rook_id = self.board.get_piece_id(rook_board_start)

        if rook_id not in rooks_moved:
            print("Invalid Castling: No valid rook")
            return False

        # Make sure the piece actually is a rook
        if not isinstance(self.pieces.piece[rook_id], rook):
            print("Invalid Castling: Piece is not a rook")
            return False 

        # Rook must not have moved before
        if rooks_moved[rook_id] != 0:
            print("Invalid Castling: Rook has already moved")
            return False

        # Every square between king and rook must be empty
        if not self.board.path_clear(board_start, rook_board_start):
            print("Invalid Castling: Path is blocked")
            return False

        # If all conditions above passed, perform castling
        self.force_castle(board_start, board_end, rook_board_start, rook_board_end)
        # - returns TRUE for KING, so king_in_check can track the king pos for check 
        #   using kings end coordinates
        return True  



    def play(self):
        playing = True
        # set playing to false when game lost
        # TODO : for castling logic using kings black or white ( 1, -1) and rooks piece_id
        kings_moved = {1 : 0, -1 : 0}
        rooks_moved = {1 : 0, -9 : 0,
                       8 : 0, -16 : 0}
                        # coordinates in x,y format 
        king_position = {1 : (4,0),
                         -1 : (4, 7)}
        while playing:
            print("\n\n")
            self.board.game_view()
            # below the tuple stores everything as string
            start = tuple(map(int, input("Enter start coordinates in form (x,y): ")))
            x1, y1 = start
            end = tuple(map(int, input("Enter end coordinates in form (x,y): ")))
            x2, y2 = end 

            # on board row and column as x and y is flipped, so y in x and x in y position 
            board_start = (y1, x1)
            board_end = (y2, x2)
            board_piece_start = self.board.get_piece_id(board_start)
            board_piece_end = self.board.get_piece_id(board_end)
            # for en-passant logic dy
            dx = x2 - x1
            dy = y2 - y1

            if self.board.get_piece_id(board_start) == 0: # fixes the 0 id bug, as not in 
                print("There is no piece at this position id: {0}")
                continue # restarts the loop cleanly 
            # retrives the id for the starting/playing piece
            piece_id = self.board.get_piece_id(board_start)
            # chess_piece holds the class for the id's piece type (eg. rook, queen ect...)
            chess_piece = self.pieces.piece[piece_id]
            # is_valid_move function used to check the move conforms to its piece id 
            print("start:", start)
            print("end:", end)
            print("piece:", type(chess_piece).__name__)
            print("valid:", chess_piece.is_valid_move(start, end, self.board, board_start, board_end, self.en_passant_target))
            # - 'start' and 'end' given to chess piece class as its the correct x,y format for user 
            #   and 'boardstart' and 'boardend' given to the internal board mechanics
            if chess_piece.is_valid_move(start, end, self.board, board_start, board_end, self.en_passant_target): 
                # - self.board instead of self.board(), as the '()' represents calling 
                #   a function, in which the piece that recieves the board function 
                #   will not be able to access the function, due to it being in the 
                #   game() class, so just pass a REFRENCE instead, aka 'self.board' 
                #   which points to the board in memory stored in game class.
                if isinstance(chess_piece, pawn) and y2 in (0 , 7):
                    # CODE FOR PAWN PROMOTION AT END OF BOARD #TODO
                    # - I can use 'or' here, since a pawn cannot travel backwards, thus any pawn at 
                    #   vertical ends y == 0 or y == 7 would be eligible for a pawn promotion
                    promotion_choice = int(input("\nPAWN has reached the end. \n"\
                    "Enter the number of the desired promotion piece: \n" \
                    "1 : ROOK \n" \
                    "2 : KNIGHT \n" \
                    "3 : BISHOP \n" \
                    "4 : QUEEN \n" \
                    "Enter Int -> "))
                    promotion = {1 : rook(),
                                 2 : knight(),
                                 3 : bishop(),
                                 4 : queen()} 
                    self.pieces.pawn_promotion(piece_id, promotion[promotion_choice])


                # - Check if the moved piece was a double step pawn for en-passant count 
                #   as en-passant only occurs on the turn after the double pawn moves forward
                if isinstance(chess_piece, pawn) and abs(dy) == 2:
                    # Target square is the skipped square in user coordinates (x, y)
                    skipped_y = (y1 + y2) // 2
                    self.en_passant_target = (x1, skipped_y)
                else:
                    # Clear en passant if any other move is made
                    self.en_passant_target = None

                if isinstance(chess_piece, knight): # knight != path check as it jumps over 
                    path_is_clear = True
                else:
                    path_is_clear = self.board.path_clear(board_start, board_end)

                if isinstance(chess_piece, king):
                    # piece_id must be the king's id, then piece_id / abs(piece_id will give +1 or -1, as black or white)
                    kings_moved[piece_id / abs(piece_id)] += 1
                    # - updates current king position for king_in_check function needing king 
                    #   coordinates at all times 
                    king_position[piece_id / abs(piece_id)] = end
                    print(kings_moved)

                if isinstance(chess_piece, rook):
                    rooks_moved[piece_id] += 1
                    print(rooks_moved)
        
                if path_is_clear and self.board.can_capture(board_start, board_end):
                    self.board.move_piece(board_start, board_end)
                else:
                    print("\nInvalid Move\n")
            # if king piece move is not valid, and is castling, execute castling_condition func 
            elif isinstance(chess_piece, king) and abs(dx) == 2 and dy == 0:
                # TODO #################### - KING CASTLING LOGIC HERE
                castle_condition = self.castling_condition(start, end, board_start, board_end, kings_moved, rooks_moved, piece_id)
                if castle_condition:
                    # - if castle condition is approved, then kings end coordinates is updated 
                    #   for king_in_check. ELSE king_position is updated
                    king_position[piece_id / abs(piece_id)] = end
                
            else:
                print("\nInvalid Move\n")
            # logic for black and white player needed, aswell as capture logic 
            # logic for king in check

Game = game()
Game.play()
# code to determine if a piece is caught or not by adding the values of 
# the 2 peices at the position, awarding capture to the current player.

#move1 = game.rook((1,6), (1,1))
# move1 has the rook class alrdy, where the coordinates are instantiated
# moves(), is the subclass of the superclass rook
# straight_vertical(), is a function/method of the subclass moves()
#move1.moves().straight_vertical()
#move1.moves().straight_horizontal()

#board1 = game.board((1,8))
#board1.game_view()


## TODO
# - King in check logic - mid - NEXT IN ######################################################
# - Black vs White logic - mid
                                # - Pawn promotion at board end - mid # DONE, FULL TESTING NEEDED
                            # - King castling with rook - easy - relys on check, unable to castle in check