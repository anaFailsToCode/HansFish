"""
Storing all the information about the current state of chess game.
Determining valid moves at current state.
It will keep move log.
"""
from pprint import pprint


class GameState:
    def __init__(self, Fen):
        """
        Board is an 8x8 2d list, each element in list has 2 characters.
        The first character represents the color of the piece: 'b' or 'w'.
        The second character represents the type of the piece: 'R', 'N', 'B', 'Q', 'K' or 'p'.
        "--" represents an empty space with no piece.
        """
       
        
        #normal position
        boardFen = 'rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR'
        #morphys mate in 2
      #  boardFen = 'kbK5/pp6/1P6/8/8/8/8/R7'
        #opera mate
       # boardFen = '4kb1r/p2n1ppp/4q3/4p1B1/4P3/1Q6/PPP2PPP/2KR4'

       # boardFen = '3K4/8/8/p2k4/pp1B4/N5N1/P2Q4/8'


     #   boardFen = 'Q7/5p2/5P1p/5PPN/6Pk/4N1Rp/7P/6K1'
      #  boardFen = '8/8/8/2P3R1/5B2/2rP1p2/p1P1PP2/RnQ1K2k'
      #  boardFen = '2r1r1k1/1p3pp1/p1bb1n1p/8/2P5/1P1R1qPP/P1Q2P2/5KR'
        boardFen = Fen
       

        def fen_to_board(fen):
           board = [['--' for file in range(8)] for rank in range(8)]
           rank = 0
           file = 0
           for i in range(len(fen)):
               if fen[i].isdigit():
                   print(fen[i])
                   for z in range(int(fen[i])):
                       board[rank][file] = "--"
                       file += 1
               elif fen[i] == '/':
                   rank += 1
                   file = 0
                 #  print("next line")
                  # print(file)
               elif fen[i].lower() == "p":
                   if fen[i].isupper():
                       board[rank][file] = 'w'+fen[i].lower()
                   else: 
                       board[rank][file] = 'b'+fen[i].lower()
                   file += 1     
               else:
                   if fen[i].isupper():
                       board[rank][file] = 'w'+fen[i].upper()
                   else: 
                       board[rank][file] = 'b'+fen[i].upper()
                   file += 1                  
                
              # pprint(board)
           return board
                   
                   
               

            

        from pprint import pprint
    #    pprint( fen_to_board(boardFen) )
      #  print("hi")
        self.board = fen_to_board(boardFen)
      
 
       
        self.moveFunctions = {"p": self.getPawnMoves, "R": self.getRookMoves, "N": self.getKnightMoves,
                              "B": self.getBishopMoves, "Q": self.getQueenMoves, "K": self.getKingMoves}
        self.white_to_move = True
        self.move_log = []
        self.white_king_location = (7, 4)
        self.black_king_location = (0, 4)
        self.checkmate = False
        self.stalemate = False
        self.in_check = False
        self.pins = []
        self.checks = []
        self.enpassant_possible = ()  # coordinates for the square where en-passant capture is possible
        self.enpassant_possible_log = [self.enpassant_possible]
        self.current_castling_rights = CastleRights(True, True, True, True)
        self.castle_rights_log = [CastleRights(self.current_castling_rights.wks, self.current_castling_rights.bks,
                                               self.current_castling_rights.wqs, self.current_castling_rights.bqs)]

    def makeMove(self, move):
        """
        Takes a Move as a parameter and executes it.
        (this will not work for castling, pawn promotion and en-passant)
        """
        self.board[move.start_rank][move.start_file] = "--"

        self.board[move.end_rank][move.end_file] = move.piece_moved
        
        self.move_log.append(move)  # log the move so we can undo it later
        self.white_to_move = not self.white_to_move  # switch players
        # update king's location if moved
        if move.piece_moved == "wK":
            self.white_king_location = (move.end_rank, move.end_file)
        elif move.piece_moved == "bK":
            self.black_king_location = (move.end_rank, move.end_file)

        # pawn promotion
        if move.is_pawn_promotion:
            # if not is_AI:
            #    promoted_piece = input("Promote to Q, R, B, or N:") #take this to UI later
            #    self.board[move.end_rank][move.end_file] = move.piece_moved[0] + promoted_piece
            # else:
            self.board[move.end_rank][move.end_file] = move.piece_moved[0] + "Q"

        # enpassant move
        if move.is_enpassant_move:
            self.board[move.start_rank][move.end_file] = "--"  # capturing the pawn

        # update enpassant_possible variable
        if move.piece_moved[1] == "p" and abs(move.start_rank - move.end_rank) == 2:  # only on 2 square pawn advance
            self.enpassant_possible = ((move.start_rank + move.end_rank) // 2, move.start_file)
        else:
            self.enpassant_possible = ()

        # castle move
        if move.is_castle_move:
            if move.end_file - move.start_file == 2:  # king-side castle move
                self.board[move.end_rank][move.end_file - 1] = self.board[move.end_rank][
                    move.end_file + 1]  # moves the rook to its new square
                self.board[move.end_rank][move.end_file + 1] = '--'  # erase old rook
            else:  # queen-side castle move
                self.board[move.end_rank][move.end_file + 1] = self.board[move.end_rank][
                    move.end_file - 2]  # moves the rook to its new square
                self.board[move.end_rank][move.end_file - 2] = '--'  # erase old rook

        self.enpassant_possible_log.append(self.enpassant_possible)

        # update castling rights - whenever it is a rook or king move
        self.updateCastleRights(move)
        self.castle_rights_log.append(CastleRights(self.current_castling_rights.wks, self.current_castling_rights.bks,
                                                   self.current_castling_rights.wqs, self.current_castling_rights.bqs))

    def undoMove(self):
        """
        Undo the last move
        """
        if len(self.move_log) != 0:  # make sure that there is a move to undo
            move = self.move_log.pop()
            self.board[move.start_rank][move.start_file] = move.piece_moved
            self.board[move.end_rank][move.end_file] = move.piece_captured
            self.white_to_move = not self.white_to_move  # swap players
            # update the king's position if needed
            if move.piece_moved == "wK":
                self.white_king_location = (move.start_rank, move.start_file)
            elif move.piece_moved == "bK":
                self.black_king_location = (move.start_rank, move.start_file)
            # undo en passant move
            if move.is_enpassant_move:
                self.board[move.end_rank][move.end_file] = "--"  # leave landing square blank
                self.board[move.start_rank][move.end_file] = move.piece_captured

            self.enpassant_possible_log.pop()
            self.enpassant_possible = self.enpassant_possible_log[-1]

            # undo castle rights
            self.castle_rights_log.pop()  # get rid of the new castle rights from the move we are undoing
            self.current_castling_rights = self.castle_rights_log[
                -1]  # set the current castle rights to the last one in the list
            # undo the castle move
            if move.is_castle_move:
                if move.end_file - move.start_file == 2:  # king-side
                    self.board[move.end_rank][move.end_file + 1] = self.board[move.end_rank][move.end_file - 1]
                    self.board[move.end_rank][move.end_file - 1] = '--'
                else:  # queen-side
                    self.board[move.end_rank][move.end_file - 2] = self.board[move.end_rank][move.end_file + 1]
                    self.board[move.end_rank][move.end_file + 1] = '--'
            self.checkmate = False
            self.stalemate = False

    def updateCastleRights(self, move):
        """
        Update the castle rights given the move
        """
        if move.piece_captured == "wR":
            if move.end_file == 0:  # left rook
                self.current_castling_rights.wqs = False
            elif move.end_file == 7:  # right rook
                self.current_castling_rights.wks = False
        elif move.piece_captured == "bR":
            if move.end_file == 0:  # left rook
                self.current_castling_rights.bqs = False
            elif move.end_file == 7:  # right rook
                self.current_castling_rights.bks = False

        if move.piece_moved == 'wK':
            self.current_castling_rights.wqs = False
            self.current_castling_rights.wks = False
        elif move.piece_moved == 'bK':
            self.current_castling_rights.bqs = False
            self.current_castling_rights.bks = False
        elif move.piece_moved == 'wR':
            if move.start_rank == 7:
                if move.start_file == 0:  # left rook
                    self.current_castling_rights.wqs = False
                elif move.start_file == 7:  # right rook
                    self.current_castling_rights.wks = False
        elif move.piece_moved == 'bR':
            if move.start_rank == 0:
                if move.start_file == 0:  # left rook
                    self.current_castling_rights.bqs = False
                elif move.start_file == 7:  # right rook
                    self.current_castling_rights.bks = False

    
    def getValidMoves(self):
        """
        All moves considering checks.
        """
        temp_castle_rights = CastleRights(self.current_castling_rights.wks, self.current_castling_rights.bks,
                                          self.current_castling_rights.wqs, self.current_castling_rights.bqs)
        # advanced algorithm
        moves = []
        self.in_check, self.pins, self.checks = self.checkForPinsAndChecks()

        if self.white_to_move:
            king_rank = self.white_king_location[0]
            king_file = self.white_king_location[1]
        else:
            king_rank = self.black_king_location[0]
            king_file = self.black_king_location[1]
        if self.in_check:
            if len(self.checks) == 1:  # only 1 check, block the check or move the king
                moves = self.getAllPossibleMoves()
                # to block the check you must put a piece into one of the squares between the enemy piece and your king
                check = self.checks[0]  # check information
                check_rank = check[0]
                check_file = check[1]
                piece_checking = self.board[check_rank][check_file]
                valid_squares = []  # squares that pieces can move to
                # if knight, must capture the knight or move your king, other pieces can be blocked
                if piece_checking[1] == "N":
                    valid_squares = [(check_rank, check_file)]
                else:
                    for i in range(1, 8):
                        valid_square = (king_rank + check[2] * i,
                                        king_file + check[3] * i)  # check[2] and check[3] are the check directions
                        valid_squares.append(valid_square)
                        if valid_square[0] == check_rank and valid_square[
                            1] == check_file:  # once you get to piece and check
                            break
                # get rid of any moves that don't block check or move king
                for i in range(len(moves) - 1, -1, -1):  # iterate through the list backwards when removing elements
                    if moves[i].piece_moved[1] != "K":  # move doesn't move king so it must block or capture
                        if not (moves[i].end_rank,
                                moves[i].end_file) in valid_squares:  # move doesn't block or capture piece
                            moves.remove(moves[i])
            else:  # double check, king has to move
                self.getKingMoves(king_rank, king_file, moves)
        else:  # not in check - all moves are fine
            moves = self.getAllPossibleMoves()
            if self.white_to_move:
                self.getCastleMoves(self.white_king_location[0], self.white_king_location[1], moves)
            else:
                self.getCastleMoves(self.black_king_location[0], self.black_king_location[1], moves)

        if len(moves) == 0:
            if self.inCheck():
                self.checkmate = True
            else:
                # TODO stalemate on repeated moves
                self.stalemate = True
        else:
            self.checkmate = False
            self.stalemate = False

        self.current_castling_rights = temp_castle_rights
        return moves

    def inCheck(self):
        """
        Determine if a current player is in check
        """
        if self.white_to_move:
            return self.squareUnderAttack(self.white_king_location[0], self.white_king_location[1])
        else:
            return self.squareUnderAttack(self.black_king_location[0], self.black_king_location[1])

    def squareUnderAttack(self, rank, file):
        """
        Determine if enemy can attack the square rank file
        """
        self.white_to_move = not self.white_to_move  # switch to opponent's point of view
        opponents_moves = self.getAllPossibleMoves()
        self.white_to_move = not self.white_to_move
        for move in opponents_moves:
            if move.end_rank == rank and move.end_file == file:  # square is under attack
                return True
        return False

    def getAllPossibleMoves(self):
        """
        All moves without considering checks.
        """
        moves = []
        for rank in range(len(self.board)):
            for file in range(len(self.board[rank])):
                turn = self.board[rank][file][0]
                if (turn == "w" and self.white_to_move) or (turn == "b" and not self.white_to_move):
                    piece = self.board[rank][file][1]
                    self.moveFunctions[piece](rank, file, moves)  # calls appropriate move function based on piece type
        return moves

    def checkForPinsAndChecks(self):
        pins = []  # squares pinned and the direction its pinned from
        checks = []  # squares where enemy is applying a check
        in_check = False
        if self.white_to_move:
            enemy_color = "b"
            ally_color = "w"
            start_rank = self.white_king_location[0]
            start_file = self.white_king_location[1]
        else:
            enemy_color = "w"
            ally_color = "b"
            start_rank = self.black_king_location[0]
            start_file = self.black_king_location[1]
        # check outwards from king for pins and checks, keep track of pins
        directions = ((-1, 0), (0, -1), (1, 0), (0, 1), (-1, -1), (-1, 1), (1, -1), (1, 1))
        for j in range(len(directions)):
            direction = directions[j]
            possible_pin = ()  # reset possible pins
            for i in range(1, 8):
                end_rank = start_rank + direction[0] * i
                end_file = start_file + direction[1] * i
                if 0 <= end_rank <= 7 and 0 <= end_file <= 7:
                    end_piece = self.board[end_rank][end_file]
                    if end_piece[0] == ally_color and end_piece[1] != "K":
                        if possible_pin == ():  # first allied piece could be pinned
                            possible_pin = (end_rank, end_file, direction[0], direction[1])
                        else:  # 2nd allied piece - no check or pin from this direction
                            break
                    elif end_piece[0] == enemy_color:
                        enemy_type = end_piece[1]
                        # 5 possibilities in this complex conditional
                        # 1.) orthogonally away from king and piece is a rook
                        # 2.) diagonally away from king and piece is a bishop
                        # 3.) 1 square away diagonally from king and piece is a pawn
                        # 4.) any direction and piece is a queen
                        # 5.) any direction 1 square away and piece is a king
                        if (0 <= j <= 3 and enemy_type == "R") or (4 <= j <= 7 and enemy_type == "B") or (
                                i == 1 and enemy_type == "p" and (
                                (enemy_color == "w" and 6 <= j <= 7) or (enemy_color == "b" and 4 <= j <= 5))) or (
                                enemy_type == "Q") or (i == 1 and enemy_type == "K"):
                            if possible_pin == ():  # no piece blocking, so check
                                in_check = True
                                checks.append((end_rank, end_file, direction[0], direction[1]))
                                break
                            else:  # piece blocking so pin
                                pins.append(possible_pin)
                                break
                        else:  # enemy piece not applying checks
                            break
                else:
                    break  # off board
        # check for knight checks
        knight_moves = ((-2, -1), (-2, 1), (-1, 2), (1, 2), (2, -1), (2, 1), (-1, -2), (1, -2))
        for move in knight_moves:
            end_rank = start_rank + move[0]
            end_file = start_file + move[1]
            if 0 <= end_rank <= 7 and 0 <= end_file <= 7:
                end_piece = self.board[end_rank][end_file]
                if end_piece[0] == enemy_color and end_piece[1] == "N":  # enemy knight attacking a king
                    in_check = True
                    checks.append((end_rank, end_file, move[0], move[1]))
        return in_check, pins, checks

    def getPawnMoves(self, rank, file, moves):
        """
        Get all the pawn moves for the pawn located at rank, file and add the moves to the list.
        """
        piece_pinned = False
        pin_direction = ()
        for i in range(len(self.pins) - 1, -1, -1):
            if self.pins[i][0] == rank and self.pins[i][1] == file:
                piece_pinned = True
                pin_direction = (self.pins[i][2], self.pins[i][3])
                self.pins.remove(self.pins[i])
                break

        if self.white_to_move:
            move_amount = -1
            start_rank = 6
            enemy_color = "b"
            king_rank, king_file = self.white_king_location
        else:
            move_amount = 1
            start_rank = 1
            enemy_color = "w"
            king_rank, king_file = self.black_king_location

        if self.board[rank + move_amount][file] == "--":  # 1 square pawn advance
            if not piece_pinned or pin_direction == (move_amount, 0):
                moves.append(Move((rank, file), (rank + move_amount, file), self.board))
                if rank == start_rank and self.board[rank + 2 * move_amount][file] == "--":  # 2 square pawn advance
                    moves.append(Move((rank, file), (rank + 2 * move_amount, file), self.board))
        if file - 1 >= 0:  # capture to the left
            if not piece_pinned or pin_direction == (move_amount, -1):
                if self.board[rank + move_amount][file - 1][0] == enemy_color:
                    moves.append(Move((rank, file), (rank + move_amount, file - 1), self.board))
                if (rank + move_amount, file - 1) == self.enpassant_possible:
                    attacking_piece = blocking_piece = False
                    if king_rank == rank:
                        if king_file < file:  # king is left of the pawn
                            # inside: between king and the pawn;
                            # outside: between pawn and border;
                            inside_range = range(king_file + 1, file - 1)
                            outside_range = range(file + 1, 8)
                        else:  # king right of the pawn
                            inside_range = range(king_file - 1, file, -1)
                            outside_range = range(file - 2, -1, -1)
                        for i in inside_range:
                            if self.board[rank][i] != "--":  # some piece beside en-passant pawn blocks
                                blocking_piece = True
                        for i in outside_range:
                            square = self.board[rank][i]
                            if square[0] == enemy_color and (square[1] == "R" or square[1] == "Q"):
                                attacking_piece = True
                            elif square != "--":
                                blocking_piece = True
                    if not attacking_piece or blocking_piece:
                        moves.append(Move((rank, file), (rank + move_amount, file - 1), self.board, is_enpassant_move=True))
        if file + 1 <= 7:  # capture to the right
            if not piece_pinned or pin_direction == (move_amount, +1):
                if self.board[rank + move_amount][file + 1][0] == enemy_color:
                    moves.append(Move((rank, file), (rank + move_amount, file + 1), self.board))
                if (rank + move_amount, file + 1) == self.enpassant_possible:
                    attacking_piece = blocking_piece = False
                    if king_rank == rank:
                        if king_file < file:  # king is left of the pawn
                            # inside: between king and the pawn;
                            # outside: between pawn and border;
                            inside_range = range(king_file + 1, file)
                            outside_range = range(file + 2, 8)
                        else:  # king right of the pawn
                            inside_range = range(king_file - 1, file + 1, -1)
                            outside_range = range(file - 1, -1, -1)
                        for i in inside_range:
                            if self.board[rank][i] != "--":  # some piece beside en-passant pawn blocks
                                blocking_piece = True
                        for i in outside_range:
                            square = self.board[rank][i]
                            if square[0] == enemy_color and (square[1] == "R" or square[1] == "Q"):
                                attacking_piece = True
                            elif square != "--":
                                blocking_piece = True
                    if not attacking_piece or blocking_piece:
                        moves.append(Move((rank, file), (rank + move_amount, file + 1), self.board, is_enpassant_move=True))

    def getRookMoves(self, rank, file, moves):
        """
        Get all the rook moves for the rook located at rank, file and add the moves to the list.
        """
        piece_pinned = False
        pin_direction = ()
        for i in range(len(self.pins) - 1, -1, -1):
            if self.pins[i][0] == rank and self.pins[i][1] == file:
                piece_pinned = True
                pin_direction = (self.pins[i][2], self.pins[i][3])
                if self.board[rank][file][
                    1] != "Q":  # can't remove queen from pin on rook moves, only remove it on bishop moves
                    self.pins.remove(self.pins[i])
                break

        directions = ((-1, 0), (0, -1), (1, 0), (0, 1))  # up, left, down, right
        enemy_color = "b" if self.white_to_move else "w"
        for direction in directions:
            for i in range(1, 8):
                end_rank = rank + direction[0] * i
                end_file = file + direction[1] * i
                if 0 <= end_rank <= 7 and 0 <= end_file <= 7:  # check for possible moves only in boundaries of the board
                    if not piece_pinned or pin_direction == direction or pin_direction == (
                            -direction[0], -direction[1]):
                        end_piece = self.board[end_rank][end_file]
                        if end_piece == "--":  # empty space is valid
                            moves.append(Move((rank, file), (end_rank, end_file), self.board))
                        elif end_piece[0] == enemy_color:  # capture enemy piece
                            moves.append(Move((rank, file), (end_rank, end_file), self.board))
                            break
                        else:  # friendly piece
                            break
                else:  # off board
                    break

    def getKnightMoves(self, rank, file, moves):
        """
        Get all the knight moves for the knight located at rank file and add the moves to the list.
        """
        piece_pinned = False
        for i in range(len(self.pins) - 1, -1, -1):
            if self.pins[i][0] == rank and self.pins[i][1] == file:
                piece_pinned = True
                self.pins.remove(self.pins[i])
                break

        knight_moves = ((-2, -1), (-2, 1), (-1, 2), (1, 2), (2, -1), (2, 1), (-1, -2),
                        (1, -2))  # up/left up/right right/up right/down down/left down/right left/up left/down
        ally_color = "w" if self.white_to_move else "b"
        for move in knight_moves:
            end_rank = rank + move[0]
            end_file = file + move[1]
            if 0 <= end_rank <= 7 and 0 <= end_file <= 7:
                if not piece_pinned:
                    end_piece = self.board[end_rank][end_file]
                    if end_piece[0] != ally_color:  # so its either enemy piece or empty square
                        moves.append(Move((rank, file), (end_rank, end_file), self.board))

    def getBishopMoves(self, rank, file, moves):
        """
        Get all the bishop moves for the bishop located at rank file and add the moves to the list.
        """
        piece_pinned = False
        pin_direction = ()
        for i in range(len(self.pins) - 1, -1, -1):
            if self.pins[i][0] == rank and self.pins[i][1] == file:
                piece_pinned = True
                pin_direction = (self.pins[i][2], self.pins[i][3])
                self.pins.remove(self.pins[i])
                break

        directions = ((-1, -1), (-1, 1), (1, 1), (1, -1))  # diagonals: up/left up/right down/right down/left
        enemy_color = "b" if self.white_to_move else "w"
        for direction in directions:
            for i in range(1, 8):
                end_rank = rank + direction[0] * i
                end_file = file + direction[1] * i
                if 0 <= end_rank <= 7 and 0 <= end_file <= 7:  # check if the move is on board
                    if not piece_pinned or pin_direction == direction or pin_direction == (
                            -direction[0], -direction[1]):
                        end_piece = self.board[end_rank][end_file]
                        if end_piece == "--":  # empty space is valid
                            moves.append(Move((rank, file), (end_rank, end_file), self.board))
                        elif end_piece[0] == enemy_color:  # capture enemy piece
                            moves.append(Move((rank, file), (end_rank, end_file), self.board))
                            break
                        else:  # friendly piece
                            break
                else:  # off board
                    break

    def getQueenMoves(self, rank, file, moves):
        """
        Get all the queen moves for the queen located at rank file and add the moves to the list.
        """
        self.getBishopMoves(rank, file, moves)
        self.getRookMoves(rank, file, moves)

    def getKingMoves(self, rank, file, moves):
        """
        Get all the king moves for the king located at rank file and add the moves to the list.
        """
        rank_moves = (-1, -1, -1, 0, 0, 1, 1, 1)
        file_moves = (-1, 0, 1, -1, 1, -1, 0, 1)
        ally_color = "w" if self.white_to_move else "b"
        for i in range(8):
            end_rank = rank + rank_moves[i]
            end_file = file + file_moves[i]
            if 0 <= end_rank <= 7 and 0 <= end_file <= 7:
                end_piece = self.board[end_rank][end_file]
                if end_piece[0] != ally_color:  # not an ally piece - empty or enemy
                    # place king on end square and check for checks
                    if ally_color == "w":
                        self.white_king_location = (end_rank, end_file)
                    else:
                        self.black_king_location = (end_rank, end_file)
                    in_check, pins, checks = self.checkForPinsAndChecks()
                    if not in_check:
                        moves.append(Move((rank, file), (end_rank, end_file), self.board))
                    # place king back on original location
                    if ally_color == "w":
                        self.white_king_location = (rank, file)
                    else:
                        self.black_king_location = (rank, file)

    def getCastleMoves(self, rank, file, moves):
        """
        Generate all valid castle moves for the king at (rank, file) and add them to the list of moves.
        """
        if self.squareUnderAttack(rank, file):
            return  # can't castle while in check
        if (self.white_to_move and self.current_castling_rights.wks) or (
                not self.white_to_move and self.current_castling_rights.bks):
            self.getKingsideCastleMoves(rank, file, moves)
        if (self.white_to_move and self.current_castling_rights.wqs) or (
                not self.white_to_move and self.current_castling_rights.bqs):
            self.getQueensideCastleMoves(rank, file, moves)

    def getKingsideCastleMoves(self, rank, file, moves):
        if file+1< 7:
            if self.board[rank][file + 1] == '--' and self.board[rank][file + 2] == '--':
                if not self.squareUnderAttack(rank, file + 1) and not self.squareUnderAttack(rank, file + 2):
                    moves.append(Move((rank, file), (rank, file + 2), self.board, is_castle_move=True))

    def getQueensideCastleMoves(self, rank, file, moves):
        if self.board[rank][file - 1] == '--' and self.board[rank][file - 2] == '--' and self.board[rank][file - 3] == '--':
            if not self.squareUnderAttack(rank, file - 1) and not self.squareUnderAttack(rank, file - 2):
                moves.append(Move((rank, file), (rank, file - 2), self.board, is_castle_move=True))


class CastleRights:
    def __init__(self, wks, bks, wqs, bqs):
        self.wks = wks
        self.bks = bks
        self.wqs = wqs
        self.bqs = bqs


class Move:
    # in chess, fields on the board are described by two symbols, one of them being number between 1-8 (which is corresponding to ranks)
    # and the second one being a letter between a-f (corresponding to fileumns), in order to use this notation we need to map our [rank][file] coordinates
    # to match the ones used in the original chess game
    ranks_to_ranks = {"1": 7, "2": 6, "3": 5, "4": 4,
                     "5": 3, "6": 2, "7": 1, "8": 0}
    ranks_to_ranks = {v: k for k, v in ranks_to_ranks.items()}
    files_to_files = {"a": 0, "b": 1, "c": 2, "d": 3,
                     "e": 4, "f": 5, "g": 6, "h": 7}
    files_to_files = {v: k for k, v in files_to_files.items()}

    def __init__(self, start_square, end_square, board, is_enpassant_move=False, is_castle_move=False):
        self.start_rank = start_square[0]
        self.start_file = start_square[1]
        self.end_rank = end_square[0]
        self.end_file = end_square[1]
        self.piece_moved = board[self.start_rank][self.start_file]
        self.piece_captured = board[self.end_rank][self.end_file]
        # pawn promotion
        self.is_pawn_promotion = (self.piece_moved == "wp" and self.end_rank == 0) or (
                self.piece_moved == "bp" and self.end_rank == 7)
        # en passant
        self.is_enpassant_move = is_enpassant_move
        if self.is_enpassant_move:
            self.piece_captured = "wp" if self.piece_moved == "bp" else "bp"
        # castle move
        self.is_castle_move = is_castle_move

        self.is_capture = self.piece_captured != "--"
        self.moveID = self.start_rank * 1000 + self.start_file * 100 + self.end_rank * 10 + self.end_file

    def __eq__(self, other):
        """
        Overriding the equals method.
        """
        if isinstance(other, Move):
            return self.moveID == other.moveID
        return False

    def getChessNotation(self):
        if self.is_pawn_promotion:
            return self.getRankFile(self.end_rank, self.end_file) + "Q"
        if self.is_castle_move:
            if self.end_file == 1:
                return "0-0-0"
            else:
                return "0-0"
        if self.is_enpassant_move:
            return self.getRankFile(self.start_rank, self.start_file)[0] + "x" + self.getRankFile(self.end_rank,
                                                                                                self.end_file) + " e.p."
        if self.piece_captured != "--":
            if self.piece_moved[1] == "p":
                return self.getRankFile(self.start_rank, self.start_file)[0] + "x" + self.getRankFile(self.end_rank,
                                                                                                    self.end_file)
            else:
                return self.piece_moved[1] + "x" + self.getRankFile(self.end_rank, self.end_file)
        else:
            if self.piece_moved[1] == "p":
                return self.getRankFile(self.end_rank, self.end_file)
            else:
                return self.piece_moved[1] + self.getRankFile(self.end_rank, self.end_file)

        # TODO Disambiguating moves

    def getRankFile(self, rank, file):
        return self.files_to_files[file] + self.ranks_to_ranks[rank]

    def __str__(self):
        if self.is_castle_move:
            return "0-0" if self.end_file == 6 else "0-0-0"

        end_square = self.getRankFile(self.end_rank, self.end_file)

        if self.piece_moved[1] == "p":
            if self.is_capture:
                return self.files_to_files[self.start_file] + "x" + end_square
            else:
                return end_square + "Q" if self.is_pawn_promotion else end_square

        move_string = self.piece_moved[1]
        if self.is_capture:
            move_string += "x"
        return move_string + end_square
