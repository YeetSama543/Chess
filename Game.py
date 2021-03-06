#contains functionality of the game

from typing import Set
from Board import Board
from Piece import *
from Game_Constants import *

turn = 0

def get_clicked_square(mouse_pos: tuple, pos: tuple) -> list:
    relative_x = mouse_pos[0] - pos[0]
    relative_y = mouse_pos[1] - pos[1]
    return [relative_y // SQUARE_SIZE, relative_x // SQUARE_SIZE] #x and y get flipped since first val represents the row# and second is col#

def clicked_on_board(mouse_pos: tuple, pos: tuple) -> bool:
    min_x = pos[0]
    max_x = pos[0] + BOARD_SIZE
    min_y = pos[1]
    max_y = pos[1] + BOARD_SIZE

    if mouse_pos[0] > min_x and mouse_pos[0] < max_x:
        if mouse_pos[1] > min_y and mouse_pos[1] < max_y:
            return True
    return False

def is_valid_square(square: list) -> bool:
    if square[0] > 7 or square[0] < 0 or square[1] > 7 or square[1] < 0:
        return False
    return True

def suppose_move(piece: Piece, new_square: list, position: list):
    new_position = [[position[j][i] for i in range(8)] for j in range(8)]
    new_position[new_square[0]][new_square[1]] = piece
    new_position[piece.square[0]][piece.square[1]] = None

    return new_position

#these move generating helper functions DO NOT account for check
def __generate_attacked_squares_pawn(pawn: Piece, position: list, moves: list):
    attacked_squares = []
    #determine if the pawn has previously moved
    has_moved = True
    if pawn.get_color() == Color.WHITE and pawn.square[0] == 6:
        has_moved = False
    elif pawn.get_color() == Color.BLACK and pawn.square[0] == 1:
        has_moved = False

    #use color to determine candidate squares to add
    if pawn.get_color() == Color.WHITE:
        square_in_front = [pawn.square[0] - 1, pawn.square[1]]
        square_two_ahead = [pawn.square[0] - 2, pawn.square[1]]
        diag_left = [pawn.square[0] - 1, pawn.square[1] - 1]
        diag_right = [pawn.square[0] - 1, pawn.square[1] + 1]
    else: #pawn is black
        square_in_front = [pawn.square[0] + 1, pawn.square[1]]
        square_two_ahead = [pawn.square[0] + 2, pawn.square[1]]
        diag_left = [pawn.square[0] + 1, pawn.square[1] - 1]
        diag_right = [pawn.square[0] + 1, pawn.square[1] + 1]

    #check if pawn can move forward
    if is_valid_square(square_in_front) and not position[square_in_front[0]][square_in_front[1]]:
        attacked_squares.append(square_in_front)
        #now check if pawn can move forward twice
        if not has_moved and is_valid_square(square_two_ahead) and not position[square_two_ahead[0]][square_two_ahead[1]]:
            attacked_squares.append(square_two_ahead)
    #check if pawn can move diagonally
    if is_valid_square(diag_left) and position[diag_left[0]][diag_left[1]]:
        if position[diag_left[0]][diag_left[1]].get_color() != pawn.get_color():
            attacked_squares.append(diag_left)
    if is_valid_square(diag_right) and position[diag_right[0]][diag_right[1]]:
        if position[diag_right[0]][diag_right[1]].get_color() != pawn.get_color():
            attacked_squares.append(diag_right)

    #handle ep
    ep_square = ep(position, moves)
    if ep_square:
        if ep_square in [diag_left, diag_right]:
            attacked_squares.append(ep_square)

    return attacked_squares

def __generate_attacked_squares_knight(knight: Piece, position: list):
    attacked_squares = []
    for i in [-2,2]:
        for j in [-1,1]:
            potential_square_vertical = [knight.square[0] + i, knight.square[1] + j]
            potential_square_horizontal = [knight.square[0] + j, knight.square[1] + i]

            if is_valid_square(potential_square_vertical):
                if not position[potential_square_vertical[0]][potential_square_vertical[1]]: #no piece on square
                    attacked_squares.append(potential_square_vertical)
                elif position[potential_square_vertical[0]][potential_square_vertical[1]].get_color() != knight.get_color():
                    attacked_squares.append(potential_square_vertical)
            
            if is_valid_square(potential_square_horizontal):
                if not position[potential_square_horizontal[0]][potential_square_horizontal[1]]: #no piece on square
                    attacked_squares.append(potential_square_horizontal)
                elif position[potential_square_horizontal[0]][potential_square_horizontal[1]].get_color() != knight.get_color():
                    attacked_squares.append(potential_square_horizontal)
    return attacked_squares
    
def __generate_attacked_squares_rook(rook: Piece, position: list):
    attacked_squares = []
    #up
    valid = True
    row = rook.square[0]
    col = rook.square[1]
    while valid:
        row -= 1
        potential_square = [row, col]
        if is_valid_square(potential_square):
            if not position[potential_square[0]][potential_square[1]]:
                attacked_squares.append(potential_square)
            elif position[potential_square[0]][potential_square[1]].get_color() != rook.get_color():
                attacked_squares.append(potential_square)
                valid = False #square was valid, but next one will not be
            elif position[potential_square[0]][potential_square[1]].get_color() == rook.get_color():
                valid = False
        else:
            valid = False
    #down
    valid = True
    row = rook.square[0]
    col = rook.square[1]
    while valid:
        row += 1
        potential_square = [row, col]
        if is_valid_square(potential_square):
            if not position[potential_square[0]][potential_square[1]]:
                attacked_squares.append(potential_square)
            elif position[potential_square[0]][potential_square[1]].get_color() != rook.get_color():
                attacked_squares.append(potential_square)
                valid = False #square was valid, but next one will not be
            elif position[potential_square[0]][potential_square[1]].get_color() == rook.get_color():
                valid = False
        else:
            valid = False
    #right
    valid = True
    row = rook.square[0]
    col = rook.square[1]
    while valid:
        col += 1
        potential_square = [row, col]
        if is_valid_square(potential_square):
            if not position[potential_square[0]][potential_square[1]]:
                attacked_squares.append(potential_square)
            elif position[potential_square[0]][potential_square[1]].get_color() != rook.get_color():
                attacked_squares.append(potential_square)
                valid = False #square was valid, but next one will not be
            elif position[potential_square[0]][potential_square[1]].get_color() == rook.get_color():
                valid = False
        else:
            valid = False
    #left
    valid = True
    row = rook.square[0]
    col = rook.square[1]
    while valid:
        col -= 1
        potential_square = [row, col]
        if is_valid_square(potential_square):
            if not position[potential_square[0]][potential_square[1]]:
                attacked_squares.append(potential_square)
            elif position[potential_square[0]][potential_square[1]].get_color() != rook.get_color():
                attacked_squares.append(potential_square)
                valid = False #square was valid, but next one will not be
            elif position[potential_square[0]][potential_square[1]].get_color() == rook.get_color():
                valid = False
        else:
            valid = False

    return attacked_squares

def __generate_attacked_squares_bishop(bishop: Piece, position: list):
    attacked_squares = []

    #down-right
    valid = True
    row = bishop.square[0]
    col = bishop.square[1]
    while valid:
        row += 1
        col += 1
        potential_square = [row, col]
        if is_valid_square(potential_square):
            if not position[potential_square[0]][potential_square[1]]:
                attacked_squares.append(potential_square)
            elif position[potential_square[0]][potential_square[1]].get_color() != bishop.get_color():
                attacked_squares.append(potential_square)
                valid = False #square was valid, but next one will not be
            elif position[potential_square[0]][potential_square[1]].get_color() == bishop.get_color():
                valid = False
        else:
            valid = False
    #down-left
    valid = True
    row = bishop.square[0]
    col = bishop.square[1]
    while valid:
        row += 1
        col -= 1
        potential_square = [row, col]
        if is_valid_square(potential_square):
            if not position[potential_square[0]][potential_square[1]]:
                attacked_squares.append(potential_square)
            elif position[potential_square[0]][potential_square[1]].get_color() != bishop.get_color():
                attacked_squares.append(potential_square)
                valid = False #square was valid, but next one will not be
            elif position[potential_square[0]][potential_square[1]].get_color() == bishop.get_color():
                valid = False
        else:
            valid = False
    #up-right
    valid = True
    row = bishop.square[0]
    col = bishop.square[1]
    while valid:
        row -= 1
        col += 1
        potential_square = [row, col]
        if is_valid_square(potential_square):
            if not position[potential_square[0]][potential_square[1]]:
                attacked_squares.append(potential_square)
            elif position[potential_square[0]][potential_square[1]].get_color() != bishop.get_color():
                attacked_squares.append(potential_square)
                valid = False #square was valid, but next one will not be
            elif position[potential_square[0]][potential_square[1]].get_color() == bishop.get_color():
                valid = False
        else:
            valid = False
    #up-left
    valid = True
    row = bishop.square[0]
    col = bishop.square[1]
    while valid:
        row -= 1
        col -= 1
        potential_square = [row, col]
        if is_valid_square(potential_square):
            if not position[potential_square[0]][potential_square[1]]:
                attacked_squares.append(potential_square)
            elif position[potential_square[0]][potential_square[1]].get_color() != bishop.get_color():
                attacked_squares.append(potential_square)
                valid = False #square was valid, but next one will not be
            elif position[potential_square[0]][potential_square[1]].get_color() == bishop.get_color():
                valid = False
        else:
            valid = False

    return attacked_squares

def __generate_attacked_squares_queen(queen: Piece, position: list):
    #queen is combination of rook and bishop
    #so generate moves for rook and bishop and return both together

    rook_squares = __generate_attacked_squares_rook(queen, position)
    bishop_squares = __generate_attacked_squares_bishop(queen, position)
    attacked_squares = rook_squares + bishop_squares

    return attacked_squares

def __generate_attacked_squares_king(king: Piece, position: list):
    attacked_squares = []
    #we include the original square of the king as part of the squares we check in the
    #following for loop, but since the king's color is equal to itself, the square won't be added

    for i in [-1, 0, 1]:
        for j in [-1, 0, 1]:
            potential_square = [king.square[0] + i, king.square[1] + j]
            if is_valid_square(potential_square):
                if not position[potential_square[0]][potential_square[1]]: #no piece on square
                    attacked_squares.append(potential_square)
                elif position[potential_square[0]][potential_square[1]].get_color() != king.get_color():
                    attacked_squares.append(potential_square)

    return attacked_squares

def generate_attacked_squares(piece: Piece, position: list, moves: list):
    attacked_squares = []
    if piece.type == Type.BLACK_PAWN or piece.type == Type.WHITE_PAWN:
        attacked_squares = __generate_attacked_squares_pawn(piece, position, moves)
    elif piece.type == Type.BLACK_ROOK or piece.type == Type.WHITE_ROOK:
        attacked_squares = __generate_attacked_squares_rook(piece, position)
    elif piece.type == Type.BLACK_KNIGHT or piece.type == Type.WHITE_KNIGHT:
        attacked_squares = __generate_attacked_squares_knight(piece, position)
    elif piece.type == Type.BLACK_BISHOP or piece.type == Type.WHITE_BISHOP:
        attacked_squares = __generate_attacked_squares_bishop(piece, position)
    elif piece.type == Type.BLACK_QUEEN or piece.type == Type.WHITE_QUEEN:
        attacked_squares = __generate_attacked_squares_queen(piece, position)
    elif piece.type == Type.BLACK_KING or piece.type == Type.WHITE_KING:
        attacked_squares = __generate_attacked_squares_king(piece, position)

    return attacked_squares

def is_check(position: list, moves: list) -> bool: #returns true when you make a move and your king remains in check
    global turn
    danger_squares = []
    king_square = []

    for i in range(8):
        for j in range(8):
            piece_on_square = position[i][j]
            if piece_on_square: #there is a piece on square
                if piece_on_square.get_color().value != turn: #color of piece is diff from person making a move
                    danger_squares += generate_attacked_squares(piece_on_square, position, moves)
                elif turn == 0 and piece_on_square.type == Type.WHITE_KING:
                    king_square = [i, j]
                elif turn == 1 and piece_on_square.type == Type.BLACK_KING:
                    king_square = [i, j]
    return king_square in danger_squares
                
def is_win(position: list, moves: list) -> Color:
    winner = None
    global turn

    if get_all_valid_moves(position, moves) == []:
        if is_check(position, moves):
            if turn == 0:
                winner = Color.BLACK
            else:
                winner = Color.WHITE

    return winner

def change_turn(board: Board): #changes turn. Also resets clicked piece
    global turn
    turn += 1
    turn %= 2
    board.clicked_piece = None

def pawn_promotion(position: list) -> bool: #returns promotion square if a pawn can promote, None otherwise
    for i in range(8):
        p1 = position[0][i]
        p2 = position[7][i]

        if p1:
            if p1.type == Type.WHITE_PAWN:
                return p1.square
        if p2:
            if p2.type == Type.BLACK_PAWN:
                return p2.square
    return None

def get_pawn_promotion_choice() -> Type:
    valid_choice = False
    while not valid_choice:
        for event in pg.event.get():
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_q:
                    if turn == 0: #white
                        choice = Type.WHITE_QUEEN
                    else: #black
                        choice = Type.BLACK_QUEEN
                    
                    valid_choice = True
                if event.key == pg.K_n:
                    if turn == 0: #white
                        choice = Type.WHITE_KNIGHT
                    else: #black
                        choice = Type.BLACK_KNIGHT

                    valid_choice = True
                if event.key == pg.K_b:
                    if turn == 0: #white
                        choice = Type.WHITE_BISHOP
                    else: #black
                        choice = Type.BLACK_BISHOP

                    valid_choice = True
                if event.key == pg.K_r:
                    if turn == 0: #white
                        choice = Type.WHITE_ROOK
                    else: #black
                        choice = Type.BLACK_ROOK

                    valid_choice = True

    return choice

def ep(position: list, moves: list):
    global turn
    if moves != []:
        last_move = moves[-1]
        if turn == 0: #white to move, look for black pawn moves
            if last_move[0].type == Type.BLACK_PAWN and last_move[1][0] == 3: #last pawn move is a candidate
                black_pawn_square = [last_move[1][0], last_move[1][1]]
                black_pawn = position[black_pawn_square[0]][black_pawn_square[1]]

                for move in reversed(moves[:-1]): #start from second to last move
                    if position[move[1][0]][move[1][1]] == black_pawn: #the black pawn has moved before, and thus did not double jump
                        return None

                #pawn never moved before last turn, but is on a double moved square. Thus
                #pawn must have just double moved. so we construct the ep square and return
                ep_square = []
                ep_square.append(last_move[1][0] - 1)
                ep_square.append(last_move[1][1])
                
                return ep_square

            else: #no possible ep
                return None
        else: #black to move, look for white pawn moves
            if last_move[0].type == Type.WHITE_PAWN and last_move[1][0] == 4: #last pawn move is a candidate
                white_pawn_square = [last_move[1][0], last_move[1][1]]
                white_pawn = position[white_pawn_square[0]][white_pawn_square[1]]

                for move in reversed(moves[:-1]): #start from second to last move
                    if position[move[1][0]][move[1][1]] == white_pawn: #the black pawn has moved before, and thus did not double jump
                        return None

                #pawn never moved before last turn, but is on a double moved square. Thus
                #pawn must have just double moved. so we construct the ep square and return
                ep_square = []
                ep_square.append(last_move[1][0] + 1)
                ep_square.append(last_move[1][1])
                
                return ep_square

            else: #no possible ep
                return None
    else:
        return None

def has_moved(piece: Piece, moves: list):
    for move in moves:
        if move[0] == piece:
            return True
    return False

def can_castle(position: list, moves: list): #returns dict with bools for kingside and queenside
    global turn
    can_castle_kingside = False
    can_castle_queenside = False
    kingside_rook_moved = True
    queenside_rook_moved = True
    king_moved = True
    in_check = True
    passing_check_kingside = True
    passing_check_queenside = False
    piece_on_castle_square_kingside = True
    piece_on_castle_square_queenside = True


    if turn == 0: #white to move
        piece_on_kingside_rook_square = position[7][7]
        piece_on_queenside_rook_square = position[7][0]
        piece_on_king_square = position[7][4]
        square_right_of_king = [7,5]
        square_two_right_of_king = [7,6]
        square_left_of_king = [7,3]
        square_two_left_of_king = [7,2]
    else:
        piece_on_kingside_rook_square = position[0][7]
        piece_on_queenside_rook_square = position[0][0]
        piece_on_king_square = position[0][4]
        square_right_of_king = [0,5]
        square_two_right_of_king = [0,6]
        square_left_of_king = [0,3]
        square_two_left_of_king = [0,2]

    #check if there in an obstructing piece
    if not position[square_right_of_king[0]][square_right_of_king[1]] and not position[square_two_right_of_king[0]][square_two_right_of_king[1]]:
        piece_on_castle_square_kingside = False

    if not position[square_left_of_king[0]][square_left_of_king[1]] and not position[square_two_left_of_king[0]][square_two_left_of_king[1]]:
        piece_on_castle_square_queenside = False

    #check if kingside rook moved
    if piece_on_kingside_rook_square: #piece on king's rook square
        kingside_rook_moved = has_moved(piece_on_kingside_rook_square, moves)

    #check if queenside rook moved
    if piece_on_queenside_rook_square: #piece on queen's rook square
        queenside_rook_moved = has_moved(piece_on_queenside_rook_square, moves)

    #check if king moved
    if piece_on_king_square: #piece on king's rook square
        king_moved = has_moved(piece_on_king_square, moves)
    
    #check if king is currently in check if necessary
    if not king_moved:
        in_check = is_check(position, moves)

    #check if king will pass over a square in check kingside
    if not king_moved and not kingside_rook_moved and not in_check:
        position_one = suppose_move(piece_on_king_square, square_right_of_king, position)
        position_two = suppose_move(piece_on_king_square, square_two_right_of_king, position)

        if not is_check(position_one, moves) and not is_check(position_two, moves):
            passing_check_kingside = False
    #check if king will pass over a sqaure in check queenside
    if not king_moved and not queenside_rook_moved and not in_check:
        position_one = suppose_move(piece_on_king_square, square_left_of_king, position)
        position_two = suppose_move(piece_on_king_square, square_two_left_of_king, position)

        if not is_check(position_one, moves) and not is_check(position_two, moves):
            passing_check_queenside = False

    #decide if king can castle on either side
    if not king_moved and not in_check:
        if not kingside_rook_moved and not passing_check_kingside and not piece_on_castle_square_kingside:
            can_castle_kingside = True
        if not queenside_rook_moved and not passing_check_queenside and not piece_on_castle_square_queenside:
            can_castle_queenside = True

    return {
        "queenside" : can_castle_queenside,
        "kingside" : can_castle_kingside
    }

def get_valid_moves(piece_square: list, position: list, moves: list): #gets valid moves for specific piece
    piece = position[piece_square[0]][piece_square[1]]
    valid_squares = []

    if piece:
        #handle check
        possible_squares = generate_attacked_squares(piece, position, moves)
        for square in possible_squares:
            supposed_position = suppose_move(piece, square, position)
            if not is_check(supposed_position, moves):
                valid_squares.append(square)
        #handle castling
        if piece.type == Type.WHITE_KING or piece.type == Type.BLACK_KING:
            castle = can_castle(position, moves)
            if turn == 0:
                if castle['queenside']:
                    valid_squares.append([7,2])
                if castle['kingside']:
                    valid_squares.append([7,6])
            else:
                if castle['queenside']:
                    valid_squares.append([0,2])
                if castle['kingside']:
                    valid_squares.append([0,6])

    return valid_squares

def get_all_valid_moves(position: list, moves: list): #gets all valid moves for color making a move
    global turn
    valid_squares = []
    res = []

    for i in range(8):
        for j in range(8):
            piece = position[i][j]
            if piece:
                if piece.get_color().value == turn: #color is same
                    valid_squares += get_valid_moves([i,j], position, moves)

    #remove duplicate squares and return
    [res.append(square) for square in valid_squares if square not in res]
    return res

def __is_stalemate(position: list, moves: list) -> bool:
    if get_all_valid_moves(position, moves) == [] and not is_check(position, moves):
        return True
    return False

def __is_draw_by_50_moves(moves: list) -> bool:
    if len(moves) < 100:
        return False
    else:
        moves_without_pawn_move = 0
        for i in range(len(moves)):
            if i % 1 == 0:
                moves_without_pawn_move += 1
            if moves[i][0].type == Type.BLACK_PAWN or moves[i][0].type == Type.WHITE_PAWN:
                moves_without_pawn_move = 0
            if moves_without_pawn_move > 50:
                return True
    return False
            

def __is_draw_by_repetition(position: list, moves: list) -> bool:
    return False

def is_draw(position: list, moves: list) -> bool:
    if __is_stalemate(position, moves) or __is_draw_by_50_moves(moves) or __is_draw_by_repetition(position, moves):
        return True
    return False