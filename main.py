import pygame as pg
import random 
import os
import math
from classes import *
from settings import *
from utils import *
pg.init()

     
def main():
    running = True
    grid = HexGrid(SCREEN, 20)
    grid.populate(5)
    while running:
        # keys = pg.key.get_pressed()
        # if keys[pg.K_RIGHT]:
        #     s.update(1)
        # if keys[pg.K_LEFT]:
        #     s.update(0)
        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False
        #     if event.type == pg.KEYDOWN:
        #         if event.key == pg.K_SPACE:
        #             s.shoot()
        #s.curr_bubble.check_collision(bubbles)       
        # if s.curr_bubble.vel.y == 0  and s.state == 2:
        #     grid.snap_to_tile(s.curr_bubble)
        #     s.load()
        SCREEN.blit(BG, (0,0))
        grid.draw(SCREEN)
        #s.draw(SCREEN)
        pg.display.flip()
        CLOCK.tick(FPS)

main()
pg.quit()


