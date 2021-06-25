import pygame as pg
import math
import numpy as np
pg.init()

WIDTH = 315
HEIGHT = 500
SCREEN = pg.display.set_mode((WIDTH,HEIGHT))
CLOCK = pg.time.Clock()
FPS = 60
BLACK = (0,0,0)
WHITE = (255,255,255)
RED = (255,0,0)

def draw_reg_polygon(surface, color, num_vertices, radius, pos):
    n,r = num_vertices,radius
    x,y = pos
    vertices = [(x + r*math.cos(2*math.pi*(i/n)), y + r*math.sin(2*math.pi*(i/n))) for i in range(n)]
    pg.draw.polygon(surface, color, vertices, 1)
    return vertices

def hex_tiling(surface, radius, color):
    width = surface.get_width()
    height = surface.get_height()
    hex_width = math.sqrt(3) * radius
    hex_height = 2 * radius 
    y_spacing = hex_width
    x_spacing = 0.75 * hex_height
    for i in range(int(width//x_spacing)):
        if i % 2 == 0:
                offset = radius
        else:
            offset = 0
        for j in range(int(height//y_spacing)):
            draw_reg_polygon(surface, color, 6, 15, (i*x_spacing+radius, j*y_spacing+offset))

            
    
    
def main():
    running = True
    SCREEN.fill(BLACK)
    hex_tiling(SCREEN, 15, RED)
    pg.display.flip()
    while running:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False
        
main()
pg.quit()
    
    