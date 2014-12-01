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
        self.test_ai_player = AIPlayer(mediator=None, playerID=0)
        self.test_board = Board(2, 2)

    def test_terminaltest_correct1(self):
        self.test_board.squares = [[0, 0], [3, 5]]

        self.assertTrue(self.test_ai_player.terminal_test(self.test_board),
                        "AIPlayer.terminal_test: function did not return expected value for true terminal state.")

    def test_terminaltest_correct2(self):
        self.test_board.squares = [[0, 0], [5, 3]]

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

    def test_cutofftest_mindepth(self):
        ''' Use minimum depth '''
        self.assertFalse(self.test_ai_player.cutoff_test(self.test_board, 0),
                         "AIPlayer.cutoff_test: function did not return False for non-terminal board and minimum depth.")

    def test_cutofftest_maxdepth(self):
        ''' Use maximum depth '''
        self.assertTrue(self.test_ai_player.cutoff_test(self.test_board, self.test_ai_player.MAX_DEPTH),
                        "AIPlayer.cutoff_test: function did not return True for non-terminal board and maximum depth.")

    def test_cutofftest_terminalboard(self):
        self.test_board.squares = [[0, 0], [3, 5]]

        self.assertTrue(self.test_ai_player.cutoff_test(self.test_board, 0),
                        "AIPlayer.cutoff_test: function did not return True for terminal board.")

    def test_defensive_heuristic_p0(self):
        '''tests the defensive heuristic for default player 0'''
        self.test_board.squares = [[1, 0], [2, 5]]
        heuristic_result = self.test_ai_player.defensive_heuristic(self.test_board)

        self.assertEqual(heuristic_result, 1,
                         "AIPlayer.defensive_heuristic: defensive heuristic value returned is invalid. Expected: "
                         + str(1) + " but got " + str(heuristic_result) + ".")

    def test_defensive_heuristic_p1(self):
        '''tests the defensive heuristic for default player 1'''
        self.test_ai_player.playerID = 1
        self.test_board.squares = [[1, 0], [2, 5]]
        heuristic_result = self.test_ai_player.defensive_heuristic(self.test_board)

        self.assertEqual(heuristic_result, 5,
                         "AIPlayer.defensive_heuristic: defensive heuristic value returned is invalid. Expected: "
                         + str(5) + " but got " + str(heuristic_result) + ".")

    def test_aggressive_heuristic_p0(self):
            '''tests the aggressive heuristic for default player 0'''
            self.test_board.squares = [[1, 0], [2, 5]]
            heuristic_result = self.test_ai_player.aggressive_heuristic(self.test_board)

            self.assertEqual(heuristic_result, 0,
                             "AIPlayer.aggressive_heuristic: aggressive heuristic value returned is invalid. Expected: "
                             + str(0) + " but got " + str(heuristic_result) + ".")

    def test_aggressive_heuristic_p1(self):
            '''tests the aggressive heuristic for default player 0'''
            self.test_ai_player.playerID = 1
            self.test_board.squares = [[1, 0], [2, 5]]
            heuristic_result = self.test_ai_player.aggressive_heuristic(self.test_board)

            self.assertEqual(heuristic_result, 2,
                             "AIPlayer.aggressive_heuristic: aggressive heuristic value returned is invalid. Expected: "
                             + str(2) + " but got " + str(heuristic_result) + ".")
if __name__ == '__main__':
    unittest.main()
