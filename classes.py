import pygame as pg
import random
import os
import math
from settings import *
from utils import *
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

    def draw(self, surface):
        surface.blit(self.image, self.rect)

class HexTile():
    """Use a dict to store neighbors.
    Each pair of opposing sides on a hexagon will be equal to
    a different value mod 3. 0,1,2,3,4,5."""

    def __init__(self, pos, radius, bubble=None):
        self.pos = pos
        self.radius = radius
        self.neighbors = []
        self.bubble = bubble

    def set_bubble(self, b):
        self.bubble = Bubble(self.pos, (0,0), b.color)

    def clear_bubble(self):
        self.bubble = None

    def is_occupied(self):
        if self.bubble is None:
            return False
        else:
            return True

    def draw(self, surface):
        draw_hexagon(self.pos, self.radius, surface, RED)
        if self.bubble:
            self.bubble.draw(surface)

class HexGrid():
    def __init__(self, surface, radius):
        self.surface = surface
        self.radius  = radius
        self.width = surface.get_width()
        self.height = surface.get_height()
        self.hex_width = math.sqrt(3) * radius
        self.hex_height = 2 * radius
        self.horizontal_spacing = self.hex_width
        self.vertical_spacing = self.hex_height * 0.75
        self.rows =  int(self.height//self.vertical_spacing)
        self.cols = int(self.width//self.horizontal_spacing)
        self.tiles = {}
        self.tile_surface()

    def tile_surface(self):
        for i in range(self.rows):
            if i % 2 == 0:
                offset = self.hex_width//2
            else:
                offset = 0
            for j in range(self.cols):
                center = (j*self.horizontal_spacing+self.hex_width//2+offset, i*self.vertical_spacing+self.radius)
                self.tiles[(i,j)] = HexTile(center, self.radius)
                if offset:
                    neighbors = [(i-1,j), (i-1,j+1), (i,j-1), (i,j+1), (i+1,j), (i+1,j+1)]
                else:
                    neighbors = [(i-1,j-1), (i-1,j), (i,j-1), (i,j+1), (i+1,j-1), (i+1,j)]
                neighbors = [x for x in neighbors if x[0]>=0 and x[0]<self.rows and x[1]>=0 and x[1]<self.cols]
                self.tiles[(i,j)].neighbors += neighbors

    def draw(self, surface):
        for tile in self.tiles.values():
            tile.draw(surface)

    def snap_to_tile(self, bubble):
        x = bubble.pos.x
        y = bubble.pos.y
        row = int(y // self.vertical_spacing)
        if row % 2 == 0:
            offset = self.hex_width // 2
        else:
            offset = 0
        col = int((x-offset) // self.horizontal_spacing)
        self.tiles[(row,col)].set_bubble(bubble)
        
    def snap_to_tile2(self, bubble):
        x = bubble.pos.x
        y = bubble.pos.y
        closest_tile = None
        index = None
        min_dist = 10000
        for tile in self.tiles.items():
            i = tile[0]
            t = tile[1]
            tx = t.pos[0]
            ty = t.pos[1]
            if t.bubble is None:
                dist = math.sqrt((x-tx)**2 + (y-ty)**2) 
                if dist < min_dist:
                    closest_tile = tile
                    index = i
                    min_dist = dist
        self.tiles[index].set_bubble(bubble)
        return index
        
    def find_cluster(self, tile):
        cluster_type = tile.bubble.color
        checked = []
        cluster = []
        unchecked = [tile]
        while len(unchecked) > 0:
            curr_tile = unchecked.pop()
            if curr_tile.bubble.color == cluster_type:
                cluster.append(curr_tile)
                for neighbor in curr_tile.neighbors:
                    if self.tiles[neighbor].bubble is not None and self.tiles[neighbor] not in checked: 
                        unchecked.append(self.tiles[neighbor])
            checked.append(curr_tile)
        # for tile in cluster:
        #     print(tile.bubble.color)
        if len(cluster) >= 3:
            for tile in cluster:
                tile.clear_bubble()
                # print(tile.bubble.color)
                    

    def populate(self, row):
        """Populate the grid up to a certain row with random bubbles"""

        for i in range(row):
            for j in range(self.cols):
                tile = self.tiles[(i,j)]
                pos = tile.pos
                self.tiles[(i,j)].set_bubble(Bubble(pos, (0,0), random.choice(COLORS)))

    def update(self):
        pass

def test():
    running = True
    h = HexGrid(SCREEN, 20)
    h.populate(5)
    while running:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False
        h.draw(SCREEN)
        pg.display.flip()

# test()
# pg.quit()


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

    def draw(self, surface):
        pg.draw.line(surface, RED, self.start, self.end, 5)
