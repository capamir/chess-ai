import pygame
import sys

from const import *
from game import Game

class Main:
    def __init__(self):
        size = (WIDTH, HEIGHT)
        pygame.init()
        self.screen = pygame.display.set_mode(size)
        pygame.display.set_caption("Chess")
        self.game = Game()

    def mainloop(self):
        while True:
            self.game.show_bg(self.screen)

            # closing the game
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
            # main code

            # end code
            pygame.display.update()

main = Main()
main.mainloop()
