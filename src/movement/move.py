
class Move:
    def __init__(self, initial, final):
        """
            take the initial and final squares
        """
        self.initial = initial
        self.final = final

    def __eq__(self, other):
        return self.initial == other.initial and self.final == other.final
    
    def __str__(self):
        return f'initial=> ({self.initial.row}, {self.initial.col}) , final=> ({self.final.row}, {self.final.col})'