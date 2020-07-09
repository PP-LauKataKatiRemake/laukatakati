class Minimax():
    def __init__(self, depth, board, captures, moves, parent):
        self.depth = depth
        self.board = board
        self.captures = captures
        self.moves = moves
        self.parent = parent
