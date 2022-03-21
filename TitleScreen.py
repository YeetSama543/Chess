import pygame
from Game_Constants import *
from App import screen
from Button import Button

#buttons
choice1 = Button(TITLE_BUTTON_WIDTH, TITLE_BUTTON_HEIGHT, BUTTON_TEXT_COLOR, BUTTON_BG_COLOR, BUTTON_HOVER_COLOR, False, False, "Human Vs Human")
choice2 = Button(TITLE_BUTTON_WIDTH, TITLE_BUTTON_HEIGHT, BUTTON_TEXT_COLOR, BUTTON_BG_COLOR, BUTTON_HOVER_COLOR, False, False, "Human Vs Computer")
choice3 = Button(TITLE_BUTTON_WIDTH, TITLE_BUTTON_HEIGHT, BUTTON_TEXT_COLOR, BUTTON_BG_COLOR, BUTTON_HOVER_COLOR, False, False, "Quit")
buttons = [choice1, choice2, choice3]
#positioning vars
title_text_box = pygame.font.SysFont("arial", 50).render("Chess", True, BUTTON_TEXT_COLOR)
title_width = title_text_box.get_width()
title_height = title_text_box.get_height()
title_x = (SCREEN_SIZE[0] - title_width) // 2
title_y = 0
button_x = (SCREEN_SIZE[0] - TITLE_BUTTON_WIDTH) // 2
space_between_buttons = 100

def draw():
    #bg
    screen.fill(TITLE_BG_COLOR)

    #draw title
    screen.blit(title_text_box, (title_x,title_y))

    #draw buttons
    choice1.draw(screen, (button_x, title_height + space_between_buttons))
    choice2.draw(screen, (button_x, title_height + 2 * space_between_buttons))
    choice3.draw(screen, (button_x, title_height + 3 * space_between_buttons))

def update(): #redraw buttons for when they are hovered or unhovered
    choice1.draw(screen, (button_x, title_height + space_between_buttons))
    choice2.draw(screen, (button_x, title_height + 2 * space_between_buttons))
    choice3.draw(screen, (button_x, title_height + 3 * space_between_buttons))