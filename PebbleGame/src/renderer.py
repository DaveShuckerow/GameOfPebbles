"""
renderer.py
Placeholder for a more advanced renderer.
"""

class Renderer:
    def __init__(self, board):
        self.draw(board)
    def moveEvent(self, board):
        self.draw(board)
    def victoryEvent(self, board):
        self.draw(board)
    def draw(self, board):
        length = len(board.squares[0])
        split = "#"*(2+length*2)
        for row in board.squares:
            print(split)
            print('#'+'#'.join(map(str,row))+'#')
        print(split)
