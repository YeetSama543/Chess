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

    def is_castle_square(self, new_square) -> bool:
        if self.clicked_piece.get_color() == Color.WHITE:
            if self.clicked_piece.type == Type.WHITE_KING and self.clicked_piece.square == [7,4]:
                if new_square == [7,6] or new_square == [7,2]:
                    return True
            return False

        else:
            if self.clicked_piece.type == Type.BLACK_KING and self.clicked_piece.square == [0,4]:
                if new_square == [0,6] or new_square == [0,2]:
                    return True
            return False

    def castle(self, castle_square):
        if self.clicked_piece.get_color() == Color.WHITE:
            if castle_square == [7,6]: #kingside castle
                rook_dest = [7,5]
                rook_start = [7,7]
            elif castle_square == [7,2]: #queenside
                rook_dest = [7,3]
                rook_start = [7,0]
        else:
            if castle_square == [0,6]: #kingside castle
                rook_dest = [0,5]
                rook_start = [0,7]
            elif castle_square == [0,2]: #queenside
                rook_dest = [0,3]
                rook_start = [0,0]
        #move king
        self.position[castle_square[0]][castle_square[1]] = self.clicked_piece
        self.position[self.clicked_piece.square[0]][self.clicked_piece.square[1]] = None
        self.clicked_piece.place(castle_square)
        self.clicked_piece = None

        #move rook
        self.position[rook_dest[0]][rook_dest[1]] = self.position[rook_start[0]][rook_start[1]]
        self.position[rook_start[0]][rook_start[1]] = None
        self.position[rook_dest[0]][rook_dest[1]].place(rook_dest)


    def move(self, new_square): #moves clicked piece to new square
        if self.clicked_piece:
            #add to moves
            self.moves.append([self.clicked_piece, new_square])

            if self.is_castle_square(new_square): #castle
                self.castle(new_square)

            else: #not castle, move normally
                #remove piece on target square if needed
                piece_on_clicked_square = self.get_piece_on_square(new_square)
                if piece_on_clicked_square:
                    self.remove_piece(piece_on_clicked_square)

                else: #no piece on clicked square, handle ep
                    if self.clicked_piece.type == Type.WHITE_PAWN or self.clicked_piece.type == Type.BLACK_PAWN:
                        if self.clicked_piece.square[1] != new_square[1]:
                            if self.clicked_piece.get_color() == Color.WHITE:
                                taken_piece_square = [new_square[0] + 1, new_square[1]]
                            else:
                                taken_piece_square = [new_square[0] - 1, new_square[1]]

                            #remove piece
                            taken_piece = self.get_piece_on_square(taken_piece_square)
                            self.remove_piece(taken_piece)

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
        highlighted_square = pg.Surface((SQUARE_SIZE,SQUARE_SIZE), pg.SRCALPHA)
        highlighted_square.convert_alpha()
        highlighted_square.fill(HIGHLIGHT_SQUARE_COLOR)

        #draw square onto board
        surf.blit(highlighted_square, topleft)

        #redraw piece
        self.clicked_piece.draw(surf, topleft)

    def highlight_attacked_squares(self, surf: pg.Surface, squares: list):
        attacked_square = pg.Surface((SQUARE_SIZE,SQUARE_SIZE), pg.SRCALPHA)
        attacked_square.convert_alpha()
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
                piece.place(None)
                self.pieces.remove(piece)
                return True
        return False

    def promote(self, square: list, choice: Type):
        self.remove_piece(self.get_piece_on_square(square))
        self.add(Piece(choice, square))