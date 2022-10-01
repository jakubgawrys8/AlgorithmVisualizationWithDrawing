import random
import globals as gv
import pygame
import math

def randomBoolean(probability):
    return random.random() < probability

def draw_rectangle(x, y, screen, block_size, color):
    pygame.draw.rect(screen, color, (x * block_size, y * block_size, block_size, block_size))

def round_to_block_size(number):
    return math.floor(number/gv.BLOCK_SIZE)