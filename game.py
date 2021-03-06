from enum import Enum
from minimax import Minimax


class State(Enum):
    BLACK = 'black'
    WHITE = 'white'
    EMPTY = 'empty'


class Game:
    def __init__(self):
        self.positions = {
            1: (133, 100),
            2: (400, 100),
            3: (666, 100),
            4: (222, 200),
            5: (400, 200),
            6: (578, 200),
            7: (310, 300),
            8: (400, 300),
            9: (490, 300),
            10: (400, 400),
            11: (310, 500),
            12: (400, 500),
            13: (490, 500),
            14: (222, 600),
            15: (400, 600),
            16: (578, 600),
            17: (133, 700),
            18: (400, 700),
            19: (666, 700)
        }

        self.interaction = []

        self.board = {
            1: State.BLACK,
            2: State.BLACK,
            3: State.BLACK,
            4: State.BLACK,
            5: State.BLACK,
            6: State.BLACK,
            7: State.BLACK,
            8: State.BLACK,
            9: State.BLACK,
            10: State.EMPTY,
            11: State.WHITE,
            12: State.WHITE,
            13: State.WHITE,
            14: State.WHITE,
            15: State.WHITE,
            16: State.WHITE,
            17: State.WHITE,
            18: State.WHITE,
            19: State.WHITE
        }

        self.white_turn = True
        self.game_over = False
        self.white_wins = False
        self.black_wins = False

        self.Max = -1000
        self.pos = 0
        self.available_moves = {
            1: [2, 4],
            2: [1, 3, 5],
            3: [2, 6],
            4: [1, 5, 7],
            5: [2, 4, 6, 8],
            6: [3, 5, 9],
            7: [4, 8, 10],
            8: [5, 7, 9, 10],
            9: [6, 8, 10],
            10: [7, 8, 9, 11, 12, 13],
            11: [14, 12, 10],
            12: [15, 13, 11, 10],
            13: [16, 12, 10],
            14: [17, 15, 11],
            15: [18, 16, 14, 12],
            16: [19, 15, 13],
            17: [18, 14],
            18: [19, 17, 15],
            19: [18, 16]
        }

        self.available_captures = {
            1: [3, 7],
            2: [8],
            3: [1, 9],
            4: [6, 10],
            5: [10],
            6: [4, 10],
            7: [1, 9, 13],
            8: [2, 12],
            9: [3, 7, 11],
            10: [4, 5, 6, 14, 15, 16],
            11: [9, 13, 17],
            12: [8, 18],
            13: [7, 11, 19],
            14: [10, 16],
            15: [10],
            16: [10, 14],
            17: [11, 19],
            18: [12],
            19: [13, 17]
        }
        self.list_of_leaves = []

    def find_common_element(self, list1, list2):
        for e1 in list1:
            for e2 in list2:
                if e1 == e2:
                    return e1
        return False

    def is_interactive(self, mouse_position):
        for i in range(1, 20):
            x_min = self.positions[i][0] - 40
            x_max = self.positions[i][0] + 40
            y_min = self.positions[i][1] - 40
            y_max = self.positions[i][1] + 40

            if mouse_position[0] >= x_min and mouse_position[0] <= x_max and mouse_position[1] >= y_min \
                and mouse_position[1] <= y_max:
                return i

    def check_pawn_captures(self, opponent_state, my_position):
        for element in self.available_captures[my_position]:
            if self.board[element] == State.EMPTY:
                capture = self.find_common_element(self.available_moves[my_position], self.available_moves[element])
                if self.board[capture] == opponent_state:
                    return True

        return False

    def minimax_pawn_captures(self, list_of_states, opponent_state, my_position):
        list_full = []
        for element in self.available_captures[my_position]:
            if list_of_states[element] == State.EMPTY:
                hit = self.find_common_element(self.available_moves[my_position], self.available_moves[element])
                if list_of_states[hit] == opponent_state:
                    l = [my_position, hit, element]
                    list_full.append(l)

        return list_full

    def check_possible_captures(self, my_state, opponent_state):
        for index in self.board:
            if self.board[index] == my_state:
                for el in self.available_captures[index]:
                    if self.board[el] == State.EMPTY:
                        hit = self.find_common_element(self.available_moves[index], self.available_moves[el])

                        if self.board[hit] == opponent_state:
                            return True

        return False

    def get_captures(self, list_of_states, my_state, opponent_state):
        list_full = []
        for index in list_of_states:
            if list_of_states[index] == my_state:
                for el in self.available_captures[index]:
                    if list_of_states[el] == State.EMPTY:
                        hit = self.find_common_element(self.available_moves[index], self.available_moves[el])

                        if list_of_states[hit] == opponent_state:
                            l = [index, hit, el]
                            list_full.append(l)

        return list_full

    def get_moves(self, list_of_states, my_state):
        list_of_moves = []
        for index in list_of_states:
            if list_of_states[index] == my_state:
                for el in self.available_moves[index]:
                    if list_of_states[el] == State.EMPTY:
                        l = [index, el]
                        list_of_moves.append(l)

        return list_of_moves

    @staticmethod
    def count_pawns(list_of_states, given_state):
        counter = 0
        for state in list_of_states:
            if list_of_states[state] == given_state:
                counter += 1

        return counter

    def minimax(self, list_of_states, depth, actual_state, parent, alpha, beta):
        if actual_state == State.WHITE:
            opponent_state = State.BLACK
        elif actual_state == State.BLACK:
            opponent_state = State.WHITE

        white_pawns_counter = self.count_pawns(list_of_states, State.WHITE)
        black_pawns_counter = self.count_pawns(list_of_states, State.BLACK)
        evaluation = black_pawns_counter - white_pawns_counter

        if actual_state == State.WHITE:
            alpha = min(alpha, evaluation)
        if actual_state == State.BLACK:
            beta = max(beta, evaluation)

        possible_captures = self.get_captures(list_of_states, actual_state, opponent_state)
        possible_moves = self.get_moves(list_of_states, actual_state)
        leaf = Minimax(depth, list_of_states.copy(), possible_captures, possible_moves, parent, alpha, beta)
        self.list_of_leaves.append(leaf)
        if depth > 0:
            if possible_captures:
                for capture in leaf.captures:
                    if alpha >= beta:
                        break

                    self.minimax(self.minimax_capture(capture, list_of_states.copy(), actual_state, opponent_state),
                                 depth - 1, opponent_state, leaf, alpha, beta)

            if possible_captures == [] and possible_moves:
                for move in leaf.moves:
                    if alpha >= beta:
                        break

                    self.minimax(self.minimax_move(move, list_of_states.copy(), actual_state), depth - 1,
                                 opponent_state, leaf, alpha, beta)

            if possible_moves == [] and possible_captures == []:
                white_pawns_counter = self.count_pawns(list_of_states, State.WHITE)
                black_pawns_counter = self.count_pawns(list_of_states, State.BLACK)
                evaluation = black_pawns_counter - white_pawns_counter
                if evaluation > self.Max:
                    self.Max = evaluation
                    while leaf.parent.parent != 0:
                        leaf = leaf.parent
                    self.pos = leaf.board
        else:
            white_pawns_counter = self.count_pawns(list_of_states, State.WHITE)
            black_pawns_counter = self.count_pawns(list_of_states, State.BLACK)
            evaluation = black_pawns_counter - white_pawns_counter
            if evaluation > self.Max:
                self.Max = evaluation
                while leaf.parent.parent != 0:
                    leaf = leaf.parent
                self.pos = leaf.board

    def minimax_capture(self, capture_list, list_of_states, actual_state, opponent_state):
        list_of_states[capture_list[0]] = State.EMPTY
        list_of_states[capture_list[1]] = State.EMPTY
        list_of_states[capture_list[2]] = actual_state
        c_l = self.minimax_pawn_captures(list_of_states, opponent_state, capture_list[2])
        if not c_l:
            return list_of_states
        else:
            for cap in c_l:
                self.minimax_capture(cap, list_of_states, actual_state, opponent_state)
            return list_of_states

    @staticmethod
    def minimax_move(moves_list, list_of_states, actual_state):
        list_of_states[moves_list[0]] = State.EMPTY
        list_of_states[moves_list[1]] = actual_state
        return list_of_states

    def check_win_condition(self, given_state):
        counter = 0
        for x in self.board:
            if self.board[x] == given_state:
                counter += 1

        if counter == 0:
            return True
        else:
            return False

    def capture(self):
        hit_pawn = self.find_common_element(self.available_moves[self.interaction[0]], self.available_moves[self.interaction[1]])
        self.board[hit_pawn] = State.EMPTY
        self.board[self.interaction[1]] = self.board[self.interaction[0]]
        self.board[self.interaction[0]] = State.EMPTY

    def move(self):
        self.board[self.interaction[1]] = self.board[self.interaction[0]]
        self.board[self.interaction[0]] = State.EMPTY
        self.white_turn = not self.white_turn
        self.interaction.clear()

    def add_interactions(self, pos):
        if self.white_turn:
            if (len(self.interaction)) == 0 and self.board[pos] == State.WHITE:
                self.interaction.append(pos)

            elif (len(self.interaction)) == 1 and self.board[pos] != State.EMPTY:
                self.interaction.clear()

            elif (len(self.interaction)) == 1 and self.board[pos] == State.EMPTY:
                self.interaction.append(pos)

                if self.check_possible_captures(State.WHITE, State.BLACK):
                    if self.interaction[1] in self.available_moves[self.interaction[0]]:
                        self.interaction.clear()

                    elif (self.interaction[1] not in self.available_moves[self.interaction[0]])\
                            and ((self.interaction[1] in self.available_captures[self.interaction[0]])
                                 and (self.board[self.find_common_element(self.available_moves[self.interaction[0]],
                                                                          self.available_moves[self.interaction[1]])] == State.BLACK)):
                        self.capture()

                        if self.check_pawn_captures(State.BLACK, self.interaction[1]):
                            self.interaction.clear()
                        else:
                            self.white_turn = False
                            self.interaction.clear()
                    else:
                        self.interaction.clear()
                else:
                    if self.interaction[1] in self.available_moves[self.interaction[0]]:
                        self.move()

                    elif (self.interaction[1] not in self.available_moves[self.interaction[0]]) \
                            and ((self.interaction[1] in self.available_captures[self.interaction[0]])
                                 and (self.board[self.find_common_element(self.available_moves[self.interaction[0]],
                                                                          self.available_moves[
                                                                           self.interaction[1]])] == State.BLACK)):
                        self.capture()

                        if self.check_pawn_captures(State.BLACK, self.interaction[1]):
                            self.interaction.clear()
                        else:
                            self.white_turn = False
                    else:
                        self.interaction.clear()
                if self.check_win_condition(State.BLACK):
                    self.white_wins = True
                    self.game_over = True

        elif not self.white_turn:
            self.black_turn()
            if self.check_win_condition(State.WHITE):
                self.black_wins = True
                self.game_over = True

    def black_turn(self):
        self.minimax(self.board, 6, State.BLACK, 0, -1000, 1000)
        self.board = self.pos
        self.Max = -100
        self.white_turn = True
