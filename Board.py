import pygame as pg
from Piece import *
from Game_Constants import *

class Board:
    def __init__(self, pos: tuple):
        self.pos = pos
        self.position = [[None for i in range(8)] for j in range(8)]
        self.pieces = []
        self.clicked_piece = None

    def add_pieces(self): #adds all pieces onto board for start of game
        #rooks
        self.pieces.append(Piece(Type.WHITE_ROOK, [7,0]))
        self.pieces.append(Piece(Type.WHITE_ROOK, [7,7]))
        self.pieces.append(Piece(Type.BLACK_ROOK, [0,0]))
        self.pieces.append(Piece(Type.BLACK_ROOK, [0,7]))

        #knights
        self.pieces.append(Piece(Type.WHITE_KNIGHT, [7,1]))
        self.pieces.append(Piece(Type.WHITE_KNIGHT, [7,6]))
        self.pieces.append(Piece(Type.BLACK_KNIGHT, [0,1]))
        self.pieces.append(Piece(Type.BLACK_KNIGHT, [0,6]))

        #bishops
        self.pieces.append(Piece(Type.WHITE_BISHOP, [7,2]))
        self.pieces.append(Piece(Type.WHITE_BISHOP, [7,5]))
        self.pieces.append(Piece(Type.BLACK_BISHOP, [0,2]))
        self.pieces.append(Piece(Type.BLACK_BISHOP, [0,5]))

        #queens
        self.pieces.append(Piece(Type.WHITE_QUEEN, [7,3]))
        self.pieces.append(Piece(Type.BLACK_QUEEN, [0,3]))
        #kings
        self.pieces.append(Piece(Type.WHITE_KING, [7,4]))
        self.pieces.append(Piece(Type.BLACK_KING, [0,4]))

        #pawns
        for i in range(8):
            self.pieces.append(Piece(Type.WHITE_PAWN, [6,i]))
            self.pieces.append(Piece(Type.BLACK_PAWN, [1,i]))

        #update position with all the new pieces
        for piece in self.pieces:
            self.position[piece.square[0]][piece.square[1]] = piece

    def square_to_topleft(self, square: list) -> tuple: #returns topleft position of corresponding square
        x = self.pos[0] + (square[1] * SQUARE_SIZE)
        y = self.pos[1] + (square[0] * SQUARE_SIZE)
        return (x,y)
    def draw(self, surf: pg.Surface):
        #create light and dark squares
        light_square = pg.Surface((SQUARE_SIZE, SQUARE_SIZE))
        light_square.fill(LIGHT_SQUARE_COLOR)
        dark_square = pg.Surface((SQUARE_SIZE, SQUARE_SIZE))
        dark_square.fill(DARK_SQUARE_COLOR)

        #draw squares
        for i in range(8):
            for j in range(8):
                topleft = self.square_to_topleft([i,j])
                if (i + j) % 2 == 0:
                    surf.blit(light_square, topleft)
                else:
                    surf.blit(dark_square, topleft)

        #draw pieces

    def move(self, new_square):
        pass