import pygame as pg
from Images import images
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
    def __init__(self, type: Type, square: list):
        self.type = type
        self.square = square
        self.has_moved = False
    def draw(self, surf: pg.Surface, pos: tuple):
        image = images[self.type.value]
        surf.blit(image, pos)
    def place(self, newSquare: list):
        self.square = newSquare
        self.has_moved = True
    def get_color(self) -> Color:
        if self.type.value.isupper(): #white
            return Color.WHITE
        return Color.BLACK