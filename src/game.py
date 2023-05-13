import pygame

from .const import ROWS, COLS, SQSIZE, COLORS
from .board.board import Board
from .movement.dragger import Dragger

class Game:
    def __init__(self, surface):
        self.surface = surface
        self.board = Board()
        self.dragger = Dragger()

    def show_bg(self):
        for row in range(ROWS):
            for col in range(COLS):
                if (row + col) % 2 == 0:
                    color = COLORS['green']['light'] # light green
                else:
                    color = COLORS['green']['dark'] # dark green
                
                rect = (col*SQSIZE, row*SQSIZE, SQSIZE, SQSIZE)

                pygame.draw.rect(self.surface, color, rect)

    def show_pieces(self):
        for row in range(ROWS):
            for col in range(COLS):
                if self.board.squares[row][col].has_piece():
                    piece = self.board.squares[row][col].piece
                    # all pieces except the dragger piece 
                    if piece is not self.dragger.piece:
                        img = pygame.image.load(piece.texture) # image object
                        img_center = (col*SQSIZE + SQSIZE//2, row*SQSIZE + SQSIZE//2)
                        piece.texture_rect = img.get_rect(center=img_center) # position of the piece
                        self.surface.blit(img, piece.texture_rect)
