import pygame

from .conf.const import ROWS, COLS, SQSIZE, HEIGHT
from .conf.config import Config
from .board.board import Board, Square
from .movement.dragger import Dragger

class Game:
    def __init__(self, surface):
        self.surface = surface
        self.next_player = 'white'
        self.hovered_sqr = None
        self.board = Board()
        self.dragger = Dragger()
        self.config = Config()

    # show methods
    def show_bg(self):
        theme = self.config.theme
        for row in range(ROWS):
            for col in range(COLS):
                # color
                color  = theme.bg_color(row, col)
                # rect
                rect = Square.rect(row, col)
                # blit
                pygame.draw.rect(self.surface, color, rect)

                if col == 0:
                    # color
                    color = theme.bg_color(row, col, reverse=True)
                    # label
                    lbl = self.config.font.render(str(ROWS-row), 1, color)
                    # label position
                    lbl_pos = (5, 5 + row*SQSIZE)
                    # blit
                    self.surface.blit(lbl, lbl_pos)

                if row == 7:
                    # color
                    color = theme.bg_color(row, col, reverse=True)
                    # label
                    lbl = self.config.font.render(Square.get_alphacol(col), 1, color)
                    # label position
                    lbl_pos = ((col+1)*SQSIZE -20, HEIGHT-20)
                    # blit
                    self.surface.blit(lbl, lbl_pos)


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
        theme = self.config.theme

        if self.dragger.dragging:
            piece = self.dragger.piece
            # loop all the valid moves
            for move in piece.valid_moves:
                # color
                color = theme.moves_color(move.final.row, move.final.col)
                # rect
                rect = Square.rect(move.final.row, move.final.col)
                # blit
                self._blit(color, rect)

    def show_last_move(self):
        theme = self.config.theme

        if self.board.last_move:
            initial = self.board.last_move.initial
            final = self.board.last_move.final
            for pos in [initial, final]:
                # color
                color = theme.trace_color(pos.row, pos.col)
                # rect
                rect = Square.rect(pos.row, pos.col)
                # blit
                self._blit(color, rect)
    
    def show_hover(self):
        if self.hovered_sqr:
            # color
            color = (180, 180, 180)
            # rect
            rect = Square.rect(self.hovered_sqr.row, self.hovered_sqr.col)
            # blit
            pygame.draw.rect(self.surface, color, rect, width=3)

    def _blit(self, color, rect):
        pygame.draw.rect(self.surface, color, rect)
        

    # other methods
    def next_turn(self):
        self.next_player = 'white' if self.next_player == 'black' else 'black'

    def set_hover(self, row, col):
        self.hovered_sqr = self.board.squares[row][col]

    def change_theme(self):
        self.config.change_theme()

    def sound_effect(self, captured=False):
        if captured:
            self.config.capture_sound.play()
        else: 
            self.config.move_sound.play()
