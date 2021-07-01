import pygame as pg
import math
import os
from classes import *
from settings import *

WIDTH = 330
HEIGHT = 500
SCREEN = pg.display.set_mode((WIDTH, HEIGHT))

def draw_hexagon(center, radius, surface, color):
    x,y = center[0],center[1]
    p1 = (x, y+radius)
    p2 = (x+radius*math.cos(math.radians(30)), y+radius*math.sin(math.radians(30)))
    p3 = (x+radius*math.cos(math.radians(30)), y-radius*math.sin(math.radians(30)))
    p4 = (x, y-radius)
    p5 = (x-radius*math.cos(math.radians(30)), y-radius*math.sin(math.radians(30)))
    p6 = (x-radius*math.cos(math.radians(30)), y+radius*math.sin(math.radians(30)))
    points = (p1,p2,p3,p4,p5,p6)
    pg.draw.polygon(surface, color, points, 1)

def tile_surface(surface, radius):
    width = surface.get_width()
    height = surface.get_height()
    hex_width  = math.sqrt(3) * radius
    hex_height = 2 * radius
    horizontal_spacing = hex_width
    veritcal_spacing = hex_height * 0.75
    rows = int(height//veritcal_spacing)
    cols = int(width//horizontal_spacing)
    bubbles = pg.sprite.Group()
    tiles = {}
    for i in range(rows):
        if i % 2 == 0:
            offset = hex_width//2
        else:
            offset = 0
        for j in range(cols):
            center = (j*horizontal_spacing+hex_width//2+offset, i*veritcal_spacing+radius)
            draw_hexagon(center, radius, surface, (255,0,0))
            b = Bubble(center, (0,0), color=random.choice(COLORS))
            bubbles.add(b)
            tiles[(j,i)] = HexTile(center, b)
    return bubbles, tiles

def test():
    running = True
    bubbles, tiles = tile_surface(SCREEN, 20)
    pg.display.flip()
    while running:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False
        bubbles.update()
        bubbles.draw(SCREEN)
        pg.display.flip()
test()
pg.quit()
