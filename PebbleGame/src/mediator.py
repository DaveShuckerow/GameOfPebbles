'''
Mediator.py
by: David Shuckerow (djs0017@auburn.edu) and Carlos Lemus (cal0018@auburn.edu)
date: 11/26/2014
'''
__author__ = "Carlos Lemus, David Shuckerow"
__license__ = "MIT"


class Mediator(object):
    """
    The Mediator abstract class implements the mediator design pattern.
    It is responsible for coordinating the Board model, the View of the board, and
    the AI Controller(s) responsible for instructing how to change the board state.

    Any Mediator must at least have a set_state and a update_ui function implemented.
    """

    def __init__(self, game_board, user_interface):
        raise NotImplementedError("Mediator.__init__: function not implemented.")

    def set_state(self, player, row, col):
        """
        :param row: row to move from.
        :param col: column to move from.
        :param player: the number of the player (integer 0 or 1)
        """
        raise NotImplementedError("Mediator.set_state: function not implemented.")

    def update_ui(self):
        raise NotImplementedError("Mediator.update_ui: function not implemented.")