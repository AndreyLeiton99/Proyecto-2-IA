import random


class Minimax:
    def __init__(self, board):
        self.board = [row[:] for row in board]
        self.colors = ["x", "o"]

    def best_move(self, depth, state, curr_player):
        opp_player = self.colors[1 - self.colors.index(curr_player)]

        legal_moves = {}
        for col in range(7):
            if self.is_legal_move(col, state):
                temp = self.make_move(state, col, curr_player)
                legal_moves[col] = -self.search(depth - 1, temp, opp_player)

        best_alpha = float('-inf')
        best_move = None

        for move, alpha in legal_moves.items():
            if alpha >= best_alpha:
                best_alpha = alpha
                best_move = move

        return best_move, best_alpha

    def search(self, depth, state, curr_player):
        opp_player = self.colors[1 - self.colors.index(curr_player)]

        legal_moves = [self.make_move(state, col, curr_player) for col in range(7) if self.is_legal_move(col, state)]

        if depth == 0 or not legal_moves or self.game_over(state):
            return self.value(state, curr_player)

        alpha = float('-inf')

        for child in legal_moves:
            alpha = max(alpha, -self.search(depth - 1, child, opp_player))

        return alpha

    def is_legal_move(self, column, state):
        return any(row[column] == ' ' for row in state)

    def game_over(self, state):
        return self.check_for_streak(state, self.colors[0], 4) >= 1 or self.check_for_streak(state, self.colors[1],
                                                                                             4) >= 1

    def make_move(self, state, column, color):
        temp = [row[:] for row in state]
        for row in range(6):
            if temp[row][column] == ' ':
                temp[row][column] = color
                return temp

    def value(self, state, color):
        o_color = self.colors[1 - self.colors.index(color)]

        my_fours = self.check_for_streak(state, color, 4)
        my_threes = self.check_for_streak(state, color, 3)
        my_twos = self.check_for_streak(state, color, 2)
        opp_fours = self.check_for_streak(state, o_color, 4)

        if opp_fours > 0:
            return -100000
        else:
            return (my_fours * 100000) + (my_threes * 100) + my_twos

    def check_for_streak(self, state, color, streak):
        count = 0
        for row in range(6):
            for col in range(7):
                if state[row][col].lower() == color.lower():
                    count += self.vertical_streak(row, col, state, streak)
                    count += self.horizontal_streak(row, col, state, streak)
                    count += self.diagonal_check(row, col, state, streak)
        return count

    def vertical_streak(self, row, col, state, streak):
        consecutive_count = 0
        for i in range(row, 6):
            if state[i][col].lower() == state[row][col].lower():
                consecutive_count += 1
            else:
                break
        return 1 if consecutive_count >= streak else 0

    def horizontal_streak(self, row, col, state, streak):
        consecutive_count = 0
        for j in range(col, 7):
            if state[row][j].lower() == state[row][col].lower():
                consecutive_count += 1
            else:
                break
        return 1 if consecutive_count >= streak else 0

    def diagonal_check(self, row, col, state, streak):
        total = 0
        total += self.diagonal_check_direction(row, col, state, streak, 1, 1)
        total += self.diagonal_check_direction(row, col, state, streak, 1, -1)
        total += self.diagonal_check_direction(row, col, state, streak, -1, 1)
        total += self.diagonal_check_direction(row, col, state, streak, -1, -1)
        return total

    def diagonal_check_direction(self, row, col, state, streak, row_step, col_step):
        consecutive_count = 0
        i, j = row, col
        while 0 <= i < 6 and 0 <= j < 7:
            if state[i][j].lower() == state[row][col].lower():
                consecutive_count += 1
            else:
                break
            i += row_step
            j += col_step
        return 1 if consecutive_count >= streak else 0

# Example usage:
# board = [[' ' for _ in range(7)] for _ in range(6)]
# minimax = Minimax(board)
# best_move, best_alpha = minimax.best_move(5, board, 'x')
# print(f"Best Move: {best_move}, Best Alpha: {best_alpha}")
