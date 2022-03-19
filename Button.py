import pygame
from App import screen, font
from Game_Constants import *

###TO DO###
#test if text can be added to the button and
#displayed properly
###TO DO###
class Button():
    def __init__(self, width, height, text_color, bg_color, hover_color, is_hovered: bool, state: bool, text: str):
        self.width = width
        self.height = height
        self.text_color = text_color
        self.bg_color = bg_color
        self.hover_color = hover_color
        self.is_hovered = is_hovered
        self.state = state
        self.text = text

        self.surface = pygame.Surface((width,height))
    def draw(self, screen: pygame.Surface, pos: tuple):
        #determine button color
        if self.is_hovered:
            self.surface.fill(self.hover_color)
        else:
            self.surface.fill(self.bg_color)
        #draw text onto button
        text_box = font.render(self.text, True, self.text_color)
        text_x = (self.width - text_box.get_width()) // 2
        text_y = (self.height - text_box.get_height()) // 2
        self.surface.blit(text_box, (text_x, text_y))
        #draw button on screen
        screen.blit(self.surface, pos)

    def click(self):
        self.state = True
    def change_hover(self): #changes is_hovered to true if mouse is in button, and false otherwise. Returns true if is_hovered changed, false otherwise
        mouse_pos = pygame.mouse.get_pos()
        changed = True
        was_hovered = self.is_hovered

        self.is_hovered = self.surface.get_rect().collidepoint(mouse_pos)

        if self.is_hovered == was_hovered:
            changed = False
        return changed