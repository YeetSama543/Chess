from Game import *
from Board import Board
from Piece import *
import unittest

POS = (0,0)
board = Board(POS)
board.add_pieces()

class TestGame(unittest.TestCase):
    def test_get_clicked_square(self):
        self.assertEqual(get_clicked_square((55, 47), board.pos), [0,0])
        self.assertEqual(get_clicked_square((662, 39), board.pos), [0,7])
        self.assertEqual(get_clicked_square((671, 672), board.pos), [7,7])
        self.assertEqual(get_clicked_square((54, 664), board.pos), [7,0])
        self.assertEqual(get_clicked_square((233, 319), board.pos), [3,2])
        self.assertEqual(get_clicked_square((407, 408), board.pos), [4,4])
    def test_clicked_on_board(self):
        self.assertEqual(clicked_on_board((14, 41), board.pos), True)
        self.assertEqual(clicked_on_board((676, 50), board.pos), True)
        self.assertEqual(clicked_on_board((657, 683), board.pos), True)
        self.assertEqual(clicked_on_board((230, 400), board.pos), True)
        self.assertEqual(clicked_on_board((1049, 192), board.pos), False)
        self.assertEqual(clicked_on_board((306, 934), board.pos), False)
    def test_suppose_move(self):
        position = board.position
        new_square = [4,4]
        old_square = [6,4]
        piece = board.get_piece_on_square(old_square)

        new_position = suppose_move(piece, new_square, position)
        for i in range(8):
            for j in range(8):
                if i != new_square[0] or j != new_square[1]:
                    if i != old_square[0] or j != old_square[1]:
                        #square is neither old nor new, should equal the same as original position
                        self.assertEqual(new_position[i][j], position[i][j])
        #these are the changed squares. Old square should have no piece on it. New
        #square should have the piece on it now
        self.assertEqual(new_position[new_square[0]][new_square[1]], piece)
        self.assertEqual(new_position[old_square[0]][old_square[1]], None)