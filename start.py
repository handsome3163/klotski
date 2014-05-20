import pygame
from pygame.locals import *

NEW_LINE = '\n'

VALID_MOVE = -99

# Game Borders
LEFT_EDGE = 50
TOP_EDGE = 0
RIGHT_EDGE = 450
BOTTOM_EDGE = 500

# Colors
YELLOW = (255,255,0)
RED = (255,0,0)
LGREEN = (0,255,0)
BLACK = (0,0,0)
DGREY = (75,75,75)
GREY = (100,100,100)
WHITE = (255,255,255)

# tile pptys
SHORT = 100
NARROW = 100
TALL = 200
WIDE = 200

BGCOLOR = BLACK
FPS = 30

## Starting position of the tiles
# Big Box
BOX_X = 150
BOX_Y = 0

# VERTICAL TILES
COLM_1X = 50
COLM_1Y = 0

COLM_2X = 350
COLM_2Y = 0

COLM_3X = 50  
COLM_3Y = 200

COLM_4X = 350
COLM_4Y = 200

# HORIZANTAL TILE
HORZ_X = 150
HORZ_Y = 200

# SMALL BOX TILES
SMBX_1X = 50
SMBX_1Y = 400

SMBX_2X = 150
SMBX_2Y = 300

SMBX_3X = 250
SMBX_3Y = 300

SMBX_4X = 350
SMBX_4Y = 400

# INVISIBLE TILES THAT REPRESENT THE EMPTY SPACE
EMPTY_1X = 150
EMPTY_1Y = 400
EMPTY_2X = 250
EMPTY_2Y = 400

tiles = [ pygame.Rect((COLM_1X,COLM_1Y,NARROW,WIDE)), 
          pygame.Rect((BOX_X,BOX_Y,TALL,WIDE)),
          pygame.Rect((COLM_2X,COLM_2Y,NARROW,WIDE)),
          pygame.Rect((COLM_3X,COLM_3Y,NARROW,WIDE)), 
          pygame.Rect((HORZ_X,HORZ_Y,WIDE,SHORT)),
          pygame.Rect((COLM_4X,COLM_4Y,NARROW,TALL)),
          pygame.Rect((SMBX_2X,SMBX_2Y,NARROW,SHORT)),
          pygame.Rect((SMBX_3X,SMBX_3Y,NARROW,SHORT)),
          pygame.Rect((SMBX_1X,SMBX_1Y,NARROW,SHORT)),
          pygame.Rect((SMBX_4X,SMBX_4Y,NARROW,SHORT)) ]

# state of empty tiles
APART = 0
TOGETHER_VERT = 1
TOGETHER_HORZ = 2

emptyTiles = [ pygame.Rect((EMPTY_1X,EMPTY_1Y,NARROW,SHORT)),
                pygame.Rect((EMPTY_2X,EMPTY_2Y,NARROW,SHORT)) ]
