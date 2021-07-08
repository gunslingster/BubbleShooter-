import pygame as pg
import math
vec = pg.math.Vector2

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


