from Settings import *
import random

class Block(pg.sprite.Sprite):
    def __init__(self, tetromino, pos):
        self.tetromino = tetromino
        self.pos = vec(pos) + INIT_POS_OFFSET
        self.next_pos = vec(pos) + NEXT_POS_OFFSET
        self.alive = True 
        super().__init__(tetromino.tetris.sprite_group)
        self.image = pg.Surface([TILE, TILE])
        self.image.fill(TETROMINO_COLORS[self.tetromino.shape])
        # pg.draw.rect(self.image, self.tetromino.color, (1, 1, TILE -2, TILE -2), border_radius= 8)
        
        self.rect = self.image.get_rect()
        self.rect.topleft = self.pos * TILE
    
    def is_alive(self):
        if not self.alive:
            self.kill()
    
    def rotate(self, pivot_pos):
        translated = self.pos - pivot_pos
        rotated = translated.rotate(90)
        return rotated + pivot_pos
    
    def set_rect_pos(self):
        pos = [self.next_pos, self.pos][self.tetromino.current]
        self.rect.topleft = pos * TILE
            
    def update(self):
        self.is_alive()
        self.set_rect_pos()
         
    def is_collide(self, pos):
        x, y = int(pos.x), int(pos.y)
        if 0 <= x < W and y < H and (
            y < 0 or not self.tetromino.tetris.field_array[y][x]
        ):
            return False
        return True

class Tetromino:
    def __init__(self, tetris, current= True):
        self.tetris = tetris
        if not bool(self.tetris.grab_bag):
            self.tetris.grab_bag = list(TETROMINOES.keys())
        self.shape = random.choice(self.tetris.grab_bag)
        self.tetris.grab_bag.remove(self.shape)
        self.blocks = [Block(self, pos) for pos in TETROMINOES[self.shape]]
        self.landed = False
        self.freebie = True
        self.current = current
        
    def rotate(self):
        pivot_pos = self.blocks[0].pos
        new_block_positions = [block.rotate(pivot_pos) for block in self.blocks]
        
        if not self.is_collide(new_block_positions):
            for i, block in enumerate(self.blocks):
                block.pos = new_block_positions[i]
    
    def is_collide(self, block_positions):
        return any(map(Block.is_collide, self.blocks, block_positions))
        
    def move(self, direction):
        move_direction = MOVE_DIRECTIONS[direction]
        new_block_position = [block.pos + move_direction for block in self.blocks]
        is_collide = self.is_collide(new_block_position)
        
        if not is_collide:
            for block in self.blocks:
                block.pos += move_direction
        elif direction == 'down':
            if self.freebie:
                self.freebie = False
            else:
                self.landed = True
    
    def update(self):
        self.move(direction='down')