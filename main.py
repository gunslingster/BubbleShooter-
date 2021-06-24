import pygame as pg
import random 
import os
import math
from classes import *
from settings import *
pg.init()
     
def main():
    running = True
    s = Shooter()
    b = BubbleGrid(30 ,(WIDTH, HEIGHT//2))
    bubbles = pg.sprite.Group()
    bubbles.add(s.curr_bubble)
    bubbles.add(b.bubbles)
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
        
        s.curr_bubble.check_collision(bubbles)       
        if s.curr_bubble.vel.y == 0  and s.state == 2:
            snap_to_grid(s.curr_bubble)
            s.load()
            bubbles.add(s.curr_bubble)
        SCREEN.blit(BG, (0,0))
        bubbles.update()
        bubbles.draw(SCREEN)
        s.draw()
        pg.display.flip()
        CLOCK.tick(FPS)

main()
pg.quit()


