import pygame as pg

#load image
pieces_image = pg.image.load('540px-Chess_Pieces_Sprite.png')
piece_width = pieces_image.get_width() // 6
piece_height = pieces_image.get_height() // 2

#create dict containing surfaces of pieces
white_pieces = []
black_pieces = []

for i in range(6): #white pieces
    white_pieces.append(pieces_image.subsurface(i * piece_width, 0, piece_width, piece_height))
for i in range(6): #black pieces
    black_pieces.append(pieces_image.subsurface(i * piece_width, piece_height, piece_width, piece_height))

images = {
    'K' : white_pieces[0],
    'Q' : white_pieces[1],
    'B' : white_pieces[2],
    'N' : white_pieces[3],
    'R' : white_pieces[4],
    'P' : white_pieces[5],
    'k' : black_pieces[0],
    'q' : black_pieces[1],
    'b' : black_pieces[2],
    'n' : black_pieces[3],
    'r' : black_pieces[4],
    'p' : black_pieces[5] 
}