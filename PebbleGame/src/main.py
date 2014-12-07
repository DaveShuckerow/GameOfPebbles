#!/usr/bin/python3
"""
main.py

Responsible for running the game as a kivy app.
Contains the control interface logic for the UI.
"""
__author__ = "Carlos Lemus, David Shuckerow"
__license__ = "MIT"

print(__package__)
import PebbleGame.src.ai_player as ai_player
import PebbleGame.src.board as board
import PebbleGame.src.board_mediator as board_mediator
import kivy
from kivy.app import App
from kivy.animation import Animation
from kivy.base import EventLoop
EventLoop.ensure_window()
from kivy.core.window import Window
from kivy.clock import Clock
from kivy.graphics import Color
from kivy.graphics import Line
from kivy.graphics import Rectangle
from kivy.properties import BoundedNumericProperty
from kivy.properties import ListProperty
from kivy.properties import NumericProperty
from kivy.properties import ObjectProperty
import kivy.resources as resources
from kivy.uix.screenmanager import Screen
from kivy.uix.screenmanager import ScreenManager
from kivy.uix.widget import Widget
import random

PEBBLE_ANIM_SPEED = 0.5

class PebbleGame(Widget):
    """
    The PebbleGame widget displays a game of the pebble game.

    It includes a display for the game board, and whenever
    a board update event occurs.
    """
    board_renderer = ObjectProperty(None)
    mediator = ObjectProperty(None)
    player = NumericProperty(0)
    p0_score = NumericProperty(0)
    p1_score = NumericProperty(0)
    ai = ListProperty([None, None])
    mode = NumericProperty(0)
    cont_button = ObjectProperty(None)
    quit_button = ObjectProperty(None)

    def __init__(self, gameboard=None, mediator=None, ai0=None, ai1=None, mode=0, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.board_renderer.game_board = gameboard
        self.p0_score = gameboard.get_score(0)
        self.p1_score = gameboard.get_score(1)
        self.board_renderer.player_change(self, -1)
        self.mode = mode
        self.ai = [ai0, ai1]
        self.mediator = mediator
        self.mediator.ui = self
        self.player = 0
        # Initialize the coloring:
        if ai0 is None:
            Clock.schedule_once((lambda x: self.board_renderer.player_change(self, self.player)), 1)
        if ai0 is not None and ai1 is not None:
                self.quit_button.opacity = 1.0
                self.quit_button.disabled = False
        if self.mode == 0:
            Clock.schedule_once(lambda dt: self.ai_move(), 3)
        else:
            self.cont_button.opacity = 1.0
            self.cont_button.disabled = False

    def update(self, player, row, col, message=""):
        """
        update the render_board with the latest move.
        """
        time_delay = self.board_renderer.update(player, row, col)+PEBBLE_ANIM_SPEED
        self.board_renderer.player_change(self, -1)
        Clock.schedule_once((lambda x: self.board_renderer.player_change(self, self.player, self.ai[self.player] is not None)), time_delay)
        def set_score(dt=None):
            self.p0_score = self.board_renderer.game_board.get_score(0)
            self.p1_score = self.board_renderer.game_board.get_score(1)
        Clock.schedule_once(set_score, time_delay)
        if self.mode == 0:
            Clock.schedule_once(lambda dt: self.ai_move(), time_delay)

    def make_move(self, row, col):
        print("Player {}'s move: {} {}".format(self.player, row, col))
        if self.mediator.set_state(self.player, row, col):
            self.player = (self.player+1)%2
            #move = input("Player {}, select your row col move: ".format(self.player))
            #row, col = map(int, move.split())
            print("Moving...")

    def ai_move(self):
        if self.board_renderer.game_over():
            self.quit_button.disabled = False
            self.quit_button.opacity = 1.0
        elif self.ai[self.player] is not None:
            self.ai[self.player].play()
            self.player = (self.player+1)%2

    def end(self):
        self.parent.game_over()

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
        self.player = 0

    def game_over(self):
        return self.game_board.get_score(0) == 0 or self.game_board.get_score(1) == 0

    def on_game_board(self, instance, value):
        if self.game_board is not None:
            self.square_count = self.game_board._squareCount

    def player_change(self, instance, value, robot=False):
        self.player = value
        for child in self.children:
            if hasattr(child, "row"):
                if child.row == value and not robot and not self.game_over():
                    child.min_intensity = 0.2
                else:
                    child.min_intensity = 0


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
        def create_square(x, y, row, col):
            """Factory for making squares."""
            sq = Square(pos=(x, y), size=(self.scale,self.scale), row=row, col=col)
            Window.bind(mouse_pos=sq.on_mouse_pos)
            Clock.schedule_interval(sq.fade, 0.05)
            print(row, col)
            if len(squares) > 0:
                squares[-1].next = sq
            squares.append(sq)
            self.add_widget(sq)
            for j in range(self.game_board.squares[row][col]):
                p = Pebble(current_square=sq)
                p.offset_x = random.random()*(self.scale-p.radius*3) + p.radius
                p.offset_y = random.random()*(self.scale-p.radius*3) + p.radius
                p.x = sq.x + p.offset_x
                p.y = sq.y + p.offset_y
                self.add_widget(p)
            return sq
        # Top squares
        for i in range(self.square_count):
            create_square(self.x+self.scale*i, self.y+self.height/2, 0, i)
        # bottom squares
        for i in range(self.square_count-1, -1, -1):
            create_square(self.x+self.scale*i, self.y, 1, i)
        squares[-1].next = squares[0]
        print("Pebbles made!")
        self.player_change(self, self.player)

    def update(self, player, row, col):
        # Move all the pebbles in a given square.
        print(self.game_board.squares)
        move_count = 1
        for child in self.children:
            #print(child)
            if hasattr(child, "current_square"): # We have a pebble in a square.
                #print(child.current_square.row, child.current_square.col, move_count)
                if child.current_square.row == row and child.current_square.col == col:
                    child.move(move_count)
                    move_count += 1
        return move_count*PEBBLE_ANIM_SPEED
        #self.render()


class Square(Widget):
    """
    Data class whose position and size are used to tell Pebbles where to go 
    on the gameboard.
    """
    row = NumericProperty(0)
    col = NumericProperty(0)
    play_intensity = NumericProperty(0.2) # How bright to make the square glow!
    min_intensity = NumericProperty(0.2)
    next = ObjectProperty(None)
    player = NumericProperty(0)

    def on_mouse_pos(self, *args):
        mx, my = Window.mouse_pos
        if self.min_intensity != 0:
            self.min_intensity = 0.2
            if self.collide_point(mx, my):
                self.min_intensity = 0.4

    def on_player(self, instance, value):
        pass

    def on_touch_down(self, touch):
        if self.collide_point(touch.x, touch.y) and self.play_intensity > 0:
            self.play_intensity = 1.2
            self.parent.parent.make_move(self.row, self.col)

    def fade(self, dt=None):
        self.play_intensity = max(self.play_intensity-dt, self.min_intensity)


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
                                       self.parent.y+self.parent.height/2-self.radius),
                                  t='in_out_circ',
                                  duration=0.333*PEBBLE_ANIM_SPEED)
            self.current_square = self.current_square.next
            moveAnim += Animation(pos=(self.offset_x+self.current_square.x,
                                       self.parent.y+self.parent.height/2-self.radius),
                                  t='in_out_circ',
                                  duration=0.334*PEBBLE_ANIM_SPEED)
            moveAnim += Animation(pos=(self.offset_x+self.current_square.x,
                                       self.offset_y+self.current_square.y),
                                  t='in_out_circ',
                                  duration=0.333*PEBBLE_ANIM_SPEED)
            distance -= 1
        moveAnim.start(self)

    """def on_touch_down(self, touch):
        if self.collide_point(touch.x, touch.y):
            self.move(3)"""


class PebbleTitle(Screen):
    pebble_count = NumericProperty(2)
    square_count = NumericProperty(2)
    ply_count = NumericProperty(10)
    run_modes = ListProperty(["Run", "Step"])
    run_mode = BoundedNumericProperty(0, min=0, max=1)
    player_modes = ListProperty(["Human", "Aggressive \u0391\u0392", "Defenseive \u0391\u0392", "Total \u0391\u0392", "And-Or Search"])
    player0_mode = BoundedNumericProperty(1, min=0, max=3)
    player1_mode = BoundedNumericProperty(2, min=0, max=3)

    def play_game(self, *args):
        gameboard = board.Board(self.square_count, self.pebble_count)
        med = board_mediator.BoardMediator(gameboard, None)
        ai0, ai1 = None, None
        ais = [ai_player.AGGRESSIVE, ai_player.DEFENSIVE, ai_player.TOTAL]
        if self.player0_mode > 0:
            ai0 = ai_player.AIPlayer(0, med, ais[self.player0_mode-1])
            ai0.MAX_DEPTH = self.ply_count
        if self.player1_mode > 0:
            ai1 = ai_player.AIPlayer(1, med, ais[self.player1_mode-1])
            ai1.MAX_DEPTH = self.ply_count
        mode = 0
        if self.player0_mode != 0 and self.player1_mode != 0:
            mode = self.run_mode
        pb = PebbleGame(gameboard=gameboard, mediator=med, ai0=ai0, ai1=ai1, mode=mode)
        next_screen = self.manager.get_screen(self.manager.next())
        next_screen.setup(pb)
        self.manager.transition.direction = "left"
        self.manager.current = self.manager.next()

    def inc_player0(self, *args):
        self.player0_mode = self.player0_mode+1 if self.player0_mode < 3 else 0

    def inc_player1(self, *args):
        self.player1_mode = self.player1_mode+1 if self.player1_mode < 3 else 0

    def inc_run_mode(self, *args):
        self.run_mode = self.run_mode+1 if self.run_mode < 1 else 0

    
class PebbleScreen(Screen):
    def setup(self, game):
        self.clear_widgets()
        game.size_hint = (1, 1)
        self.add_widget(game)
    def game_over(self, *args):
        self.manager.transition.direction = "right"
        self.manager.current = self.manager.previous()


class PebbleApp(App):
    """
    Application that displays the PebbleGame.
    """
    def build(self):
        sm = ScreenManager()
        pt = PebbleTitle()
        pt.name="Main Menu"
        sm.add_widget(pt)
        ps = PebbleScreen()
        ps.name = "Pebble Game!"
        sm.add_widget(ps)
        return sm


def main():
    import os
    print(os.listdir('.'))
    resources.resource_add_path("./PebbleGame/data/")
    print(os.listdir('./PebbleGame/data/'))
    print("Lucida Console: "+resources.resource_find("lucon.ttf"))
    PebbleApp().run()

if __name__=="__main__":
    main()