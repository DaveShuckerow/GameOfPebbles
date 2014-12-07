"""
board_mediator.py
by: Carlos Lemus (cal0018@auburn.edu) and David Shuckerow (djs0017@auburn.edu)
date: 11/26/2014
"""
__author__ = "Carlos Lemus, David Shuckerow"
__license__ = "MIT"

from PebbleGame.src.mediator import Mediator as Mediator


class BoardMediator(Mediator):
    """ Board implementation of Mediator abstract class """

    def __init__(self, game_board, user_interface):
        self.board = game_board
        self.ui = user_interface

    def main(self):
        """ Filler """
        pass

    def set_state(self, player, row, col):
        """Validate the player and square combination. Move if valid """
        if self.validate_move(player, row):
            self.board.move(row, col)
            self.ui.update(player, row, col)
            return True
        else:
            return False

    def validate_move(self, player, row):
        """
        :return: whether player is playing on its assigned row.
        """
        return (player == 0 and row == 0) or (player == 1 and row == 1)

    def update_ui(self):
        """ currently stub for UI function """
        pass


if __name__ == '__main__':
    Mediator().main()