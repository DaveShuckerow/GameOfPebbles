__author__ = "Carlos Lemus (cal0018@auburn.edu)"

from PebbleGame.src.player import Player as Player

DEFENSIVE = 0
AGGRESSIVE = 1
TOTAL = 2
ANDOR = 3

class AIPlayer(Player):
    def __init__(self, playerID, mediator, preferred_heuristic=0, play_strategy=0, max_depth=20):
        self.play_strategy = play_strategy
        self.plan = dict()

        self.max_depth = max_depth
        self.state_table = dict()

        self.preferred_heuristic = preferred_heuristic
        self.heuristics_list = [self.defensive_heuristic, self.aggressive_heuristic, self.total_heuristic]

        super(AIPlayer, self).__init__(mediator, playerID)

    def play(self):
        best_move = 0
        if self.play_strategy == 0:
            self.state_table = dict()
            best_move = self.max_value(self.mediator.board, float("-inf"), float("inf"))[1]
        else:
            self.plan = dict()
            path = dict()
            self.or_search(self.mediator.board, path)

            best_move = self.plan[self.mediator.board]

        self.mediator.set_state(self.playerID, self.playerID, best_move)


    def max_value(self, board, alpha, beta, current_depth=0):
        if self.cutoff_test(board, current_depth):
            if board in self.state_table:
                return self.state_table[board]
            return self.heuristics_list[self.preferred_heuristic](board), None

        self.state_table[board] = (float("-inf"), None)

        v = float("-inf")
        best_branch = 0

        for current_column in range(0, board._squareCount):
            if board.squares[self.playerID][current_column] == 0:
                continue

            potential_max_value = self.min_value(self.result(board, self.playerID, current_column), alpha, beta,
                                                 current_depth + 1)

            v = max(v, potential_max_value)

            # if V is higher than the lowest known potential value
            if v >= beta:
                return v, None

            if (v > alpha):
                alpha = v
                best_branch = current_column

        self.state_table[board] = (v, best_branch)
        return v, best_branch

    def min_value(self, board, alpha, beta, current_depth=0):
        if self.min_cutoff_test(board, current_depth):
            return self.heuristics_list[self.preferred_heuristic](board)

        v = float("inf")

        for current_column in range(0, board._squareCount):
            if board.squares[self.playerID][current_column] == 0:
                continue

            potential_min_value = self.max_value(self.result(board, (self.playerID + 1) % 2, current_column), alpha,
                                                 beta, current_depth + 1)

            v = min(v, potential_min_value[0])

            # if V is lower than highest known value
            if v <= alpha:
                return v

            beta = min(beta, v)

        return v

    def or_search(self, board, path):
        # print("OR_SEARCHing: " + str(board.squares))

        if self.victory_test(board):
            return True

        # watch for loops
        if hash(board) in path:
            return False

        path[hash(board)] = True

        for column in range(0, board._squareCount):
            if board.squares[self.playerID][column] == 0:
                continue

            valid_in_plan = self.and_search(self.result(board, self.playerID, column), path)
            if valid_in_plan:
                self.plan[board] = column
                return True

        return False

    def and_search(self, board, path):
        # print("AND_SEARCHing: " + str(board.squares))
        for column in range(0, board._squareCount):
            if board.squares[(self.playerID + 1) % 2][column] == 0:
                continue
            # is there at least one move by the opponent that will lead to victory?
            # >>or is there at least one move by the opponent that will lead to loss?
            valid_in_plan = self.or_search(self.result(board, (self.playerID + 1) % 2, column), path)
            if valid_in_plan:
                return True

        return False


    def result(self, board, current_player, column_number):
        board_copy = board.copy()
        board_copy.move(current_player, column_number)

        return board_copy

    def terminal_test(self, board):
        return sum(board.squares[0]) == 0 or sum(board.squares[1]) == 0

    def victory_test(self, board):
        # sum of opponent's squares == 0
        return sum(board.squares[(self.playerID + 1) % 2]) == 0

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
        elif depth == self.max_depth:
            return True
        elif board in self.state_table:
            return True
        else:
            return False

    def min_cutoff_test(self, board, depth):
        """
        Determines if the AI should stop exploring the decision tree by checking
        for terminal states, maximum exploration depth, or previous decision knowledge.

        :param board: board containing current state
        :param depth: the maximum depth the decision tree should be explored
        :return: whether the AI should stop exploring the decision tree.
        """
        if self.terminal_test(board):
            return True
        elif depth == self.max_depth:
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

    def total_heuristic(self, board):
        return board.squares[self.playerID][0] + board.squares[self.playerID][1]

    # CONFIG

    def set_max_search_depth(self, depth):
        self.max_depth = depth
