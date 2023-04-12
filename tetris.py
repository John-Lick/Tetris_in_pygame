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
        self.font_2.render_to(self.app.screen, (GAME_W * 0.7, GAME_H * 0.5),
                              text= 'SCORE', fgcolor='white',
                              size= TILE * 1.45)
        self.font_3.render_to(self.app.screen, (GAME_W * 0.685, GAME_H * 0.57),
                              text= f'{self.app.tetris.score}', fgcolor='white',
                              size= TILE * 1.3)
        self.font_2.render_to(self.app.screen, (GAME_W * 0.7, GAME_H * 0.7),
                              text= 'LEVEL', fgcolor='white',
                              size= TILE * 1.45)
        self.font_3.render_to(self.app.screen, (GAME_W * 0.802, GAME_H * 0.77),
                              text= f'{self.app.tetris.level}', fgcolor='white',
                              size= TILE * 1.3)
#The Game itself
class Tetris:
    def __init__(self, app) -> None:
        self.app = app
        self.sprite_group = pg.sprite.Group()
        self.field_array = self.get_field_array()
        self.grab_bag = list(TETROMINOES.keys())
        self.tetromino = Tetromino(self)
        self.next_tetromino = Tetromino(self, current= False)
        self.speed_up = False
        self.level = 0
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

        
        self.score = 0
        self.full_lines = 0
        self.levelcounter = 0
        self.sfx_key = {0 : None, 1 : self.line_clear}
    
    def get_score(self):
        self.score += POINT_PER_LINE[self.full_lines]
        if self.leveled_up:
            self.sfx.play(self.level_up)
        elif self.full_lines == 4:
            self.sfx.play(self.four_lines)
        elif self.full_lines > 0:
            self.sfx.play(self.line_clear)
        self.full_lines = 0
        
    def check_full_lines(self):
        self.leveled_up = False
        row = H - 1
        for y in range(H - 1, -1, -1):
            for x in range(W):
                self.field_array[row][x] = self.field_array[y][x]
                
                if self.field_array[y][x]:
                    self.field_array[row][x].pos = vec(x, y)
            
            if sum(map(bool, self.field_array[y])) < W:
                row -= 1
            else:
                for x in range(W):
                    self.field_array[row][x].alive = False
                    self.field_array[row][x] = 0
                self.full_lines += 1
                if self.level < 9:
                    self.levelcounter += 1
                    if self.levelcounter >= 10:
                        self.leveled_up = True
                        self.level +=1
                        self.levelcounter -= 10
                        pg.time.set_timer(self.app.user_event, DIFFICULTY_MAP[self.level]) 
            
            
    def put_tetromino_in_array(self):
        for block in self.tetromino.blocks:
            x, y = int(block.pos.x), int(block.pos.y)
            self.field_array[y][x] = block
    
    def get_field_array(self):
        return [[0 for x in range(W)] for y in range(H)]
    
    def is_game_over(self):
        if self.tetromino.blocks[0].pos.y == INIT_POS_OFFSET[1]:
            pg.time.wait(300)
            return True
    
    def check_tetromino_landing(self):
        if self.tetromino.landed:
            if self.is_game_over():
                pg.time.set_timer(self.app.user_event, DIFFICULTY_MAP[0]) 
                self.__init__(self.app)
            else:
                self.speed_up = False
                self.put_tetromino_in_array()
                self.next_tetromino.current = True
                self.tetromino = self.next_tetromino
                self.next_tetromino = Tetromino(self, current= False)
    
    def control(self, pressed_key):
        if pressed_key == K_LEFT:
            self.tetromino.move(direction='left')
        if pressed_key == K_RIGHT:
            self.tetromino.move(direction='right')
        if pressed_key == K_UP:
            self.tetromino.rotate()
        if pressed_key == K_DOWN:
            self.speed_up = True
    
    def draw_grid(self):
        for x in range(W):
            for y in range(H):
                pg.draw.rect(self.app.screen, (0, 0, 0), (x * TILE, y * TILE, TILE, TILE), 1)
    
    def update(self):
        trigger = [self.app.anim_trigger, self.app.fast_anim_trigger][self.speed_up]
        if trigger:
            self.check_full_lines()
            self.tetromino.update()
            self.check_tetromino_landing()
            self.get_score()
        self.sprite_group.update()
    
    def draw(self):
        self.draw_grid()
        self.sprite_group.draw(self.app.screen)