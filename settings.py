import pygame as pg
import os

# Set global variables
vec = pg.math.Vector2
PROJECT_PATH = os.path.dirname(os.path.abspath(__file__))
BUBBLE_PATH = os.path.join(PROJECT_PATH, 'Bubbles')
WIDTH = 315
HEIGHT = 500
SCREEN = pg.display.set_mode((WIDTH,HEIGHT))
CLOCK = pg.time.Clock()
FPS = 60
BG = pg.transform.scale(pg.image.load('background.png'), (WIDTH, HEIGHT))
WHITE = (255,255,255)
BLACK = (0,0,0)
RED = 'red'
GREEN = 'green'
BLUE  = 'blue'
PINK = 'pink'
PURPLE = 'purple'
YELLOW = 'yellow'
COLORS = [RED,GREEN,BLUE,PINK,PURPLE,YELLOW]

