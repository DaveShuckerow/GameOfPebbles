__author__ = 'Carlos'

from PebbleGame.src.player import Player as Player


class AIPlayer(Player):
    def __init__(self, playerID, mediator, preferred_heuristic=0):
        self.MAX_DEPTH = 3
        self.state_table = dict()

        self.preferred_heuristic = preferred_heuristic
        self.heuristics_list = [self.defensive_heuristic, self.aggressive_heuristic]

        super(AIPlayer, self).__init__(mediator, playerID)

    def play(self):
        pass

    def result(self, board, column_number):
        board_copy = board.copy()
        board_copy.move(self.playerID, column_number)

        return board_copy

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

    def defensive_heuristic(self, board):
        ''' returns value of players right-most square as a heuristic value '''
        right_sq_col = 0
        if self.playerID != 0:
            right_sq_col = board._squareCount - 1

        return board.squares[self.playerID][right_sq_col]

    def aggressive_heuristic(self, board):
        ''' returns value of players left-most square as a heuristic value '''
        left_sq_col = 0
        if self.playerID == 0:
            left_sq_col = board._squareCount - 1

        return board.squares[self.playerID][left_sq_col]