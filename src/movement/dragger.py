import pygame

from src.const import SQSIZE

class Dragger:
    def __init__(self):
        self.piece = None
        self.dragging: bool = False
        self.mouseX: int = 0
        self.mouseY: int = 0
        self.initial_row: int = 0
        self.initial_col: int = 0

    def update_mouse_pos(self, pos):
        self.mouseX, self.mouseY = pos # (Xcor, Ycor)

    def save_initial(self, pos):
        self.initial_row = pos[1] // SQSIZE
        self.initial_col = pos[0] // SQSIZE

    def draged_piece(self, piece):
        self.piece = piece
        self.dragging = True
    
    def undrag_piece(self):
        self.piece.set_texture()

        self.piece = None
        self.dragging = False

    def update_blit(self, surface):
        # path
        self.piece.set_texture(size=128)
        # image
        img = pygame.image.load(self.piece.texture)
        # rect
        img_center = (self.mouseX, self.mouseY)
        self.piece.texture_rect = img.get_rect(center=img_center)
        surface.blit(img, self.piece.texture_rect)
