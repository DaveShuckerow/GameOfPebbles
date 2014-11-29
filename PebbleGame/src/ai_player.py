__author__ = 'Carlos'

from PebbleGame.src.player import Player as Player


class AIPlayer(Player):
    def __init__(self, mediator):
        super(AIPlayer, self).__init__(mediator)

    def play(self):
        pass

    def terminal_test(self, board):
        return (board.squares[0][0] == 0 and board.squares[0][1] == 0) \
               or (board.squares[1][0] == 0 and board.squares[1][1] == 0)