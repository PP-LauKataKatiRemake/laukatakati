class Minimax():
    def __init__(self, depth, board, captures, moves, parent, alpha, beta):
        self.depth = depth
        self.board = board
        self.captures = captures
        self.moves = moves
        self.parent = parent
        self.alpha = alpha
        self.beta = beta
