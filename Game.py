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

def __generate_attacked_squares_pawn(pawn: Piece):
    pass
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