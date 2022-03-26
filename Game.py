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

def __generate_attacked_squares_pawn(pawn: Piece, board: Board):
    attacked_squares = []
    #determine if the pawn has previously moved
    has_moved = False
    if pawn.get_color() == Color.WHITE and pawn.square[0] == 6:
        has_moved = True
    elif pawn.get_color() == Color.BLACK and pawn.square[0] == 1:
        has_moved = True

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

def __generate_attacked_squares_knight(knight: Piece):
    pass
def __generate_attacked_squares_rook(rook: Piece):
    pass
def __generate_attacked_squares_bishop(bishop: Piece):
    pass
def __generate_attacked_squares_queen(queen: Piece):
    pass
def __generate_attacked_squares_king(king: Piece):
    pass

def generate_attacked_pieces(piece: Piece, board: Board):
    pass

def is_check(board: Board):
    pass

def is_win(board: Board):
    pass

def change_turn(board: Board):
    pass