import pygame as pg
import random
import os
import math
from classes import *
from settings import *
from utils import *
vec = pg.math.Vector2
pg.init()


def main():
    running = True
    grid = HexGrid(SCREEN, 20)
    grid.populate(5)
    s = Shooter()
    while running:
        keys = pg.key.get_pressed()
        if keys[pg.K_RIGHT]:
            s.update(1)
        if keys[pg.K_LEFT]:
            s.update(0)
        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_SPACE:
                    s.shoot()
        for tile in grid.tiles.values():
            if tile.is_occupied():
                if pg.sprite.collide_mask(s.curr_bubble, tile.bubble):
                    s.curr_bubble.vel = vec((0,0))
        if s.curr_bubble.vel.y == 0  and s.state == 2:
            grid.snap_to_tile(s.curr_bubble)
            s.load()
        s.curr_bubble.update()
        SCREEN.blit(BG, (0,0))
        grid.draw(SCREEN)
        s.draw(SCREEN)
        s.curr_bubble.draw(SCREEN)
        pg.display.flip()
        CLOCK.tick(FPS)

main()
pg.quit()
