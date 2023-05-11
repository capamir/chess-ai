import pygame
import sys

from const import WIDTH, HEIGHT
from game import Game

class Main:
    def __init__(self):
        size = (WIDTH, HEIGHT)
        pygame.init()
        self.screen = pygame.display.set_mode(size)
        pygame.display.set_caption("Chess")
        self.game = Game(self.screen)

    def mainloop(self):
        game = self.game

        while True:
            game.show_bg()
            game.show_pieces()
            # closing the game
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
            
            pygame.display.update()

main = Main()
main.mainloop()
