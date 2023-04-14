import pygame as pg
import pygame.mixer as mixer
from pygame.locals import *

vec = pg.math.Vector2

#size of the grid on the game field
FIELD_SIZE = W, H = 10, 20
#scale of the game
TILE = 40

#directory constants
FONT_1 = 'assets/font/1up.ttf'
FONT_2 = 'assets/font/Inlanders.ttf'
FONT_3 = 'assets/font/Square.ttf'
THEME = 'assets/sounds/Theme.ogg'
LINE_CLEAR = 'assets/sounds/Line_Clear.wav'
FOUR_LINES = 'assets/sounds/4_Lines.wav'
LEVEL_UP = 'assets/sounds/Levelup.wav'

#Timer based constants
FAST_TIME = 10
PLAYER_TIME = 100
DIFFICULTY_MAP = {
    0 : 600,
    1 : 500,
    2 : 450,
    3 : 355,
    4 : 325,
    5 : 293,
    6 : 264,
    7 : 238,
    8 : 214,
    9 : 180
}
#Key for score based on lines cleared
POINT_PER_LINE = {
    0 : 0,
    1 : 100,
    2 : 500,
    3 : 1000,
    4 : 1500
}
#resolution of the playfield
WIDTH, HEIGHT = W * TILE, H * TILE
#scalers for HUD
FIELD_SCALE_W, FIELD_SCALE_H = 1.5,  1
#final game res
GAME_RES = (GAME_W, GAME_H) = WIDTH * FIELD_SCALE_W, HEIGHT * FIELD_SCALE_H  
FPS = 60
#background color
BGC = (30, 30, 30)

#initial position of the tetromino
INIT_POS_OFFSET = vec(W // 2 - 1, 0)
#position of the "next" tetrmonino
NEXT_POS_OFFSET = vec(W * 1.2, H * 0.3)
#Key for movement directions
MOVE_DIRECTIONS = {'left' : vec(-1, 0), 'right' : vec(1, 0), 'down' : vec(0, 1)}
#Dictionary that defines tetromno shapes as a series of vectors stemming from a pivot point
TETROMINOES = {
    'T' : [(0, 0), (-1, 0), (1, 0), (0, -1)],
    'O' : [(0, 0), (0, -1), (1, 0), (1, -1)],
    'J' : [(0, 0), (-1, 0), (1, 0), (-1, -1)],
    'L' : [(0, 0), (-1, 0), (1, 0), (1, -1)],
    'I' : [(0, 0), (-1, 0), (1, 0), (2, 0)],
    'S' : [(0, 0), (-1, 0), (0, -1), (1, -1)],
    'Z' : [(0, 0), (1, 0), (0, -1), (-1, -1)]
}
#tetromino color keys
TETROMINO_COLORS = {
    'T' : 'hotpink',
    'O' : 'gold',
    'J' : 'blue',
    'L' : 'darkorange',
    'I' : 'cyan',
    'S' : 'green',
    'Z' : 'red'
}
#WALL KICK TESTS
DEFAULT_KICK_DATA = {
    (0, 1) : [vec(0, 0), vec(-1, 0), vec(-1, -1), vec(0, 2) , vec(-1, 2) ],
    (1, 0) : [vec(0, 0), vec(1, 0) , vec(1, 1),   vec(0, -2), vec(1, -2) ],
    (1, 2) : [vec(0, 0), vec(1, 0) , vec(1, 1),   vec(0, -2), vec(1, -2) ],
    (2, 1) : [vec(0, 0), vec(-1, 0), vec(-1, -1), vec(0, 2) , vec(-1, 2) ],
    (2, 3) : [vec(0, 0), vec(1, 0) , vec(1, -1),  vec(0, 2) , vec(1, 2)  ],
    (3, 2) : [vec(0, 0), vec(-1, 0), vec(-1, 1),  vec(0, -2), vec(-1, -2)],
    (3, 0) : [vec(0, 0), vec(-1, 0), vec(-1, 1),  vec(0, -2), vec(-1, -2)],
    (0, 3) : [vec(0, 0), vec(1, 0) , vec(1, -1),  vec(0, 2) , vec(1, 2)  ]
}
I_KICK_DATA = { 
    (0, 1) : [vec(1, 0) , vec(-1, 0), vec(2, 0)  , vec(-1, 1) , vec(2,  -2)],
    (1, 0) : [vec(-1, 0), vec(1, 0) , vec(-2, 0) , vec(1, -1) , vec(-2, 2) ],
    (1, 2) : [vec(0, 1) , vec(-1, 1), vec(2, 1)  , vec(-1, -1), vec(2,  2) ],
    (2, 1) : [vec(0, -1), vec(1, -1), vec(-2, -1), vec(1, 1)  , vec(-2, -2)],
    (2, 3) : [vec(-1, 0), vec(1, 0) , vec(-2, 0) , vec(1, -1) , vec(-2, 2) ],
    (3, 2) : [vec(1, 0) , vec(-1, 0), vec(2, 0)  , vec(-1, 1) , vec(2,  -2)],
    (3, 0) : [vec(0, -1), vec(1, -1), vec(-2, -1), vec(1, 1)  , vec(-2, -2)],
    (0, 3) : [vec(0, 1) , vec(-1, 1), vec(2, 1)  , vec(-1, -1), vec(2,  2) ]
}