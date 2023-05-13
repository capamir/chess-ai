from src.const import COLS, ROWS
from .square import Square
from .piece import Pawn, Rook, Knight, Bishop, King, Queen

class Board:
    def __init__(self):
        self.squares = [ [0]*ROWS for _ in range(COLS) ]
        self._create()
        self._add_piece('white')
        self._add_piece('black')


    def _create(self):
        """
            creates the squares for the game board
        """
        for row in range(ROWS):
            for col in range(COLS):
                self.squares[row][col] = Square(row, col)

    def _add_piece(self, color):
        """
            create the pieces in thier original position at the beginning of the game
        """
        row_pawn, row_other = (6, 7) if color == 'white' else (1, 0)

        # pawns
        for col in range(COLS):
            self.squares[row_pawn][col] = Square(row_pawn, col, Pawn(color))

        # rocks
        self.squares[row_other][0] = Square(row_other, 0, Rook(color))
        self.squares[row_other][7] = Square(row_other, 7, Rook(color))

        # knights
        self.squares[row_other][1] = Square(row_other, 1, Knight(color))
        self.squares[row_other][6] = Square(row_other, 6, Knight(color))

        # bishops
        self.squares[row_other][2] = Square(row_other, 2, Bishop(color))
        self.squares[row_other][5] = Square(row_other, 5, Bishop(color))

        # queen
        self.squares[row_other][3] = Square(row_other, 3, Queen(color))

        # king
        self.squares[row_other][4] = Square(row_other, 4, King(color))

    def calc_moves(self, piece, row, col):
        """
            claculate all the possible (valid) moves of a specific piece on the specific position
        """
