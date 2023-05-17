from src.conf.const import COLS, ROWS
from .square import Square
from .piece import Pawn, Rook, Knight, Bishop, King, Queen
from src.movement.move import Move


class Board:
    def __init__(self):
        self.squares = [ [0]*ROWS for _ in range(COLS) ]
        self.last_move = None
        self.moves = []
        self._create()
        self._add_piece('white')
        self._add_piece('black')

    def move(self, piece, move):
        initial = move.initial
        final = move.final
        # cunsole move update
        self.squares[initial.row][initial.col].piece = None
        self.squares[final.row][final.col].piece = piece

        # pawn promotion
        if isinstance(piece, Pawn):
            self.check_promotion(piece, final)
        
        # castling
        if isinstance(piece, King):
            if self.is_castling(initial, final):
                self.casting(piece.color, initial, final)

        piece.moved = True # important for pawn move
        piece.clear_moves() # clears the piece's valid moves
        self.last_move = move
        self.moves.append( {piece.name: move} )

    def check_promotion(self, piece, final):
        if final.row == 0 or final.row == 7:
            self.squares[final.row][final.col].piece = Queen(piece.color)
    
    def is_castling(self, initial, final):
        return abs(initial.col - final.col) == 2
    
    def casting(self, color, initial, final):
        # king castling
        if final.col == 6:
            rook_initial_col = 7
            rook_final_col = 5
            
        # queen castling
        elif final.col == 2:
            rook_initial_col = 0
            rook_final_col = 3
            
        self.squares[initial.row][rook_initial_col].piece = None
        self.squares[final.row][rook_final_col].piece = Rook(color)


    def valid_move(self, piece, move):
        return move in piece.valid_moves

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
        # self.squares[3][3] = Square(3, 3, King(color))

        # queen
        self.squares[row_other][3] = Square(row_other, 3, Queen(color))

        # king
        self.squares[row_other][4] = Square(row_other, 4, King(color))

    def calc_moves(self, piece, row, col):
        """
            claculate all the possible (valid) moves of a specific piece on the specific position
        """
        # Pawn's moves
        if isinstance(piece, Pawn): piece.moves(self.squares, row, col)
        # Knight's moves
        elif isinstance(piece, Knight): piece.moves(self.squares, row, col)
        # Queen's moves
        elif isinstance(piece, Queen): piece.moves(self.squares, row, col)
        # Bishop's moves
        elif isinstance(piece, Bishop): piece.moves(self.squares, row, col)
        # Rook's moves
        elif isinstance(piece, Rook): piece.moves(self.squares, row, col)
        # King's moves
        elif isinstance(piece, King): piece.moves(self.squares, row, col)
