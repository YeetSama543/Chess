import pygame as pg
from Piece import *
from Game_Constants import *

class Board:
    def __init__(self, pos: tuple):
        self.pos = pos
        self.position = [[None for i in range(8)] for j in range(8)]
        self.pieces = []
        self.clicked_piece = None

        self.moves = []

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

    def add(self, piece: Piece): #adds a single piece to board
        self.pieces.append(piece)
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
        for piece in self.pieces:
            piece_pos = self.square_to_topleft(piece.square)
            piece.draw(surf, piece_pos)

    def update(self, surf: pg.Surface): #redraw pieces
        for piece in self.pieces:
            piece_pos = self.square_to_topleft(piece.square)
            piece.draw(surf, piece_pos)

    def move(self, new_square): #moves clicked piece to new square
        if self.clicked_piece:
            #add to moves
            self.moves.append([self.clicked_piece.type, new_square])

            #remove piece on target square if needed
            piece_on_clicked_square = self.get_piece_on_square(new_square)
            if piece_on_clicked_square:
                self.remove_piece(piece_on_clicked_square)

            #move piece
            self.position[new_square[0]][new_square[1]] = self.clicked_piece
            self.position[self.clicked_piece.square[0]][self.clicked_piece.square[1]] = None
            self.clicked_piece.place(new_square)
            self.clicked_piece = None

    def get_piece_on_square(self, square: list) -> Piece:
        return self.position[square[0]][square[1]]
    
    def highlight_clicked_square(self, surf: pg.Surface):
        #create highlighted square
        topleft = self.square_to_topleft(self.clicked_piece.square)
        highlighted_square = pg.Surface((SQUARE_SIZE,SQUARE_SIZE))
        highlighted_square.fill(HIGHLIGHT_SQUARE_COLOR)
        #draw square onto board
        surf.blit(highlighted_square, topleft)
        #redraw piece
        self.clicked_piece.draw(surf, topleft)

    def highlight_attacked_squares(self, surf: pg.Surface, squares: list):
        attacked_square = pg.Surface((SQUARE_SIZE,SQUARE_SIZE))
        attacked_square.fill(ATTACKED_SQUARE_COLOR)

        for square in squares:
            #draw attacked square
            topleft = self.square_to_topleft(square)
            surf.blit(attacked_square, topleft)
            #draw piece if there originally was one
            piece_on_square = self.get_piece_on_square(square)
            if piece_on_square:
                piece_on_square.draw(surf, topleft)

    def click_piece(self, screen: pg.Surface, piece: Piece, attacked_squares: list): #highlights piece, attacked squares
        self.clicked_piece = piece
        self.highlight_clicked_square(screen)
        self.highlight_attacked_squares(screen, attacked_squares)

    def remove_piece(self, piece_to_remove: Piece):
        for piece in self.pieces:
            if piece.square == piece_to_remove.square:
                self.position[piece.square[0]][piece.square[1]] = None
                self.pieces.remove(piece)
                return True
        return False