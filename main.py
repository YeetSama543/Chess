import pygame as pg
import App
import Game
import TitleScreen

def main():
    #game loop for title screen
    running = True
    choice = 0
    TitleScreen.draw()
    while running:
        for event in pg.event.get(): #check for events
            if event.type == pg.QUIT: #player exited
                running = False
            if event.type == pg.MOUSEMOTION:
                for button in TitleScreen.buttons:
                    if button.change_hover():
                        TitleScreen.update()
            if event.type == pg.MOUSEBUTTONUP:
                button_count = 0 #used to set choice
                for button in TitleScreen.buttons:
                    button_count += 1
                    if button.is_hovered: #mouse was on button when mouse button was released
                        button.click()
                        choice = button_count
                        running = False
        #update screen
        pg.display.update()
        #set max frame rate
        App.clock.tick(60)


    pg.quit()
if __name__ == "__main__":
    main()
