from Settings import *
import random

class Block(pg.sprite.Sprite):
    def __init__(self, tetromino, pos):
        #reference to class above
        self.tetromino = tetromino
        #starting position
        self.pos = vec(pos) + INIT_POS_OFFSET
        self.next_pos = vec(pos) + NEXT_POS_OFFSET
        self.alive = True 
        #allows use of functins from the pygame sprite class 
        super().__init__(tetromino.tetris.sprite_group)
        #generates a square 
        self.image = pg.Surface([TILE, TILE])
        #colors it based on the shape
        self.image.fill(TETROMINO_COLORS[self.tetromino.shape])
        # pg.draw.rect(self.image, self.tetromino.color, (1, 1, TILE -2, TILE -2), border_radius= 8)
        #allows placement of the block to our tile grid and allows it to render to scale
        self.rect = self.image.get_rect()
        self.rect.topleft = self.pos * TILE
    #destroy the sprite if it's not alive
    def is_alive(self):
        if not self.alive:
            self.kill()
    #rotating relative to pivot position
    def rotate(self, pivot_pos, counter_clockwise):
        translated = self.pos - pivot_pos
        if counter_clockwise:
            rotated = translated.rotate(-90)
        else:
            rotated = translated.rotate(90) 
        return rotated + pivot_pos
    #sets the position of the tetromino and checks if we're the one in the next window
    def set_rect_pos(self):
        pos = [self.next_pos, self.pos][self.tetromino.current]
        self.rect.topleft = pos * TILE
    #check if we're alive and move
    def update(self):
        self.is_alive()
        self.set_rect_pos()
    #checks for collisions with the world border or other blocks at a given position
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
        #generate shape from grab bag
        if not bool(self.tetris.grab_bag):
            self.tetris.grab_bag = list(TETROMINOES.keys())
        self.shape = random.choice(self.tetris.grab_bag)
        self.tetris.grab_bag.remove(self.shape)
        #generates blocks according to the tetromno dictionary
        self.blocks = [Block(self, pos) for pos in TETROMINOES[self.shape]]
        #initializing variables
        self.landed = False
        self.freebie = True
        self.rotation_state = 0
        self.current = current
        self.state = 0
    #Get rotation type given rotation direction
    def get_rotate_type(self, counter_clockwise):
        if counter_clockwise:
            new_state = self.state - 1
        else:
            new_state = self.state + 1
        if new_state < 0:
            new_state = 3
        elif new_state > 3:
            new_state = 0
        return (self.state, new_state)
    #rotate around pivot
    def rotate(self, counter_clockwise = False):
        #sets the pivot pos to be the central blocks pivot position
        pivot_pos = self.blocks[0].pos
        new_block_positions = [block.rotate(pivot_pos, counter_clockwise) for block in self.blocks]
        rotate_type = self.get_rotate_type(counter_clockwise)
        # if the shape is an I shape run the I tests for it
        if self.shape == 'I':
            for test in I_KICK_DATA[rotate_type]:
                test_positions = [positions + test for positions in new_block_positions]
                if not self.is_collide(test_positions):
                    for i, block in enumerate(self.blocks):
                        block.pos = test_positions[i]
                    self.state = rotate_type[1]
                    break
        else:
            #Test the kick data using the current rotation state
            for test in DEFAULT_KICK_DATA[rotate_type]:
                test_positions = [positions + test for positions in new_block_positions]
                #if there's no collision update the piece position
                if not self.is_collide(test_positions):
                    for i, block in enumerate(self.blocks):
                        block.pos = test_positions[i]
                    self.state = rotate_type[1]
                    break
    #check for any collisions with any blocks in the array
    def is_collide(self, block_positions):
        return any(map(Block.is_collide, self.blocks, block_positions))
    #move in a direction with a given vector
    def move(self, direction):
        #generate an attempted movement based on direction
        move_direction = MOVE_DIRECTIONS[direction]
        new_block_position = [block.pos + move_direction for block in self.blocks]
        is_collide = self.is_collide(new_block_position)
        
        #if there's no collision we go down
        if not is_collide:
            for block in self.blocks:
                block.pos += move_direction
        #checks if theres a collision while heading down
        elif direction == 'down':
            #more lenient just before landing
            if self.freebie:
                self.freebie = False
            else:
                self.landed = True
    
    def update(self):
        self.move(direction='down')