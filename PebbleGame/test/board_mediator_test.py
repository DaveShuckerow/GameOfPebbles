"""
Tests for the board class
"""
__author__ = 'Carlos Lemus'
__license__ = "MIT"

import unittest

import PebbleGame.src.board as board
import PebbleGame.src.board_mediator as board_mediator


class BoardMediatorTest(unittest.TestCase):
    def setUp(self):
        self.test_board = board.Board(2, 2)
        self.test_mediator = board_mediator.BoardMediator(self.test_board, None)

    def testGoodMovePlayer1(self):
        self.assertTrue(self.test_mediator.set_state(0, 0, 0))

    def testGoodMovePlayer2(self):
        self.assertTrue(self.test_mediator.set_state(1, 1, 0))

    def testBadMovePlayer1(self):
        self.assertFalse(self.test_mediator.set_state(0, 1, 0))

    def testBadMovePlayer2(self):
        self.assertFalse(self.test_mediator.set_state(1, 0, 0))
        # TODO: make tests to check that squares have been mov


if __name__ == '__main__':
    unittest.main()