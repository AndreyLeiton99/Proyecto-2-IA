import random
import os
from minimax import Minimax


class Game:
    def __init__(self):
        self.round = 1
        self.finished = False
        self.winner = None

        os.system('cls' if os.name == 'nt' else 'clear')
        print("Welcome to Connect 4™!")
        self.players = [None, None]
        self.colors = ["x", "o"]
        self.setup_players()

        self.turn = self.players[0]
        self.board = [[' ' for _ in range(7)] for _ in range(6)]

    def setup_players(self):
        for i in range(2):
            while self.players[i] is None:
                choice = input(f"Should Player {i + 1} be a Human or a Computer? (H/C): ")
                if choice.lower() == "human" or choice.lower() == "h":
                    name = input(f"What is Player {i + 1}'s name? ")
                    self.players[i] = Player(name, self.colors[i])
                elif choice.lower() == "computer" or choice.lower() == "c":
                    name = input(f"What is Player {i + 1}'s name? ")
                    difficulty = int(input("Enter difficulty for this AI (1 - 4): "))
                    self.players[i] = AIPlayer(name, self.colors[i], difficulty + 1)
                else:
                    print("Invalid choice, please try again.")

        print(f"{self.players[0].name} will be {self.colors[0]}")
        print(f"{self.players[1].name} will be {self.colors[1]}")

    def new_game(self):
        self.round = 1
        self.finished = False
        self.winner = None

        self.turn = self.players[0]
        self.board = [[' ' for _ in range(7)] for _ in range(6)]

    def switch_turn(self):
        self.turn = self.players[1] if self.turn == self.players[0] else self.players[0]
        self.round += 1

    def next_move(self):
        if self.round > 42:
            self.finished = True
            return

        move = self.turn.move(self.board)

        for i in range(6):
            if self.board[i][move] == ' ':
                self.board[i][move] = self.turn.color
                self.switch_turn()
                self.check_for_fours()
                self.print_state()
                return

        print("Invalid move (column is full)")

    def check_for_fours(self):
        for i in range(6):
            for j in range(7):
                if self.board[i][j] != ' ':
                    if self.vertical_check(i, j) or self.horizontal_check(i, j) or self.diagonal_check(i, j)[0]:
                        print(self.vertical_check(i, j), self.horizontal_check(i, j), self.diagonal_check(i, j))
                        self.finished = True
                        return

    def vertical_check(self, row, col):
        consecutive_count = 0
        for i in range(row, 6):
            if self.board[i][col].lower() == self.board[row][col].lower():
                consecutive_count += 1
            else:
                break
        return consecutive_count >= 4

    def horizontal_check(self, row, col):
        consecutive_count = 0
        for j in range(col, 7):
            if self.board[row][j].lower() == self.board[row][col].lower():
                consecutive_count += 1
            else:
                break
        return consecutive_count >= 4

    def diagonal_check(self, row, col):
        four_in_a_row = False
        count = 0
        slope = None

        # check for diagonals with positive slope
        consecutive_count = 0
        j = col
        for i in range(row, 6):
            if j > 6:
                break
            elif self.board[i][j].lower() == self.board[row][col].lower():
                consecutive_count += 1
            else:
                break
            j += 1  # increment column when row is incremented

        if consecutive_count >= 4:
            count += 1
            slope = 'positive'
            if self.players[0].color.lower() == self.board[row][col].lower():
                self.winner = self.players[0]
            else:
                self.winner = self.players[1]

        # check for diagonals with negative slope
        consecutive_count = 0
        j = col
        for i in range(row, -1, -1):
            if j > 6:
                break
            elif self.board[i][j].lower() == self.board[row][col].lower():
                consecutive_count += 1
            else:
                break
            j += 1  # increment column when row is decremented

        if consecutive_count >= 4:
            count += 1
            slope = 'negative'
            if self.players[0].color.lower() == self.board[row][col].lower():
                self.winner = self.players[0]
            else:
                self.winner = self.players[1]

        if count > 0:
            four_in_a_row = True
        if count == 2:
            slope = 'both'

        return four_in_a_row, slope

    def diagonal_check_direction(self, row, col, row_step, col_step):
        consecutive_count = 0
        i, j = row, col
        while 0 <= i < 6 and 0 <= j < 7:
            if self.board[i][j].lower() == self.board[row][col].lower():
                consecutive_count += 1
            else:
                break
            i += row_step
            j += col_step
        return consecutive_count >= 4

    def find_fours(self):
        for i in range(6):
            for j in range(7):
                if self.board[i][j] != ' ':
                    if self.vertical_check(i, j):
                        self.highlight_four(i, j, 'vertical')
                    if self.horizontal_check(i, j):
                        self.highlight_four(i, j, 'horizontal')
                    diag_fours, slope = self.diagonal_check(i, j)
                    if diag_fours:
                        self.highlight_four(i, j, 'diagonal', slope)

    def highlight_four(self, row, col, direction, slope=None):
        if direction == 'vertical':
            for i in range(4):
                self.board[row + i][col] = self.board[row + i][col].upper()
        elif direction == 'horizontal':
            for i in range(4):
                self.board[row][col + i] = self.board[row][col + i].upper()
        elif direction == 'diagonal':
            if slope == 'positive' or slope == 'both':
                for i in range(4):
                    self.board[row + i][col + i] = self.board[row + i][col + i].upper()
            elif slope == 'negative' or slope == 'both':
                for i in range(4):
                    self.board[row - i][col + i] = self.board[row - i][col + i].upper()
        else:
            print("Error - Cannot enunciate four-of-a-kind")

    def print_state(self):
        os.system('cls' if os.name == 'nt' else 'clear')
        print("Connect 4™!")
        print("Round:", self.round)
        for i in range(5, -1, -1):
            print("\t", end="")
            for j in range(7):
                print("| " + str(self.board[i][j]), end=" ")
            print("|")
        print("\t  1   2   3   4   5   6   7 ")

        if self.finished:
            print("Game Over!")
            if self.winner is not None:
                print(f"{self.winner.name} is the winner")
            else:
                print("Game was a draw")


class Player:
    def __init__(self, name, color):
        self.name = name
        self.color = color

    def move(self, state):
        print(f"{self.name}'s turn. {self.name} is {self.color}")
        column = None
        while column is None:
            try:
                choice = int(input("Enter a move (by column number): ")) - 1
            except ValueError:
                choice = None
            if 0 <= choice <= 6:
                column = choice
            else:
                print("Invalid choice, try again")
        return column


class AIPlayer(Player):
    def __init__(self, name, color, difficulty=5):
        super().__init__(name, color)
        self.difficulty = difficulty

    def move(self, state):
        print(f"{self.name}'s turn. {self.name} is {self.color}")
        m = Minimax(state)
        best_move, _ = m.best_move(self.difficulty, state, self.color)
        return best_move
