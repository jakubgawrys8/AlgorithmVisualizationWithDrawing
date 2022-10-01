import pygame
from enum import Enum
import pygame.freetype

BLACK = (0, 0, 0)
WHITE = (200, 200, 200)
BLOCK_SIZE = 20
WINDOW_HEIGHT = 720
WINDOW_WIDTH = 1320

SCREEN = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
CLOCK = pygame.time.Clock()

number_of_x_blocks = int(WINDOW_WIDTH / BLOCK_SIZE)
number_of_y_blocks = int(WINDOW_HEIGHT / BLOCK_SIZE)

map = [[0 for y in range(0, number_of_y_blocks)] for x in range(0, number_of_x_blocks)] 

walkableList = []
terrainList = []

openList = [] # green
closedList = [] # red

finalList = []

game_end = False

i = 0

class Position(Enum):
    TOP_LEFT = 1
    TOP = 2
    TOP_RIGHT = 3
    RIGHT = 4
    BOTTOM_RIGHT = 5
    BOTTOM = 6
    BOTTOM_LEFT = 7
    LEFT = 8
    NONE = 9

class Node:
    def __init__(self, x, y, g = 1, h = 1, f = 1, parent = None, final = False):
        self.x = x
        self.y = y
        self.g = g
        self.h = h
        self.f = f
        self.parent = parent
        self.final = final

    def equals(self, other):
        if(self.x == other.x and self.y == other.y):
            return True
        else:
            return False

class DistRect:
    def __init__(self, dist_val_name, rect_x, rect_y, value):
        self.dist_val_name = dist_val_name
        self.rect_x = rect_x
        self.rect_y = rect_y
        self.value = value

    def equals(self, other):
        if(self.rect_x == other.rect_x and self.rect_y == other.rect_y and self.dist_val_name == other.dist_val_name):
            return True
        else:
            return False

