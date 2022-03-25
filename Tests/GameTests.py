from Game import *
from Board import Board
from Piece import *
import unittest

POS = (0,0)
board = Board(POS)
board.add_pieces()

class TestGame(unittest.TestCase):
    def test_get_clicked_square(self):
        self.assertEqual(get_clicked_square((55, 47), board), [0,0])
        self.assertEqual(get_clicked_square((662, 39), board), [0,7])
        self.assertEqual(get_clicked_square((671, 672), board), [7,7])
        self.assertEqual(get_clicked_square((54, 664), board), [7,0])
        self.assertEqual(get_clicked_square((233, 319), board), [3,2])
        self.assertEqual(get_clicked_square((407, 408), board), [4,4])
    def test_clicked_on_board(self):
        self.assertEqual(clicked_on_board((14, 41), board), True)
        self.assertEqual(clicked_on_board((676, 50), board), True)
        self.assertEqual(clicked_on_board((657, 683), board), True)
        self.assertEqual(clicked_on_board((230, 400), board), True)
        self.assertEqual(clicked_on_board((1049, 192), board), False)
        self.assertEqual(clicked_on_board((306, 934), board), False)