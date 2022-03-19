import pygame
from Game_Constants import *
from App import screen
from Button import Button

choice1 = Button(TITLE_BUTTON_WIDTH, TITLE_BUTTON_HEIGHT, BUTTON_TEXT_COLOR, BUTTON_BG_COLOR, BUTTON_HOVER_COLOR, False, False, "Human Vs Human")
choice1 = Button(TITLE_BUTTON_WIDTH, TITLE_BUTTON_HEIGHT, BUTTON_TEXT_COLOR, BUTTON_BG_COLOR, BUTTON_HOVER_COLOR, False, False, "Human Vs Computer")
choice1 = Button(TITLE_BUTTON_WIDTH, TITLE_BUTTON_HEIGHT, BUTTON_TEXT_COLOR, BUTTON_BG_COLOR, BUTTON_HOVER_COLOR, False, False, "Quit")

def draw():
    title_text_box = pygame.font.SysFont("arial", 50).render("Chess", True, BUTTON_TEXT_COLOR)
    screen.fill(TITLE_BG_COLOR)

def update(): #redraw buttons for when they are hovered or unhovered
    pass