#contains functionality of the game

from Board import Board
from Piece import *
from Game_Constants import *

def get_clicked_square(mouse_pos: tuple, board: Board) -> list:
    relative_x = mouse_pos[0] - board.pos[0]
    relative_y = mouse_pos[1] - board.pos[1]
    return [relative_y // SQUARE_SIZE, relative_x // SQUARE_SIZE] #x and y get flipped since first val represents the row# and second is col#

def clicked_on_board(mouse_pos: tuple, board: Board) -> bool:
    min_x = board.pos[0]
    max_x = board.pos[0] + BOARD_SIZE
    min_y = board.pos[1]
    max_y = board.pos[1] + BOARD_SIZE

    if mouse_pos[0] > min_x and mouse_pos[0] < max_x:
        if mouse_pos[1] > min_y and mouse_pos[1] < max_y:
            return True
    return False

def is_valid_square(square: list) -> bool:
    if square[0] > 7 or square[0] < 0 or square[1] > 7 or square[1] < 0:
        return False
    return True

#these move generating helper functions DO NOT account for special rules, such as check and E.P.
def __generate_attacked_squares_pawn(pawn: Piece, board: Board):
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
    if is_valid_square(square_in_front) and not board.get_piece_on_square(square_in_front):
        attacked_squares.append(square_in_front)
        #now check if pawn can move forward twice
        if not has_moved and is_valid_square(square_two_ahead) and not board.get_piece_on_square(square_two_ahead):
            attacked_squares.append(square_two_ahead)
    #check if pawn can move diagonally
    if is_valid_square(diag_left) and board.get_piece_on_square(diag_left):
        if board.get_piece_on_square(diag_left).get_color() != pawn.get_color():
            attacked_squares.append(diag_left)
    if is_valid_square(diag_right) and board.get_piece_on_square(diag_right):
        if board.get_piece_on_square(diag_right).get_color() != pawn.get_color():
            attacked_squares.append(diag_right)
    return attacked_squares

def __generate_attacked_squares_knight(knight: Piece, board: Board):
    attacked_squares = []
    for i in [-2,2]:
        for j in [-1,1]:
            potential_square_vertical = [knight.square[0] + i, knight.square[1] + j]
            potential_square_horizontal = [knight.square[0] + j, knight.square[1] + i]

            if is_valid_square(potential_square_vertical):
                if not board.get_piece_on_square(potential_square_vertical): #no piece on square
                    attacked_squares.append(potential_square_vertical)
                elif board.get_piece_on_square(potential_square_vertical).get_color() != knight.get_color():
                    attacked_squares.append(potential_square_vertical)
            
            if is_valid_square(potential_square_horizontal):
                if not board.get_piece_on_square(potential_square_horizontal): #no piece on square
                    attacked_squares.append(potential_square_horizontal)
                elif board.get_piece_on_square(potential_square_horizontal).get_color() != knight.get_color():
                    attacked_squares.append(potential_square_horizontal)
    return attacked_squares
    
def __generate_attacked_squares_rook(rook: Piece, board: Board):
    attacked_squares = []
    #up
    valid = True
    row = rook.square[0]
    col = rook.square[1]
    while valid:
        row -= 1
        potential_square = [row, col]
        if is_valid_square(potential_square):
            if not board.get_piece_on_square(potential_square):
                attacked_squares.append(potential_square)
            elif board.get_piece_on_square(potential_square).get_color() != rook.get_color():
                attacked_squares.append(potential_square)
                valid = False #square was valid, but next one will not be
            elif board.get_piece_on_square(potential_square).get_color() == rook.get_color():
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
            if not board.get_piece_on_square(potential_square):
                attacked_squares.append(potential_square)
            elif board.get_piece_on_square(potential_square).get_color() != rook.get_color():
                attacked_squares.append(potential_square)
                valid = False #square was valid, but next one will not be
            elif board.get_piece_on_square(potential_square).get_color() == rook.get_color():
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
            if not board.get_piece_on_square(potential_square):
                attacked_squares.append(potential_square)
            elif board.get_piece_on_square(potential_square).get_color() != rook.get_color():
                attacked_squares.append(potential_square)
                valid = False #square was valid, but next one will not be
            elif board.get_piece_on_square(potential_square).get_color() == rook.get_color():
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
            if not board.get_piece_on_square(potential_square):
                attacked_squares.append(potential_square)
            elif board.get_piece_on_square(potential_square).get_color() != rook.get_color():
                attacked_squares.append(potential_square)
                valid = False #square was valid, but next one will not be
            elif board.get_piece_on_square(potential_square).get_color() == rook.get_color():
                valid = False
        else:
            valid = False

    return attacked_squares

def __generate_attacked_squares_bishop(bishop: Piece, board: Board):
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
            if not board.get_piece_on_square(potential_square):
                attacked_squares.append(potential_square)
            elif board.get_piece_on_square(potential_square).get_color() != bishop.get_color():
                attacked_squares.append(potential_square)
                valid = False #square was valid, but next one will not be
            elif board.get_piece_on_square(potential_square).get_color() == bishop.get_color():
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
            if not board.get_piece_on_square(potential_square):
                attacked_squares.append(potential_square)
            elif board.get_piece_on_square(potential_square).get_color() != bishop.get_color():
                attacked_squares.append(potential_square)
                valid = False #square was valid, but next one will not be
            elif board.get_piece_on_square(potential_square).get_color() == bishop.get_color():
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
            if not board.get_piece_on_square(potential_square):
                attacked_squares.append(potential_square)
            elif board.get_piece_on_square(potential_square).get_color() != bishop.get_color():
                attacked_squares.append(potential_square)
                valid = False #square was valid, but next one will not be
            elif board.get_piece_on_square(potential_square).get_color() == bishop.get_color():
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
            if not board.get_piece_on_square(potential_square):
                attacked_squares.append(potential_square)
            elif board.get_piece_on_square(potential_square).get_color() != bishop.get_color():
                attacked_squares.append(potential_square)
                valid = False #square was valid, but next one will not be
            elif board.get_piece_on_square(potential_square).get_color() == bishop.get_color():
                valid = False
        else:
            valid = False

    return attacked_squares
def __generate_attacked_squares_queen(queen: Piece, board: Board):
    #queen is combination of rook and bishop
    #so generate moves for rook and bishop and return both together

    rook_squares = __generate_attacked_squares_rook(queen, board)
    bishop_squares = __generate_attacked_squares_bishop(queen, board)
    attacked_squares = rook_squares + bishop_squares

    return attacked_squares
def __generate_attacked_squares_king(king: Piece, board: Board):
    attacked_squares = []
    #we include the original square of the king as part of the squares we check in the
    #following for loop, but since the king's color is equal to itself, the square won't be added

    for i in [-1, 0, 1]:
        for j in [-1, 0, 1]:
            potential_square = [king.square[0] + i, king.square[1] + j]
            if is_valid_square(potential_square):
                if not board.get_piece_on_square(potential_square): #no piece on square
                    attacked_squares.append(potential_square)
                elif board.get_piece_on_square(potential_square).get_color() != king.get_color():
                    attacked_squares.append(potential_square)

    return attacked_squares

def generate_attacked_squares(piece: Piece, board: Board):
    attacked_squares = []
    if piece.type == Type.BLACK_PAWN or piece.type == Type.WHITE_PAWN:
        attacked_squares = __generate_attacked_squares_pawn(piece,board)
    elif piece.type == Type.BLACK_ROOK or piece.type == Type.WHITE_ROOK:
        attacked_squares = __generate_attacked_squares_rook(piece,board)
    elif piece.type == Type.BLACK_KNIGHT or piece.type == Type.WHITE_KNIGHT:
        attacked_squares = __generate_attacked_squares_knight(piece,board)
    elif piece.type == Type.BLACK_BISHOP or piece.type == Type.WHITE_BISHOP:
        attacked_squares = __generate_attacked_squares_bishop(piece,board)
    elif piece.type == Type.BLACK_QUEEN or piece.type == Type.WHITE_QUEEN:
        attacked_squares = __generate_attacked_squares_queen(piece,board)
    elif piece.type == Type.BLACK_KING or piece.type == Type.WHITE_KING:
        attacked_squares = __generate_attacked_squares_king(piece,board)
    ###Handle special rules here###

    ###############################
    return attacked_squares

def is_check(board: Board):
    pass

def is_win(board: Board, turn: int):
    pass

def change_turn(board: Board, turn: int): #changes turn and return it. Also resets clicked piece
    turn += 1
    turn %= 2
    board.clicked_piece = None

    return turn

def pawn_promotion():
    pass

def ep():
    pass