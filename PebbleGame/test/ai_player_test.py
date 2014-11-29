"""
Tests for the AIPlayer class
"""
__author__ = 'Carlos Lemus'
__license__ = "MIT"

import unittest

from PebbleGame.src.ai_player import AIPlayer as AIPlayer
from PebbleGame.src.board import Board as Board


class AIPlayer_Test(unittest.TestCase):
    def setUp(self):
        self.test_ai_player = AIPlayer(None)
        self.test_board = Board(2, 2)

    def test_terminaltest_correct1(self):
        self.test_board.squares = [[0, 0], [0, 1]]

        self.assertTrue(self.test_ai_player.terminal_test(self.test_board),
                        "AIPlayer.terminal_test: function did not return expected value for true terminal state.")

    def test_terminaltest_correct2(self):
        self.test_board.squares = [[0, 0], [0, 1]]

        self.assertTrue(self.test_ai_player.terminal_test(self.test_board),
                        "AIPlayer.terminal_test: function did not return expected value for true terminal state.")

    def test_terminaltest_incorrect1(self):
        ''' An initial board tested for terminal state '''

        self.assertFalse(self.test_ai_player.terminal_test(self.test_board),
                        "AIPlayer.terminal_test: function did not return expected value for false terminal state.")


    def test_terminaltest_incorrect2(self):
        ''' An "almost" terminal state '''
        self.test_board.squares = [[3, 4], [0, 1]]

        self.assertFalse(self.test_ai_player.terminal_test(self.test_board),
                        "AIPlayer.terminal_test: function did not return expected value for false terminal state.")


if __name__ == '__main__':
    unittest.main()
