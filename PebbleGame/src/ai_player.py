__author__ = "Carlos Lemus (cal0018@auburn.edu)"

from PebbleGame.src.player import Player as Player


class AIPlayer(Player):
    def __init__(self, playerID, mediator, preferred_heuristic=0):
        self.MAX_DEPTH = 3
        self.state_table = dict()

        self.preferred_heuristic = preferred_heuristic
        self.heuristics_list = [self.defensive_heuristic, self.aggressive_heuristic]

        super(AIPlayer, self).__init__(mediator, playerID)

    def play(self):
        best_move = self.max_value(self.mediator.board, float("-inf"), float("inf"))[1]

        self.mediator.set_state(self.playerID, self.playerID, best_move)

    def max_value(self, board, alpha, beta, current_depth=0):
        if self.cutoff_test(board, current_depth):
            if board in self.state_table:
                return self.state_table[board]

            return self.heuristics_list[self.preferred_heuristic](board), None

        v = float("-inf")
        best_branch = 0

        for current_column in range(0, board._squareCount):
            v = max(v, self.min_value(self.result(board, self.playerID % 2, current_column), alpha, beta,
                                      current_depth + 1))

            # if V is higher than the lowest known potential value
            if v >= beta:
                return v, None

            if (v > alpha):
                alpha = v
                best_branch = current_column

        self.state_table[board] = v
        return v, best_branch

    def min_value(self, board, alpha, beta, current_depth=0):
        if self.cutoff_test(board, current_depth):
            if board in self.state_table:
                return self.state_table[board]

            return self.heuristics_list[self.preferred_heuristic](board)

        v = float("inf")

        for current_column in range(0, board._squareCount):
            max_known_value = self.max_value(self.result(board, (self.playerID + 1) % 2, current_column), alpha, beta,
                                             current_depth + 1)

            v = min(v, max_known_value[0])

            # if V is lower than highest known value
            if v <= alpha:
                return v

            beta = min(beta, v)

        return v


    def result(self, board, current_player, column_number):
        board_copy = board.copy()
        board_copy.move(current_player, column_number)

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