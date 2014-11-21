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
    _ROW_DIRECTIONS = [-1, 1]

    def __init__(self, n, p):
        self._squareCount, self._pebbleCount = n, p
        self.squares = [[p for _ in range(2)] for _ in range(n)]

    def move(self, playerNumber, squareNumber):
        """
        Performs a move on the selected square.
        Return whether the move is legal.
        """
        row, col = playerNumber, squareNumber
        if playerNumber == 0:
            col = self._squareCount - squareNumber - 1
        if self.squares[row][col] == 0:
            return False
        #print(self.squares, row, col)
        pebbles = self.squares[row][col]
        self.squares[row][col] = 0
        while pebbles > 0:
            col +=Board. _ROW_DIRECTIONS[row]
            if col < 0 or col >= self._squareCount:
                row = (row+1)%2
                col += Board._ROW_DIRECTIONS[row]
            pebbles -= 1
            self.squares[row][col] += 1
        return True

    def copy(self):
        """ Return a deep copy of the Board for simulation/lookahead"""
        copyBoard = Board(self._squareCount, self._pebbleCount)
        copyBoard.squares = [list(row) for row in self.squares]
        return copyBoard

    def getScore(self, playerNumber):
        """
        :param player:
        The score of a player is the sum quantity of pebbles in a player's own
        row.
        """
        return sum(self.squares[playerNumber])

    def gameOver(self):
        """
        Determine if the game is over or not.
        The game is over when one player has a score of 0.
        """
        for i in range(2):
            if self.getScore(i) == 0:
                return True
        return False
