"""
player.py
Placeholder for a more advanced player.
"""

class Player:
    def __init__(self, playerID):
        self.playerID = playerID
    def play(self, board):
        print("You are player {}.".format(self.playerID))
        myMove = input("Select a square to move from: ")
        return int(myMove)
