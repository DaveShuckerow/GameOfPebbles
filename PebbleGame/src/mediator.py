'''
Mediator.py
by: David Shuckerow (djs0017@auburn.edu) and Carlos Lemus (cal0018@auburn.edu)
date: 11/19/2014

The Mediator class implements the mediator design pattern.
It is responsible for coordinating the Board model, the View of the board, and 
the AI Controller(s) responsible for instructing how to change the board state.
'''
__author__ = "Carlos Lemus, David Shuckerow"
__license__ = "MIT"

from board import Board

class Mediator:
	"""
	Stub for now.
	"""
	def __init__(self):
		self.board = Board(2,2)

	def main(self):
		pass

	def setState(self):
		pass

if __name__ == '__main__':
	Mediator().main()