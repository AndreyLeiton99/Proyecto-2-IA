import random
import os
from minimax import Minimax
from alphaBeta import AlphaBeta


class Game:
    def __init__(self):
        self.round = 1
        self.finished = False
        self.winner = None

        # para limpiar la consola
        os.system('cls' if os.name == 'nt' else 'clear')
        print("Bienvenido a Conecta 4!")
        self.players = [None, None]
        self.colors = ["x", "o"]
        self.setup_players()

        self.turn = self.players[0]
        self.board = [[' ' for _ in range(7)] for _ in range(6)]

    def setup_players(self):
        for i in range(2):
            while self.players[i] is None:
                choice = input(f"Indique si el Jugador {i + 1} va a ser Humano o IA? (H/IA): ")
                if choice.lower() == "humano" or choice.lower() == "h":
                    name = input(f"Digite el nombre del Jugador {i + 1} ")
                    self.players[i] = Player(name, self.colors[i])
                elif choice.lower() == "ia" or choice.lower() == "i":
                    name = input(f"Digite el nombre del Jugador {i + 1} ")
                    difficulty = int(input("Seleccione la dificultad para esta IA (1 - 4): "))

                    opc = None
                    right = False
                    while right:
                        opc = int(input("Ahora seleccione el algoritmo que desea utilizar: \n1- Minimax \n2- Alpha-Beta"
                                        "\n ->"))
                        right = True if opc == 1 or opc == 2 else False

                    algorithm = "minimax" if opc == 1 else "alpha"
                    self.players[i] = AIPlayer(name, self.colors[i], algorithm, difficulty + 1)
                else:
                    print("Invalid choice, please try again.")

        print(f"{self.players[0].name} va a ser {self.colors[0]}")
        print(f"{self.players[1].name} va a ser {self.colors[1]}")

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

        print("Movimiento no permitido, la columna se encuentra llena")

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
            print("Error - No se pudo encontrar un Conecta 4")

    def print_state(self):
        os.system('cls' if os.name == 'nt' else 'clear')
        print("Conecta 4™!")
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
                print(f"{self.winner.name} es el ganador")
            else:
                print("El juego termina con EMPATE")


class Player:
    def __init__(self, name, color):
        self.name = name
        self.color = color

    def move(self, state):
        print(f"{self.name}'s turn. {self.name} is {self.color}")
        column = None
        while column is None:
            try:
                choice = int(input("Digite el movimiento (por numero de columna): ")) - 1
            except ValueError:
                choice = None
            if 0 <= choice <= 6:
                column = choice
            else:
                print("Columna no existente, digite de nuevo!")
        return column


class AIPlayer(Player):
    def __init__(self, name, color, algorithm, difficulty=5):
        super().__init__(name, color)
        self.difficulty = difficulty
        self.algorithm = algorithm

    def move(self, state):
        print(f"Es el turno de {self.name}. {self.name} es {self.color}")

        match self.algorithm:
            case "minimax":
                m = Minimax(state)
                best_move, _ = m.best_move(self.difficulty, state, self.color)
                return best_move
            case "alpha":
                a = AlphaBeta(state)
                best_move, _ = a.best_move(self.difficulty, state, self.color, alpha=float('-inf'), beta=float(
                    'inf'))  # alpha y beta se inicializan con esos valores por defecto
                return best_move
            case _:
                print("Algoritmo desconocido, hay problemas.")
