import os
import pygame
from .square import Square
from src.movement.move import Move


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
        """set the path of piece's image base on the size"""
        self.texture = os.path.join(
            f'src/assets/images/imgs-{size}px/{self.color}_{self.name}.png'
        )
    
    def add_move(self, row, col, possible_row, possible_col):
        """append new valid move"""
        # create squares of the move
        initial = Square(row, col)
        final = Square(possible_row, possible_col)
        # create a new move
        move = Move(initial, final)
        # append new valid move 
        self.valid_moves.append(move)
    
    def clear_moves(self):
        self.valid_moves = []

    def straightline_moves(self, squares, row, col, incrs):
        for incr in incrs:
            row_incr, col_incr = incr
            possible_row = row + row_incr
            possible_col = col + col_incr
            while True:
                if Square.in_range(possible_row, possible_col):
                    # empty = continue looping
                    if squares[possible_row][possible_col].is_empty():
                        self.add_move(row, col, possible_row, possible_col)
                    # has enemy piece
                    elif squares[possible_row][possible_col].has_rival_piece(self.color):
                        self.add_move(row, col, possible_row, possible_col)
                        break
                    # team piece
                    elif squares[possible_row][possible_col].has_team_piece(self.color):
                        break
                # not in range
                else: break
                # incrementing incrs
                possible_row += row_incr
                possible_col += col_incr

    def circle_moves(self, squares, row, col, incrs):
        for incr in incrs:
            row_incr, col_incr = incr
            possible_row = row + row_incr
            possible_col = col + col_incr

            if Square.in_range(possible_row, possible_col):
                if squares[possible_row][possible_col].is_empty_or_rival(self.color):
                    self.add_move(row, col, possible_row, possible_col)



class Pawn(Piece):
    def __init__(self, color):
        self.dir = -1 if color == 'white' else 1 # else color == 'black'
        super().__init__('pawn', color, 1.0)

    def moves(self, squares, row, col):
        steps = 1 if self.moved else 2
        # vertical moves
        start = row + self.dir
        end = row + (self.dir * (1 + steps))
        for move_row in range(start, end, self.dir):
            if Square.in_range(move_row, col) and squares[move_row][col].is_empty():
                self.add_move(row, col, move_row, col)
            # not in range or blocked
            else: break

        # diagonal moves
        possible_move_row = row + self.dir
        possibile_move_cols = [col-1, col+1]
        for move_col in possibile_move_cols:
            if Square.in_range(possible_move_row, move_col):
                if squares[possible_move_row][move_col].has_rival_piece(self.color):
                    self.add_move(row, col, possible_move_row, move_col)


class Knight(Piece):
    def __init__(self, color):
        self.incrs = [
            (-2, 1), # up right
            (-2, -1), # up left
            (-1, 2), # right up
            (1, 2), # right down
            (2, 1), # down right
            (2, -1), # down left
            (-1, -2), # left up
            (1, -2), # left down
        ]
        super().__init__('knight', color, 3.0)
    
    def moves(self, squares, row, col):
        self.circle_moves(squares, row, col, self.incrs)


class Bishop(Piece):
    def __init__(self, color):
        self.incrs = [
            (-1, -1), # up left
            (-1, 1),  # up right
            (1, 1),   # down right
            (1, -1),  # down left
        ]
        super().__init__('bishop', color, 3.001)

    def moves(self, squares, row, col):
        self.straightline_moves(squares, row, col, self.incrs)
        

class Rook(Piece):
    def __init__(self, color):
        self.incrs = [
            (-1, 0), # up
            (1, 0),  # down
            (0, 1),  # right
            (0, -1), # left
        ]
        super().__init__('rook', color, 5.0)

    def moves(self, squares, row, col):
        self.straightline_moves(squares, row, col, self.incrs)


class Queen(Piece):
    def __init__(self, color):
        self.incrs = [
            (-1, 0), # up
            (1, 0),  # down
            (0, 1),  # right
            (0, -1), # left
            (-1, -1), # up left
            (-1, 1),  # up right
            (1, 1),   # down right
            (1, -1),  # down left
        ]
        super().__init__('queen', color, 9.0)

    def moves(self, squares, row, col):
        self.straightline_moves(squares, row, col, self.incrs)
        

class King(Piece):
    def __init__(self, color):
        self.incrs = [
            (-1, 0), # up
            (1, 0),  # down
            (0, 1),  # right
            (0, -1), # left
            (-1, -1), # up left
            (-1, 1),  # up right
            (1, 1),   # down right
            (1, -1),  # down left   
        ]
        super().__init__('king', color, 10000.0)

    def moves(self, squares, row, col):
        # castling
        if not self.moved:
            # King castling increment
            if King.king_castling_valid(squares, row):
                self.incrs.append( (0, 2) )
            # Queen castling increment
            if King.queen_castling_valid(squares, row):
                self.incrs.append( (0, -2) )

        self.circle_moves(squares, row, col, self.incrs)
    

    @staticmethod
    def king_castling_valid(squares, row):
        right_rook = squares[row][7].piece
        if isinstance(right_rook, Rook):
            if not right_rook.moved:
                for col in range(5, 7):
                    # castling is not possible cause there are pieces in between
                    if squares[row][col].has_piece(): 
                        return False
                return True


    @staticmethod
    def queen_castling_valid(squares, row):
        left_rook = squares[row][0].piece
        if isinstance(left_rook, Rook):
            if not left_rook.moved:
                for col in range(1, 4):
                    # castling is not possible cause there are pieces in between
                    if squares[row][col].has_piece(): 
                        return False
                return True
