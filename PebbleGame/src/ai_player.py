__author__ = 'Carlos'

from PebbleGame.src.player import Player as Player


class AIPlayer(Player):
    def __init__(self, mediator):
        self.MAX_DEPTH = 3
        self.state_table = dict()
        super(AIPlayer, self).__init__(mediator)

    def play(self):
        pass

    def terminal_test(self, board):
        return (board.squares[0][0] == 0 and board.squares[0][1] == 0) \
               or (board.squares[1][0] == 0 and board.squares[1][1] == 0)

    def cutoff_test(self, board, depth):
        """
        Determines if the AI should stop exploring the decision tree by checking
        for terminal states, maximum exploration depth, or previous decision knowledge.

        :param board: board containing current state
        :param depth: the maximum depth the decision tree should be explored
        :return: whether the AI should stop exploring the decision tree.
        """
        if self.terminal_test(board):
            return True
        elif depth == self.MAX_DEPTH:
            return True
        elif board in self.state_table:
            return True
        else:
            return False