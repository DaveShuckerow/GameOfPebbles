"""
renderer.py
Placeholder for a more advanced renderer.
"""

class Renderer:
    def __init__(self, board):
        pass
    def moveEvent(self, board, playerNumber):
        self.draw(board)
        print("Player {}'s turn.".format(playerNumber))
    def victoryEvent(self, board, playerNumber):
        self.draw(board)
        print("Player {} wins!".format(playerNumber))
    def draw(self, board):
        length = len(board.squares[0])
        split = "#"*(1+length*4)
        for row in board.squares:
            print(split)
            print('# '+' # '.join(map(str,row))+' #')
        print(split)
