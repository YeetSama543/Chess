import pygame as pg
from Game_Constants import *
from App import screen
from Button import Button

#buttons
choice1 = Button(TITLE_BUTTON_WIDTH, TITLE_BUTTON_HEIGHT, BUTTON_TEXT_COLOR, BUTTON_BG_COLOR, BUTTON_HOVER_COLOR, False, False, "Human Vs Human")
choice2 = Button(TITLE_BUTTON_WIDTH, TITLE_BUTTON_HEIGHT, BUTTON_TEXT_COLOR, BUTTON_BG_COLOR, BUTTON_HOVER_COLOR, False, False, "Human Vs Computer")
choice3 = Button(TITLE_BUTTON_WIDTH, TITLE_BUTTON_HEIGHT, BUTTON_TEXT_COLOR, BUTTON_BG_COLOR, BUTTON_HOVER_COLOR, False, False, "Quit")
buttons = [choice1, choice2, choice3]
#positioning vars
title_text_box = pg.font.SysFont("arial", 70).render("Chess", True, TITLE_TEXT_COLOR)
title_width = title_text_box.get_width()
title_height = title_text_box.get_height()
title_x = (SCREEN_SIZE[0] - title_width) // 2
title_y = 0
button_x = (SCREEN_SIZE[0] - TITLE_BUTTON_WIDTH) // 2
space_between_buttons = 100
#background image
bg = pg.image.load('Wooden-Background.png')
bg = pg.transform.scale(bg, SCREEN_SIZE)

def draw_background():
    screen.blit(bg, (0,0))

def draw():
    #draw bg
    draw_background()

    #draw title
    screen.blit(title_text_box, (title_x,title_y))

    #draw buttons
    choice1.draw(screen, (button_x, title_height + space_between_buttons + TITLE_BUTTON_Y_START))
    choice2.draw(screen, (button_x, title_height + 2 * space_between_buttons + TITLE_BUTTON_Y_START))
    choice3.draw(screen, (button_x, title_height + 3 * space_between_buttons + TITLE_BUTTON_Y_START))

def update(): #redraw buttons for when they are hovered or unhovered
    choice1.draw(screen, (button_x, title_height + space_between_buttons + TITLE_BUTTON_Y_START))
    choice2.draw(screen, (button_x, title_height + 2 * space_between_buttons + TITLE_BUTTON_Y_START))
    choice3.draw(screen, (button_x, title_height + 3 * space_between_buttons + TITLE_BUTTON_Y_START))