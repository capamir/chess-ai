import pygame
import sys

from src.conf.const import WIDTH, HEIGHT, SQSIZE
from src.game import Game
from src.board.square import Square
from src.movement.move import Move


class Main:
    def __init__(self):
        size = (WIDTH, HEIGHT)
        pygame.init()
        self.screen = pygame.display.set_mode(size)
        pygame.display.set_caption("Chess")
        self.game = Game(self.screen)

    def clicked_event(self):
            board = self.game.board
            
            # click event
            for event in pygame.event.get():
                # clicked
                if event.type == pygame.MOUSEBUTTONDOWN:
                    self.mouse_clicked(board ,event)

                # mouse motion 
                elif event.type == pygame.MOUSEMOTION:
                    self.mouse_motion(event)

                # click release 
                elif event.type == pygame.MOUSEBUTTONUP:
                    self.mouse_released(board, event)

                # key press
                elif event.type == pygame.KEYDOWN:
                    # changing themes
                    if event.key == pygame.K_t:
                        self.game.change_theme()

                # quit application
                elif event.type == pygame.QUIT:
                    self.quit_app()

    def show_board(self, moves=True, hover=False):
        self.game.show_bg()
        self.game.show_last_move()
        if moves:
            self.game.show_moves()
        self.game.show_pieces()
        if hover:
            self.game.show_hover()

    def mouse_clicked(self, board, event):
        dragger = self.game.dragger

        dragger.update_mouse_pos(event.pos)

        clicked_row = dragger.mouseY // SQSIZE
        clicked_col = dragger.mouseX // SQSIZE
        
        # if clicked square has a piece
        if board.squares[clicked_row][clicked_col].has_piece():
            piece = board.squares[clicked_row][clicked_col].piece
            # valid piece (color)?
            if piece.color == self.game.next_player:
                board.calc_moves(piece, clicked_row, clicked_col)
                dragger.save_initial(event.pos)
                dragger.draged_piece(piece)
                
                self.show_board()

    def mouse_motion(self, event):
        dragger = self.game.dragger
        motion_row = event.pos[1] // SQSIZE
        motion_col = event.pos[0] // SQSIZE
        self.game.set_hover(motion_row, motion_col)
        
        if dragger.dragging:
            dragger.update_mouse_pos(event.pos)
            self.show_board(hover=True)
            dragger.update_blit(self.game.surface)

    def mouse_released(self, board, event):
        dragger = self.game.dragger
        if dragger.dragging:
            # released position
            dragger.update_mouse_pos(event.pos)
            released_row = dragger.mouseY // SQSIZE
            released_col = dragger.mouseX // SQSIZE
            # create possible move
            initial = Square(dragger.initial_row, dragger.initial_col)
            final = Square(released_row, released_col) #released square
            move = Move(initial, final)

            # valid move ?
            if board.valid_move(dragger.piece, move):
                captured = board.squares[released_row][released_col].has_piece()
                # move the piece
                board.move(dragger.piece, move)
                # play move sound
                if captured: # capture sound
                    self.game.sound_effect(captured=True)
                else: # move sound
                    self.game.sound_effect()

                # show methods 
                self.show_board(False)
                # next turn
                self.game.next_turn()

            dragger.undrag_piece()

    def quit_app(self):
        pygame.quit()
        sys.exit()

    def mainloop(self):
        game = self.game
        dragger = self.game.dragger

        while True:
            self.show_board(hover=True)

            if dragger.dragging:
                dragger.update_blit(game.surface)
            
            self.clicked_event()
            
            pygame.display.update()

main = Main()
main.mainloop()
