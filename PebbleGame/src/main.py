#!/usr/bin/python3
"""
main.py

Responsible for running the game as a kivy app.
Contains the control interface logic for the UI.
"""
__author__ = "Carlos Lemus, David Shuckerow"
__license__ = "MIT"

import board as board
import kivy
from kivy.app import App
from kivy.animation import Animation
from kivy.base import EventLoop
EventLoop.ensure_window()
from kivy.clock import Clock
from kivy.graphics import Color
from kivy.graphics import Line
from kivy.graphics import Rectangle
from kivy.properties import NumericProperty
from kivy.properties import ObjectProperty
from kivy.uix.widget import Widget
import random


class PebbleGame(Widget):
    """
    The PebbleGame widget displays a game of the pebble game.

    It includes a display for the game board, and whenever
    a board update event occurs.
    """
    board_renderer = ObjectProperty(None)

    def __init__(self, gameboard=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.board_renderer.game_board = gameboard

    def update(self, row=0, col=0, message=""):
        """
        update the render_board with the latest move.
        """
        self.board_renderer.update(row, col)


class BoardRenderer(Widget):
    """
    Responsible for drawing the board.
    """
    game_board = ObjectProperty(None)
    square_count = NumericProperty(10)
    scale = NumericProperty(20)

    def __init__(self, new_board=None, *args, **kwargs):
        super().__init__(**kwargs)
        #print(new_board)
        if isinstance(new_board, board.Board):
            self.game_board = new_board
        self.bind(game_board=self.on_game_board)
        self.bind(pos=self.render, size=self.render)

    def on_game_board(self, *args):
        if self.game_board is not None:
            self.square_count = self.game_board._squareCount

    def render(self, *args):
        self.canvas.clear()
        if self.game_board is None:
            return
        with self.canvas:
            Color(0.2, 0.4, 0.8, 0.2)
            Rectangle(pos=self.pos,
                      size=self.size)
            Color(0.2, 0.4, 0.8, 1.)
            Line(rectangle=(self.pos+self.size), width=2)
            print(self.x, self.y, self.width, self.height, self.square_count)
            Line(points=[self.x, self.y+self.height/2, 
                         self.x+self.width, self.y+self.height/2], 
                 width=1)
            for i in range(1,self.square_count):
                lx = self.x + self.scale*i
                Line(points=[lx, self.y, lx, self.y+self.height], width=1)
            print(self.canvas)
        self.canvas.ask_update()
        print("Making pebbles!")
        pebble_count = self.game_board._pebbleCount
        squares = []
        self.clear_widgets()
        def create_square(x, y):
            sq = Square(pos=(x, y))
            if len(squares) > 0:
                squares[-1].next = sq
            squares.append(sq)
            self.add_widget(sq)
            for j in range(pebble_count):
                p = Pebble(current_square=sq)
                p.offset_x = random.random()*(self.scale-p.radius*3) + p.radius
                p.offset_y = random.random()*(self.scale-p.radius*3) + p.radius
                p.x = sq.x + p.offset_x
                p.y = sq.y + p.offset_y
                self.add_widget(p)
        for i in range(self.square_count-1, -1, -1):
            create_square(self.x+self.scale*i, self.y+self.height/2)
        # create the top squares, also fill with pebbles.
        for i in range(self.square_count):
            create_square(self.x+self.scale*i, self.y)
        squares[-1].next = squares[0]
        print("Pebbles made!")

    def update(self, row=0, col=0):
        print(dir(self.canvas))
        #self.render()


class Square(Widget):
    """
    Data class whose position and size are used to tell Pebbles where to go 
    on the gameboard.
    """
    next = ObjectProperty(None)


class Pebble(Widget):
    """
    The Pebble to draw on the board.
    """
    current_square = ObjectProperty(None)
    offset_x = NumericProperty(0)
    offset_y = NumericProperty(0)
    radius = NumericProperty(8)
    
    def move(self, distance):
        if distance <= 0:
            return
        moveAnim = Animation(duration=0)

        while distance > 0:
            moveAnim += Animation(pos=(self.offset_x+self.current_square.x,
                                       self.parent.y+self.parent.height/2),
                                  t='in_out_circ',
                                  duration=0.3)
            self.current_square = self.current_square.next
            moveAnim += Animation(pos=(self.offset_x+self.current_square.x,
                                       self.parent.y+self.parent.height/2),
                                  t='in_out_circ',
                                  duration=0.3)
            moveAnim += Animation(pos=(self.offset_x+self.current_square.x,
                                       self.offset_y+self.current_square.y),
                                  t='in_out_circ',
                                  duration=0.3)
            distance -= 1
        moveAnim.start(self)

    def on_touch_down(self, touch):
        if self.collide_point(touch.x, touch.y):
            self.move(3)



class PebbleApp(App):
    """
    Application that displays the PebbleGame.
    """
    def build(self):
        pb = PebbleGame(gameboard=board.Board(10,4))
        return pb


if __name__=="__main__":
    PebbleApp().run()