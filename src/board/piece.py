import os
import pygame

class Piece:
    def __init__(self, name, color, value, texture=None, texture_rect=None):
        self.name = name
        self.color = color
        value_sign = 1 if color == 'white' else -1
        self.value = value * value_sign
        self.valid_moves = []
        self.moved = False

        self.texture = texture # image url
        self.set_texture()
        self.texture_rect = texture_rect # image position

    def set_texture(self, size=80):
        self.texture = os.path.join(
            f'src/assets/images/imgs-{size}px/{self.color}_{self.name}.png'
        )
    
    def add_moves(self, move):
        self.valid_moves.append(move)

    # def blit_img(self, size, cor):
    #     self.set_texture(size=size) # path
    #     img = pygame.image.load(self.texture)
    #     self.texture_rect = img.get_rect(center=cor)
    #     return img, self.texture_rect

class Pawn(Piece):
    def __init__(self, color):
        self.dir = -1 if color == 'white' else 1 # else color == 'black'
        super().__init__('pawn', color, 1.0)

class Knight(Piece):
    def __init__(self, color):
        super().__init__('knight', color, 3.0)

class Bishop(Piece):
    def __init__(self, color):
        super().__init__('bishop', color, 3.001)

class Rook(Piece):
    def __init__(self, color):
        super().__init__('rook', color, 5.0)

class Queen(Piece):
    def __init__(self, color):
        super().__init__('queen', color, 9.0)

class King(Piece):
    def __init__(self, color):
        super().__init__('king', color, 10000.0)
