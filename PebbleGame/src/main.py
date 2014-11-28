#!/usr/bin/python3

import kivy
from kivy.app import App
from kivy.uix.widget import Widget

class PebbleGame(Widget):
    pass

class PebbleApp(App):
    def build(self):
        return PebbleGame()

if __name__=="__main__":
    PebbleApp().run()