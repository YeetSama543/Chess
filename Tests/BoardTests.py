from Board import Board
from Piece import *
from Game_Constants import SQUARE_SIZE
import unittest

POS = (0,0)
board = Board(POS)
board.add_pieces()

class TestBoard(unittest.TestCase):
    def test_position_rook(self):
        self.assertEqual(board.position[0][0].type, Type.BLACK_ROOK)
        self.assertEqual(board.position[0][7].type, Type.BLACK_ROOK)
        self.assertEqual(board.position[7][0].type, Type.WHITE_ROOK)
        self.assertEqual(board.position[7][7].type, Type.WHITE_ROOK)
    def test_position_knight(self):
        self.assertEqual(board.position[0][1].type, Type.BLACK_KNIGHT)
        self.assertEqual(board.position[0][6].type, Type.BLACK_KNIGHT)
        self.assertEqual(board.position[7][1].type, Type.WHITE_KNIGHT)
        self.assertEqual(board.position[7][6].type, Type.WHITE_KNIGHT)
    def test_position_bishop(self):
        self.assertEqual(board.position[0][2].type, Type.BLACK_BISHOP)
        self.assertEqual(board.position[0][5].type, Type.BLACK_BISHOP)
        self.assertEqual(board.position[7][2].type, Type.WHITE_BISHOP)
        self.assertEqual(board.position[7][5].type, Type.WHITE_BISHOP)
    def test_position_queen(self):
        self.assertEqual(board.position[0][3].type, Type.BLACK_QUEEN)
        self.assertEqual(board.position[7][3].type, Type.WHITE_QUEEN)
    def test_position_king(self):
        self.assertEqual(board.position[0][4].type, Type.BLACK_KING)
        self.assertEqual(board.position[7][4].type, Type.WHITE_KING)
    def test_position_pawn(self):
        for i in range(8):
            self.assertEqual(board.position[1][i].type, Type.BLACK_PAWN)
            self.assertEqual(board.position[6][i].type, Type.WHITE_PAWN)
    def test_position_empty(self):
        for i in range(2,5):
            for j in range(8):
                self.assertEqual(board.position[i][j], None)
    def test_square_to_topleft(self):
        self.assertEqual(board.square_to_topleft([0,0]), (0,0))
        self.assertEqual(board.square_to_topleft([0,1]), (SQUARE_SIZE * 1,0))
        self.assertEqual(board.square_to_topleft([0,2]), (SQUARE_SIZE * 2,0))
        self.assertEqual(board.square_to_topleft([0,3]), (SQUARE_SIZE * 3,0))
        self.assertEqual(board.square_to_topleft([0,4]), (SQUARE_SIZE * 4,0))
        self.assertEqual(board.square_to_topleft([0,5]), (SQUARE_SIZE * 5,0))
        self.assertEqual(board.square_to_topleft([0,6]), (SQUARE_SIZE * 6,0))
        self.assertEqual(board.square_to_topleft([0,7]), (SQUARE_SIZE * 7,0))

        self.assertEqual(board.square_to_topleft([2,0]), (0,SQUARE_SIZE * 2))
        self.assertEqual(board.square_to_topleft([2,1]), (SQUARE_SIZE * 1,SQUARE_SIZE * 2))
        self.assertEqual(board.square_to_topleft([2,2]), (SQUARE_SIZE * 2,SQUARE_SIZE * 2))
        self.assertEqual(board.square_to_topleft([2,3]), (SQUARE_SIZE * 3,SQUARE_SIZE * 2))
        self.assertEqual(board.square_to_topleft([2,4]), (SQUARE_SIZE * 4,SQUARE_SIZE * 2))
        self.assertEqual(board.square_to_topleft([2,5]), (SQUARE_SIZE * 5,SQUARE_SIZE * 2))
        self.assertEqual(board.square_to_topleft([2,6]), (SQUARE_SIZE * 6,SQUARE_SIZE * 2))
        self.assertEqual(board.square_to_topleft([2,7]), (SQUARE_SIZE * 7,SQUARE_SIZE * 2))
    def test_move(self):
        #create second board to not mess up above tests
        board2 = Board(POS)
        board2.add_pieces()
        #set clicked piece and move it
        board2.clicked_piece = board2.position[0][0] #black rook on a8
        board2.move([2,0])
        
        self.assertEqual(board2.position[2][0].type, Type.BLACK_ROOK)