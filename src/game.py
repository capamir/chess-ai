import pygame

from .conf.const import ROWS, COLS, SQSIZE, COLORS
from .board.board import Board
from .movement.dragger import Dragger

class Game:
    def __init__(self, surface):
        self.surface = surface
        self.next_player = 'white'
        self.hovered_sqr = None
        self.board = Board()
        self.dragger = Dragger()

    # show methods
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

    def show_moves(self):
        if self.dragger.dragging:
            piece = self.dragger.piece
            # loop all the valid moves
            for move in piece.valid_moves:
                # color
                color = COLORS['red']['light'] if (move.final.row + move.final.col) % 2 == 0 else COLORS['red']['dark']
                # rect
                rect = (move.final.col*SQSIZE, move.final.row*SQSIZE, SQSIZE, SQSIZE)
                # blit
                pygame.draw.rect(self.surface, color, rect)

    def show_last_move(self):
        if self.board.last_move:
            initial = self.board.last_move.initial
            final = self.board.last_move.final
            for pos in [initial, final]:
                # color
                color = (244, 247, 116) if (pos.row + pos.col) % 2 == 0 else (172, 195, 51)
                # rect
                rect = (pos.col*SQSIZE, pos.row*SQSIZE, SQSIZE, SQSIZE)
                # blit
                pygame.draw.rect(self.surface, color, rect)
    
    def show_hover(self):
        if self.hovered_sqr:
            # color
            color = (180, 180, 180)
            # rect
            rect = (self.hovered_sqr.col*SQSIZE, self.hovered_sqr.row*SQSIZE, SQSIZE, SQSIZE)
            # blit
            pygame.draw.rect(self.surface, color, rect, width=3)


    # other methods
    def next_turn(self):
        self.next_player = 'white' if self.next_player == 'black' else 'black'

    def set_hover(self, row, col):
        self.hovered_sqr = self.board.squares[row][col]