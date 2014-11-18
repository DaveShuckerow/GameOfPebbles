'''
The Board class represents a board game containing n columns,
p pebbles per square, and one row per player. It provides functions
necessary for moving pebbles and copying the current game state.
'''
__author__ = "Carlos Lemus, David Shuckerow"
__license__ = "MIT"


class Board(object):
    """
    :param n: number of squares per player.
    :param p: number of pebbles per square.
    """

    def __init__(self, n, p):
        self.squares = [[p for _ in range(2)] for _ in range(n)]
        pass

    def move(self):
        """ Performs a move on the selected square. """
        pass

    # TODO: add copy method.

    def get_score(self, player):
        """
        :param player:
        """
        pass
