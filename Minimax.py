class Minimax():
    def __init__(self, depth, board, captures, moves, parent):
        self.depth = depth
        self.board = board
        self.captures = captures
        self.moves = moves
        self.parent = parent

    def remove_capture_from_list(self):
        self.captures.remove(self.captures[0])

    def remove_move_from_list(self):
        self.moves.remove(self.moves[0])
