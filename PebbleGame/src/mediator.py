"""
Mediator.py
by: David Shuckerow (djs0017@auburn.edu) and Carlos Lemus (cal0018@auburn.edu)
date: 11/19/2014

The Mediator class implements the mediator design pattern.
It is responsible for coordinating the Board model, the View of the board, and
the AI Controller(s) responsible for instructing how to change the board state.
"""
__author__ = "Carlos Lemus, David Shuckerow"
__license__ = "MIT"

import board, renderer, player


class Mediator:
    """
    Stub for now.
    """
    def __init__(self):
        self.gameBoard = board.Board(2, 2)
        self.render = renderer.Renderer(self.gameBoard.copy())

    def main(self):
        """Main Game Loop"""
        players = [player.Player(i) for i in range(2)]
        self.gameBoard = board.Board(2,2)
        gameOver = False
        currentPlayer = 0
        while not gameOver:
            self.render.moveEvent(self.gameBoard.copy(), currentPlayer)
            nextMove = players[currentPlayer].play(self.gameBoard.copy())
            while not self.setState(currentPlayer, nextMove):
                nextMove = players[currentPlayer].play(self.gameBoard.copy())
            gameOver = self.gameBoard.gameOver()
            currentPlayer = (currentPlayer + 1)%2
        self.render.victoryEvent(self.gameBoard.copy(), currentPlayer)

    def setState(self, playerNumber, squareNumber):
        """Set the state of the game board.
        
        :param player: the number of the player (integer 0 or 1)
        :param square: the square from which to begin the move (in range(0,n))
        Validate the player and square to be valid and then move.
        If the move is not valid, then return False.
        If the move is valid, then attempt to perform the move and return
        whether or not the move was legal.
        """
        return self.gameBoard.move(playerNumber, squareNumber)

if __name__ == '__main__':
    Mediator().main()
