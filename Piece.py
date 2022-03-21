import pygame as pg
from enum import Enum

class Type(Enum):
    WHITE_PAWN = 'P'
    WHITE_KNIGHT = 'N'
    WHITE_BISHOP = 'B'
    WHITE_ROOK = 'R'
    WHITE_QUEEN = 'Q'
    WHITE_KING = 'K'

    BLACK_PAWN = 'p'
    BLACK_KNIGHT = 'n'
    BLACK_BISHOP = 'b'
    BLACK_ROOK = 'r'
    BLACK_QUEEN = 'q'
    BLACK_KING = 'k'

class Color(Enum):
    WHITE = 0
    BLACK = 1

class Piece:
    def __init__(self, color: Color, type: Type, square: list):
        self.color = color
        self.type = type
        self.square = square
    def draw(self, surf: pg.Surface, pos: tuple):
        pass
    def place(self, newSquare: list):
        self.square = newSquare
    def remove(self):
        self.square = None