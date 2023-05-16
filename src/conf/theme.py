from .color import Color

class Theme:
    def __init__(self, light_bg, dark_bg,
                        light_trace, dark_trace,
                        light_moves, dark_moves):
        
        self.bg = Color(light_bg, dark_bg)
        self.trace = Color(light_trace, dark_trace)
        self.moves = Color(light_moves, dark_moves)
    
    def bg_color(self, row, col):
        return self.bg.light if (row + col) % 2 == 0 else self.bg.dark
    
    def trace_color(self, row, col):
        return self.trace.light if (row + col) % 2 == 0 else self.trace.dark
    
    def moves_color(self, row, col):
        return self.moves.light if (row + col) % 2 == 0 else self.moves.dark