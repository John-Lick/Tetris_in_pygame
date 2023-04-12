import pygame as pg
import pygame.mixer as mixer
from pygame.locals import *

vec = pg.math.Vector2

FIELD_SIZE = W, H = 10, 20
TILE = 40

SPRITE_DIR_PATH = 'assets/sprites'
FONT_1 = 'assets/font/1up.ttf'
FONT_2 = 'assets/font/Inlanders.ttf'
FONT_3 = 'assets/font/Square.ttf'
THEME = 'assets/sounds/Theme.ogg'
LINE_CLEAR = 'assets/sounds/Line_Clear.wav'
FOUR_LINES = 'assets/sounds/4_Lines.wav'
LEVEL_UP = 'assets/sounds/Levelup.wav'

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
POINT_PER_LINE = {
    0 : 0,
    1 : 100,
    2 : 500,
    3 : 1000,
    4 : 1500
}
FAST_TIME = 15
WIDTH, HEIGHT = W * TILE, H * TILE
FIELD_SCALE_W, FIELD_SCALE_H = 1.5,  1
GAME_RES = (GAME_W, GAME_H) = WIDTH * FIELD_SCALE_W, HEIGHT * FIELD_SCALE_H  
FPS = 60
BGC = (30, 30, 30)

INIT_POS_OFFSET = vec(W // 2 - 1, 0)
NEXT_POS_OFFSET = vec(W * 1.2, H * 0.3)
MOVE_DIRECTIONS = {'left' : vec(-1, 0), 'right' : vec(1, 0), 'down' : vec(0, 1)}

TETROMINOES = {
    'T' : [(0, 0), (-1, 0), (1, 0), (0, -1)],
    'O' : [(0, 0), (0, -1), (1, 0), (1, -1)],
    'J' : [(0, 0), (-1, 0), (0, -1), (0, -2)],
    'L' : [(0, 0), (1, 0), (0, -1), (0, -2)],
    'I' : [(0, 0), (0, 1), (0, -1), (0, -2)],
    'S' : [(0, 0), (-1, 0), (0, -1), (1, -1)],
    'Z' : [(0, 0), (1, 0), (0, -1), (-1, -1)]
}
TETROMINO_COLORS = {
    'T' : 'hotpink',
    'O' : 'gold',
    'J' : 'blue',
    'L' : 'darkorange',
    'I' : 'cyan',
    'S' : 'green',
    'Z' : 'red'
}