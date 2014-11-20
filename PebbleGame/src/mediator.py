'''
Mediator.py
by: David Shuckerow (djs0017@auburn.edu) and Carlos Lemus (cal0018@auburn.edu)
date: 11/19/2014

The Mediator class implements the mediator design pattern.
It is responsible for coordinating the Board model, the View of the board, and
the AI Controller(s) responsible for instructing how to change the board state.
'''
__author__ = "Carlos Lemus, David Shuckerow"
__license__ = "MIT"

import board


class Mediator:
    """
    Stub for now.
    """
    def __init__(self):
        self.gameBoard = board.Board(2, 2)

    def main(self):
        pass

    def setState(self, player, square):
        """
        :param player: the number of the player (integer 0 or 1)
        :param square: the square from which to begin the move (in range(0,n))
        Validate the player and square to be valid and then move.
        If the move is not valid, then return False.
        If the move is valid, then perform the move and return True.
        """
        self.gameBoard.move(player, square)
        return True

if __name__ == '__main__':
    Mediator().main()
