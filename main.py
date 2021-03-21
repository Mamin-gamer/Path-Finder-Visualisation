"""Imports"""

import pygame as pg     #allows to make a window and put the game processing powers
import numpy as np      #allows to create fast arrays and use fast features like linspace
import os               #allows to switch welcome message from pygame off
os.environ['PYGAME_HIDE_SUPPORT_PROMPT'] = "hide"   #command to stop welcome sign from Pygame to appear

""" constants"""
WIDTH = 800
HEIGHT = 600

WHITE = (255,255,255)
BLACK = (0,0,0)
GREY = (80,80,80)



""" Initialise pygame"""
def initialise_pygame():
    pg.init()
    global WIN
    WIN = pg.display.set_mode((WIDTH, HEIGHT))  #inialises window with set height and width
    pg.display.set_caption('Sorting Algorithms Visualisation')    #gives a name to the window
    display.fill(pg.Color(WHITE))


def main():
    while True:
        check_events()
        pg.display.update()

def check_events():                     #function to track of user exiting the pygame screen
    for event in pg.event.get():
        if event.type == pygame.QUIT:
            pg.quit()


if __name__ == '__main__':
    main()
    
