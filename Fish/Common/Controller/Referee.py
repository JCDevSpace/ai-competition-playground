import random

class Referee:

    def __init__(self, rows=None, cols=None):
        if not rows:
            rows = random.randint(2, 7)
        if not cols:
            cols = random.randint(2, 7)

        self.board = Board(rows, cols)
        self.generate_board()

        self.board_view = BoardView(self.board)


    def generate_board():
