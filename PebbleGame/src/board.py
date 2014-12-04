"""
The Board class represents a board game containing n columns,
p pebbles per square, and one row per player. It provides functions
necessary for moving pebbles and copying the current game state.
"""
__author__ = "Carlos Lemus, David Shuckerow"
__license__ = "MIT"


class Board(object):
    """
    :param n: number of squares per player.
    :param p: number of pebbles per square.
    """

    def __init__(self, n, p):
        self._squareCount, self._pebbleCount = n, p
        self.squares = [[p for _ in range(n)] for _ in range(2)]
        self.pebbles = 0

    def move(self, row, col):
        """ Performs a move on the selected square described in row, column"""
        # TODO: add check for valid row, col
        self.pebbles = self.squares[row][col]
        self.squares[row][col] = 0

        while self.pebbles > 0:
            # If end of row 0 has been reached
            if col == self._squareCount - 1 and row == 0:
                row = 1
            # If beginning of row 1 has been reached
            elif col == 0 and row == 1:
                row = 0
            elif row == 0:
                col += 1
            elif row == 1:
                col -= 1

            self.squares[row][col] += 1
            self.pebbles -= 1

    # Assistant Functions #

    def copy(self):
        """ Return a deep copy of the Board for simulation/lookahead"""
        copy_board = Board(self._squareCount, self._pebbleCount)
        copy_board.squares = [list(row) for row in self.squares]
        return copy_board

    def get_squares_per_player(self):
        return self._squareCount

    def get_score(self, player):
        return sum(self.squares[player])

    def __hash__(self):
        num = 1
        for r in self.squares:
            for p in r:
                num *= self._squareCount*self._pebbleCount+1
                num += p
        return num