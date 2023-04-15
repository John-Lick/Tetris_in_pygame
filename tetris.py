from Settings import *
from tetromino import Tetromino
import pygame.freetype as ft

class Text:
    def __init__(self, app):
        self.app = app
        #a couple fonts, Font 1 is unused but there in case i want to later
        self.font_1 = ft.Font(FONT_1)
        self.font_2 = ft.Font(FONT_2)
        self.font_3 = ft.Font(FONT_3)
    #HUD, pretty self explanatory
    def draw(self):
        self.font_2.render_to(self.app.screen, (GAME_W * 0.685, GAME_H * 0.02),
                              text= 'TETRIS', fgcolor='white',
                              size= TILE * 1.45)
        self.font_3.render_to(self.app.screen, (GAME_W * 0.75, GAME_H * 0.15),
                              text= 'next', fgcolor='white',
                              size= TILE * 1.2)
        self.font_2.render_to(self.app.screen, (GAME_W * 0.7, GAME_H * 0.4),
                              text= 'SCORE', fgcolor='white',
                              size= TILE * 1.45)
        self.font_3.render_to(self.app.screen, (GAME_W * 0.7, GAME_H * 0.47),
                              text= f'{self.app.tetris.score}', fgcolor='white',
                              size= TILE * 1.3)
        self.font_2.render_to(self.app.screen, (GAME_W * 0.7, GAME_H * 0.55),
                              text= 'LEVEL', fgcolor='white',
                              size= TILE * 1.45)
        self.font_3.render_to(self.app.screen, (GAME_W * 0.7, GAME_H * 0.62),
                              text= f'{self.app.tetris.level}', fgcolor='white',
                              size= TILE * 1.3)
        self.font_2.render_to(self.app.screen, (GAME_W * 0.7, GAME_H * 0.7),
                              text= 'HI-SCORE', fgcolor='white',
                              size= TILE * 1.1)
        if self.app.tetris.high_score > self.app.tetris.score:
            self.font_3.render_to(self.app.screen, (GAME_W * 0.7, GAME_H * 0.77),
                                  text= f'{self.app.tetris.high_score}', fgcolor='white',
                                  size= TILE * 1.3)
        else:
            self.font_3.render_to(self.app.screen, (GAME_W * 0.7, GAME_H * 0.77),
                                  text= f'{self.app.tetris.score}', fgcolor='white',
                                  size= TILE * 1.3)
#The Game itself
class Tetris:
    def __init__(self, app) -> None:
        #Gives us a pointer to the app a layer above
        self.app = app
        #creates a spritegroup to reference for rendering and updating purposes
        self.sprite_group = pg.sprite.Group()
        #initializes array that represents the gamespace
        self.field_array = self.get_field_array()
        #initializes a list to pull shapes from
        self.grab_bag = list(TETROMINOES.keys())
        #generates the initial tetromino
        self.tetromino = Tetromino(self)
        #generates the next tetromino
        self.next_tetromino = Tetromino(self, current= False)
        
        #initializing variables for later
        self.speed_up = False
        self.leveled_up = False
        self.level = 0
        self.score = 0
        self.full_lines = 0
        self.levelcounter = 0
        self.init_high_score()
        # Sounds
        self.theme = mixer.Sound(THEME)
        self.line_clear = mixer.Sound(LINE_CLEAR)
        self.four_lines = mixer.Sound(FOUR_LINES)
        self.level_up = mixer.Sound(LEVEL_UP)
        # Channels
        self.song = mixer.Channel(1)
        self.sfx = mixer.Channel(2)
        # Volume Adjust
        self.theme.set_volume(0.5)
        
        self.song.play(self.theme, -1)
        
    def init_high_score(self):
        self.score_data = shelve.open('data/score', writeback= True)
        if not 'hi_score' in self.score_data:
            self.score_data['hi_score'] = 0
        self.high_score = self.score_data['hi_score'] 
        self.score_data.close
    
    def check_hi_score(self):
        self.score_data = shelve.open('data/score', writeback= True)
        if self.score > self.high_score:
            self.score_data['hi_score'] = self.score
        self.score_data.close
    
    def get_score(self):
        #adds score to score variable
        self.score += POINT_PER_LINE[self.full_lines]
        #plays appropriate sound effect if there is any to play
        if self.leveled_up:
            self.sfx.play(self.level_up)
        elif self.full_lines == 4:
            self.sfx.play(self.four_lines)
        elif self.full_lines > 0:
            self.sfx.play(self.line_clear)
        self.leveled_up = False
        self.check_hi_score()
        self.full_lines = 0
        #resets the full line counter for this game cycle
        
    def check_full_lines(self):
        #row variable to be iterated from later
        row = H - 1
        # we start from the bottom and iterate backwards 
        for y in range(H - 1, -1, -1):
            #this iterates through each position in the array, and if there's a block present it updates it's position
            for x in range(W):
                self.field_array[row][x] = self.field_array[y][x]
                
                if self.field_array[y][x]:
                    self.field_array[row][x].pos = vec(x, y)
            #is the row not full? if so, go up a row
            #since we don't iterate up when we don't clear a row it causes the rows above to shift down
            #this happens because we update everything's position above
            if sum(map(bool, self.field_array[y])) < W:
                row -= 1
            else:
                #if it is full tell everything to kill itself 
                for x in range(W):
                    self.field_array[row][x].alive = False
                    self.field_array[row][x] = 0
                #log how many lines are being cleared on this run of the function
                self.full_lines += 1
                #if we level up, level up and update the game speed
                if self.level < 9:
                    self.levelcounter += 5
                    if self.levelcounter >= 10:
                        self.leveled_up = True
                        self.level +=1
                        self.levelcounter -= 10
                        pg.time.set_timer(self.app.user_event, DIFFICULTY_MAP[self.level]) 
    
    def put_tetromino_in_array(self):
        # put a pointer to each block inside the active tetromino in the array if this function is called
        for block in self.tetromino.blocks:
            x, y = int(block.pos.x), int(block.pos.y)
            self.field_array[y][x] = block
    
    #generate our empty array
    def get_field_array(self):
        return [[0 for x in range(W)] for y in range(H)]
    
    #check if the game is over by detecting a lack of change from initial position
    def is_game_over(self):
        if self.tetromino.blocks[0].pos.y == INIT_POS_OFFSET[1]:
            pg.time.wait(300)
            return True
    
    def check_tetromino_landing(self):
        if self.tetromino.landed:
            #is the game over? if so start over
            if self.is_game_over():
                pg.time.set_timer(self.app.user_event, DIFFICULTY_MAP[0]) 
                self.__init__(self.app)
            #generate next piece
            else:
                self.speed_up = False
                self.put_tetromino_in_array()
                self.next_tetromino.current = True
                self.tetromino = self.next_tetromino
                self.next_tetromino = Tetromino(self, current= False)
    
    #initiates hard drop or rotation if it's called
    def explicit_control(self, pressed_key):
        if pressed_key == K_KP_4:
            self.tetromino.move(direction= 'left')
        if pressed_key == K_KP_6:
            self.tetromino.move(direction= 'right')
        if pressed_key in {K_UP, K_KP_8, K_x}:
            self.tetromino.rotate()
        if pressed_key in {K_z, K_LCTRL}:
            self.tetromino.rotate(True)
        if pressed_key == K_SPACE:
            self.speed_up = True
    
    #passive movement
    def passive_control(self, pressed_keys):
        if pressed_keys[K_DOWN]:
            self.tetromino.move(direction= 'down')
            self.moved_down = True
        if pressed_keys[K_LEFT]:
            self.tetromino.move(direction= 'left')
        if pressed_keys[K_RIGHT]:
            self.tetromino.move(direction= 'right')
        
    #generate grid at the start of the game
    def draw_grid(self):
        for x in range(W):
            for y in range(H):
                pg.draw.rect(self.app.screen, (0, 0, 0), (x * TILE, y * TILE, TILE, TILE), 1)
    
    def update(self):
        #check if either of the passive triggers are active
        trigger = [self.app.anim_trigger, self.app.fast_anim_trigger][self.speed_up]
        self.moved_down = False
        if self.app.input_trigger:
            self.check_full_lines()
            self.passive_control(pg.key.get_pressed())
        if trigger and not self.moved_down:
            self.check_full_lines()
            self.tetromino.update()
            self.moved_down = True
        #if the trigger for the input window is on, let that happen
        if self.moved_down:
            self.check_tetromino_landing()
            self.get_score()
        self.sprite_group.update()
    #render anything
    def draw(self):
        self.draw_grid()
        self.sprite_group.draw(self.app.screen)
