# tween_test.py - a script for testing pytween.py
# Copyright (c) 2012 Carson J. Q. Farmer
# Module is based on examples from Michael Aufreiter's Tween.lib library

from pyprocessing import *
from pytween import Tween

class MovingObject:

    def __init__(self, x, y, tx, ty):
        self.x = x
        self.y = y
        self.tx = tx
        self.ty = ty
        self.blue_level = 255
        self.r = 5
        self.tweens = []
        self.tweens.append(Tween(self, "x", Tween.strongEaseInOut, x, tx, 2))
        self.tweens.append(Tween(self, "y", Tween.bounceEaseInOut, y, ty, 2))
        self.tweens.append(Tween(self, "blue_level", Tween.strongEaseInOut, 
            255, 0, 2))
        self.tweens.append(Tween(self, "r", Tween.strongEaseInOut, 
            5, 30, 2))
        self.restart()
    
    def update(self):
        for t in self.tweens:
            t.tick()
  
    def draw(self):
        noStroke()
        fill(123, 211, self.blue_level)
        ellipse(self.x, self.y, self.r, self.r)
  
    def restart(self):
        for t in self.tweens:
            t.start()

def setup():
    size(400, 150)
    smooth()
    frameRate(50)
    global mo
    mo = MovingObject(50, 30, 360, 130)

def draw():
    fill(255, 255, 255, 20)
    rect(0, 0, width, height)
    global mo
    mo.update()
    mo.draw()

def mousePressed():
    mo.restart()
  
if __name__ == '__main__':
    import sys
    run()

