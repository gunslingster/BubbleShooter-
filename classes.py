import pygame as pg
import random 
import os
import math
from settings import *
pg.init()

class Bubble(pg.sprite.Sprite):
    def __init__(self, pos=(WIDTH//2, HEIGHT-50), vel=(10,-5), color='red', size=(30,30)):
        super().__init__()
        self.pos = vec(pos)
        self.vel = vec(vel)
        self.color = color
        self.size = size
        self.radius = self.size[0]//2
        if color == 'red':
            self.image = pg.transform.scale(pg.image.load(os.path.join(BUBBLE_PATH, 'red.png')), size)
        elif color == 'green':
            self.image = pg.transform.scale(pg.image.load(os.path.join(BUBBLE_PATH, 'green.png')), size)
        elif color == 'blue':
            self.image = pg.transform.scale(pg.image.load(os.path.join(BUBBLE_PATH, 'blue.png')), size)
        elif color == 'pink':
            self.image = pg.transform.scale(pg.image.load(os.path.join(BUBBLE_PATH, 'pink.png')), size)
        elif color == 'yellow':
            self.image = pg.transform.scale(pg.image.load(os.path.join(BUBBLE_PATH, 'yellow.png')), size)
        elif color == 'purple':
            self.image = pg.transform.scale(pg.image.load(os.path.join(BUBBLE_PATH, 'purple.png')), size)
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
                if pg.sprite.collide_circle(self, bubble):
                    self.vel = vec(0,0)
                    
class HexTile():
    """Use a dict to store neighbors.
    Each pair of opposing sides on a hexagon will be equal to 
    a different value mod 3. 0,1,2,3,4,5."""
    
    def __init__(self, pos, bubble=None):
        self.pos = pos
        self.neighbors = []
        self.bubble = bubble
        
    def set_bubble(self, b):
        self.bubble = b
    
                    
class BubbleGrid():
    def __init__(self, bubble_size, grid_size):
        self.bubble_size = bubble_size
        self.grid_size = grid_size
        self.arr = self.gen_bubble_array()
        self.bubbles = pg.sprite.Group()
        self.populate()
        
    def gen_bubble_array(self):
        rows = self.grid_size[1] // self.bubble_size 
        cols = self.grid_size[0] // self.bubble_size
        arr = []
        for i in range(rows):
            row = []
            for j in range(cols):
                row.append(random.choice(COLORS))
            arr.append(row)
        return arr
    
    def populate(self):
        for i, row in enumerate(self.arr):
            if i%2 == 0:
                offset = self.bubble_size//2
            else:
                offset = 0
            for j, bubble in enumerate(row):
                b = Bubble(pos=(offset+j*self.bubble_size + self.bubble_size//2, i*self.bubble_size + self.bubble_size//2), vel=(0,0), color=random.choice(COLORS))
                self.bubbles.add(b)
    
    def draw(self, screen):
        self.bubbles.draw(screen)

def test():
    running = True
    b = BubbleGrid(30, (WIDTH,HEIGHT))
    while running:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False
        b.draw(SCREEN)
        pg.display.flip()

# test()
# pg.quit()

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
        
def snap_to_grid(bubble):
    curr_pos = bubble.pos
    print(curr_pos)
    size = bubble.size[0]
    row = curr_pos.y//size
    if row % 2 == 0:
        offset = size//2
    else:
        offset = 0
    col = curr_pos.x//size
    print(row)
    print(col)
    x = col*size + size//2 + offset
    y = row*size + size//2
    bubble.pos = vec(x,y)
    
    
    