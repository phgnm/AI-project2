import pygame

# Speed
SPEED = 50          # Change the speed of the game here.

# Window
SCREEN_WIDTH = 970
SCREEN_HEIGHT = 710
CAPTION = 'Wumpus World'

# Cell
IMG_INITIAL_CELL = '../assets/images/initial_cell.png'
IMG_DISCOVERED_CELL = '../assets/images/discovered_cell.png'

# Object
IMG_PIT = '../assets/images/pit.png'
IMG_WUMPUS = '../assets/images/wumpus.png'
IMG_GOLD = '../assets/images/gold.png'
IMG_STENCH = '../assets/images/stench.png'
IMG_BREEZE = '../assets/images/breeze.png'
IMG_POTION = '../assets/images/potion.png'
IMG_GAS = '../assets/images/gas.png'

# Hunter
IMG_HUNTER_RIGHT = '../assets/images/hunter_right.png'
IMG_HUNTER_LEFT = '../assets/images/hunter_left.png'
IMG_HUNTER_UP = '../assets/images/hunter_up.png'
IMG_HUNTER_DOWN = '../assets/images/hunter_down.png'

IMG_ARROW_RIGHT = '../assets/images/arrow_right.png'
IMG_ARROW_LEFT = '../assets/images/arrow_left.png'
IMG_ARROW_UP = '../assets/images/arrow_up.png'
IMG_ARROW_DOWN = '../assets/images/arrow_down.png'

# Map
MAP_LIST = ['../assets/input/map_1.txt',
            '../assets/input/map_2.txt',
            '../assets/input/map_3.txt',
            '../assets/input/map_4.txt',
            '../assets/input/map_5.txt']
MAP_NUM = len(MAP_LIST)

# output
output_LIST = ['../assets/output/output_1.txt',
               '../assets/output/output_2.txt',
               '../assets/output/output_3.txt',
               '../assets/output/output_4.txt',
               '../assets/output/output_5.txt']

# Fonts
FONT_MRSMONSTER = '../assets/fonts/CenturyGothic.ttf'

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
LIGHT_GREY = (170, 170, 170)
DARK_GREY = (75, 75, 75)
RED = (255, 0, 0)

# state
RUNNING = 'running'
GAMEOVER = 'gameover'
WIN = 'win'
TRYBEST = 'trybest'
MAP = 'map'

LEVEL_1_POS = pygame.Rect(235, 120, 500, 50)
LEVEL_2_POS = pygame.Rect(235, 200, 500, 50)
LEVEL_3_POS = pygame.Rect(235, 280, 500, 50)
LEVEL_4_POS = pygame.Rect(235, 360, 500, 50)
LEVEL_5_POS = pygame.Rect(235, 440, 500, 50)
EXIT_POS = pygame.Rect(235, 520, 500, 50)