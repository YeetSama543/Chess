import pygame
import App
import Game

def main():
    running = True
    while running:
        for event in pygame.event.get(): #check for events
            if event.type == pygame.QUIT: #player exited
                running = False
        #update screen
        pygame.display.update()
        #set max frame rate
        App.clock.tick(60)

    pygame.quit()
if __name__ == "__main__":
    main()
