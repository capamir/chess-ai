import pygame
import sys

from src.const import WIDTH, HEIGHT, SQSIZE
from src.game import Game

class Main:
    def __init__(self):
        size = (WIDTH, HEIGHT)
        pygame.init()
        self.screen = pygame.display.set_mode(size)
        pygame.display.set_caption("Chess")
        self.game = Game(self.screen)

    def show_board(self):
        self.game.show_bg()
        self.game.show_pieces()

    def clicked(self, board, event):
        dragger = self.game.dragger

        dragger.update_mouse_pos(event.pos)

        clicked_row = dragger.mouseY // SQSIZE
        clicked_col = dragger.mouseX // SQSIZE
        
        # if clicked square has a piece
        if board.squares[clicked_row][clicked_col].has_piece():
            piece = board.squares[clicked_row][clicked_col].piece
            dragger.save_initial(event.pos)
            dragger.draged_piece(piece)

    def mouse_motion(self, event):
        dragger = self.game.dragger
        
        if dragger.draging:
            dragger.update_mouse_pos(event.pos)
            self.show_board()
            dragger.update_blit(self.game.surface)

    def quit_app(self):
        pygame.quit()
        sys.exit()

    def mainloop(self):
        game = self.game
        board = self.game.board
        dragger = self.game.dragger

        while True:
            self.show_board()

            if dragger.draging:
                dragger.update_blit(game.surface)

            # click event
            for event in pygame.event.get():
                # clicked
                if event.type == pygame.MOUSEBUTTONDOWN:
                    self.clicked(board ,event)

                # mouse motion 
                elif event.type == pygame.MOUSEMOTION:
                    self.mouse_motion(event)

                # click release 
                elif event.type == pygame.MOUSEBUTTONUP:
                    dragger.undrag_piece()

                # quit application
                elif event.type == pygame.QUIT:
                    self.quit_app()
            
            pygame.display.update()

main = Main()
main.mainloop()
