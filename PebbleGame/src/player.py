"""
The Player class represents a player. This class can be implemented
either with an user input or plugged into an AI engine.
by: David Shuckerow (djs0017@auburn.edu) and Carlos Lemus (cal0018@auburn.edu)
date: 11/26/2014
"""

__author__ = "Carlos Lemus, David Shuckerow"
__license__ = "MIT"

class Player(object):
    def __init__(self, mediator, playerID):
        self.mediator = mediator
        self.playerID = playerID

    def play(self, board):
        # display UI for human player, set state depending on UI choice
        # do AI analysis and select square for AI
        raise NotImplementedError("Mediator.set_state: function not implemented.")
