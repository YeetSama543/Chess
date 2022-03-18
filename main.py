import pygame
import App
import Game

def main():
    running = True
    while running:
        for event in pygame.event.get(): #check for events
            if event.type == pygame.QUIT: #player exited
                running = False

if __name__ == "__main__":
    main()
