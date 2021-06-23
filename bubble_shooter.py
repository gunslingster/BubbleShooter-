import pygame as pg
import random 
import os
import math
pg.init()
vec = pg.math.Vector2

# Set global variables
PROJECT_PATH = os.path.dirname(os.path.abspath(__file__))
BUBBLE_PATH = os.path.join(PROJECT_PATH, 'Bubbles')
WIDTH = 300
HEIGHT = 500
SCREEN = pg.display.set_mode((WIDTH,HEIGHT))
CLOCK = pg.time.Clock()
FPS = 60
BG = pg.transform.scale(pg.image.load('background.png'), (WIDTH, HEIGHT))
WHITE = (255,255,255)
BLACK = (0,0,0)
RED = (216,0,0)
GREEN = (216,0,0)
BLUE  = (216,0,0)
PINK = (255,182,193)
PURPLE = (216,0,216)
YELLOW = (216,216,0)
COLORS = [RED,GREEN,BLUE,PINK,PURPLE,YELLOW]

class Bubble(pg.sprite.Sprite):
    def __init__(self, pos=(WIDTH//2, HEIGHT-50), vel=(10,-5), color=RED, size=(30,30)):
        super().__init__()
        self.pos = vec(pos)
        self.vel = vec(vel)
        self.color = color
        if color == RED:
            self.image = pg.transform.scale(pg.image.load(os.path.join(BUBBLE_PATH, 'red.png')), size)
        elif color == GREEN:
            self.image = pg.transform.scale(pg.image.load(os.path.join(BUBBLE_PATH, 'green.png')), size)
        elif color == BLUE:
            self.image = pg.transform.scale(pg.image.load(os.path.join(BUBBLE_PATH, 'neonBlue.png')), size)
        elif color == PINK:
            self.image = pg.transform.scale(pg.image.load(os.path.join(BUBBLE_PATH, 'Violet.png')), size)
        elif color == YELLOW:
            self.image = pg.transform.scale(pg.image.load(os.path.join(BUBBLE_PATH, 'Yellow.png')), size)
        elif color == PURPLE:
            self.image = pg.transform.scale(pg.image.load(os.path.join(BUBBLE_PATH, 'darkBlue.png')), size)
        else:
            self.image = pg.transform.scale(pg.image.load(os.path.join(BUBBLE_PATH, 'red.png')), size)
            
        self.rect = self.image.get_rect()
        self.rect.center = self.pos
        
    def update(self):
        self.pos.x += self.vel.x
        self.pos.y += self.vel.y
        if self.pos.x - 15 <= 0:
            self.vel.x = -self.vel.x
        if self.pos.x + 15 >= WIDTH:
            self.vel.x = -self.vel.x
        if self.pos.y - 15 <= 0:
            self.vel.x = 0
            self.vel.y = 0
            self.pos.y = 15
        self.rect.center = self.pos
    
    def check_collision(self, bubbles):
        for bubble in bubbles:
            if bubble != self:
                if pg.sprite.collide_mask(self, bubble):
                    loc = pg.sprite.collide_mask(self, bubble)
                    print('collide')
                    self.vel = vec(0,0)
    
class Shooter():
    def __init__(self):
        self.angle = 90
        self.start = (WIDTH//2, HEIGHT)
        self.end = (WIDTH//2 + 50*math.cos(math.radians(self.angle)), HEIGHT - 50*math.sin(math.radians(self.angle)))
        self.state = 1
        self.load()
    
    def update(self, cw):
        if cw:
            self.angle -= 3
        else:
            self.angle += 3
        if self.angle < 5:
            self.angle = 5
        if self.angle > 175:
            self.angle = 175
        self.end = (WIDTH//2 + 50*math.cos(math.radians(self.angle)), HEIGHT - 50*math.sin(math.radians(self.angle)))
        if self.state == 1:
            self.curr_bubble.pos = vec(self.end)
    
    def load(self):
        self.curr_bubble = Bubble(pos=self.end, vel=(0,0), color=random.choice(COLORS))
        self.state = 1
    
    def shoot(self):
        if self.state == 1:
            self.curr_bubble.vel = vec(10*math.cos(math.radians(self.angle)), -10*math.sin(math.radians(self.angle)))
        self.state = 2
       
    def draw(self):
        pg.draw.line(SCREEN, RED, self.start, self.end, 5)
        
def main():
    running = True
    s = Shooter()
    bubbles = pg.sprite.Group()
    bubbles.add(s.curr_bubble)
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


