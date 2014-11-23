"""
Tests for Board Class
"""
__author__ = "Carlos Lemus, David Shuckerow"
__license__ = "MIT"

import unittest
from PebbleGame.src import board


class BoardTest(unittest.TestCase):
    def test_move1(self):
        test_board = board.Board(2, 2)
        test_board.move(1, 0)

        expected = [[3, 3], [0, 2]]
        self.assertEqual(test_board.squares, expected,
                         "Board.move: Expected board " + str(expected) + " but got "
                         + str(test_board.squares))

    def test_move2(self):
        test_board = board.Board(2, 2)
        test_board.move(0, 1)

        expected = [[2, 0], [3, 3]]
        self.assertEqual(test_board.squares, expected,
                         "Board.move: Expected board " + str(expected) + " but got "
                         + str(test_board.squares))


if __name__ == '__main__':
    unittest.main()
