import pygame as pg
from App import *
import Game
from Piece import Color
import TitleScreen
from Board import Board
from Game_Constants import *

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
        clock.tick(60)
    
    #create board
    board = Board((0,0))
    board.add_pieces()
    #draw game screen + board
    screen.fill(GAME_BG_COLOR)
    board.draw(screen)
    if choice == 1: #human vs human
        running = True
        while running:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    running  = False
                if event.type == pg.MOUSEBUTTONUP:
                    mouse_pos = pg.mouse.get_pos()

                    if Game.clicked_on_board(mouse_pos, board): #player clicked on board
                        clicked_square = Game.get_clicked_square(mouse_pos, board)
                        piece_on_clicked_square = board.get_piece_on_square(clicked_square)

                        if board.clicked_piece: #piece is selected
                            attacked_squares = Game.generate_attacked_squares(board.clicked_piece, board)

                            #check if an attacked square was clicked
                            if clicked_square in attacked_squares:
                                #move piece
                                board.move(clicked_square)

                                #handle pawn promotion
                                promotion_square = Game.pawn_promotion(board)
                                if promotion_square: #a pawn promotes
                                    board.draw(screen) #make sure screen updates
                                    pg.display.flip()

                                    Game.promote(board, promotion_square) #promote pawn, takes keyboard input

                                #change the turn
                                Game.change_turn(board)

                            else: #pressed a square the piece can't move to
                                board.clicked_piece = None

                            #redraw board
                            board.draw(screen)

                        else: #no piece is selected
                            if piece_on_clicked_square:
                                #If it is white to move, allow white to select a white piece.
                                #similarly, if it is black to move, allow player to select black piece.
                                #attacked square generation is handled without regard to turn, so
                                #there is no need to consider turn anywhere else but here

                                if Game.turn == 0: #white to move
                                    if piece_on_clicked_square.get_color() == Color.WHITE:
                                        attacked_squares = Game.generate_attacked_squares(piece_on_clicked_square, board)
                                        board.click_piece(screen, piece_on_clicked_square, attacked_squares)

                                else: #black to move
                                    if piece_on_clicked_square.get_color() == Color.BLACK:
                                        attacked_squares = Game.generate_attacked_squares(piece_on_clicked_square, board)
                                        board.click_piece(screen, piece_on_clicked_square, attacked_squares)
                        

            #update screen
            pg.display.update()
            #set max frame rate
            clock.tick(60)

    elif choice == 2: #human vs ai
        running = True
        screen.fill(GAME_BG_COLOR)
        board.draw(screen)

        while running:
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    running  = False
            #update screen
            pg.display.update()
            #set max frame rate
            clock.tick(60)
    pg.quit()
if __name__ == "__main__":
    main()
