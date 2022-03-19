#initializes game

import pygame
from Game_Constants import *

pygame.init()
screen = pygame.display.set_mode(SCREEN_SIZE)
screen.fill(WHITE)
font = pygame.font.SysFont("arial", 20)
clock = pygame.time.Clock()