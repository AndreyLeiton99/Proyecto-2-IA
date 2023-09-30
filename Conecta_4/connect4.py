import random
import os
from minimax import Minimax
from alphaBeta import AlphaBeta


class Game:
    def __init__(self):
        self.ronda = 1
        self.terminado = False
        self.Ganador = None

        # para limpiar la consola
        os.system('cls' if os.name == 'nt' else 'clear')
        print("Bienvenido a Conecta 4!")
        self.jugadores = [None, None]
        self.fichas = ["x", "o"]

        self.setup_jugadores()

        self.turno = self.jugadores[0]
        self.tablero = [[' ' for _ in range(7)] for _ in range(6)]

    def setup_jugadores(self):
        for i in range(2):
            while self.jugadores[i] is None:
                eleccion = input(
                    f"Indique si el Jugador {i + 1} va a ser Humano o IA? (H/IA): ")
                if eleccion.lower() == "humano" or eleccion.lower() == "h":
                    nombre = input(f"Digite el nombre del Jugador {i + 1} ")
                    self.jugadores[i] = Player(nombre, self.fichas[i])
                elif eleccion.lower() == "ia" or eleccion.lower() == "i":
                    nombre = input(f"Digite el nombre del Jugador {i + 1} ")
                    dificultad = int(
                        input("Seleccione la dificultad para esta IA (1 - 4): "))

                    opc = None
                    right = False
                    while not right:
                        opc = int(input("Ahora seleccione el algoritmo que desea utilizar: \n1- Minimax \n2- Alpha-Beta"
                                        "\n ->"))
                        right = True if opc == 1 or opc == 2 else False

                    algoritmo = "minimax" if opc == 1 else "alpha"
                    self.jugadores[i] = AIPlayer(
                        nombre, self.fichas[i], algoritmo, dificultad + 1)
                else:
                    print("Invalid choice, please try again.")

        print(f"{self.jugadores[0].nombre} va a ser {self.fichas[0]}")
        print(f"{self.jugadores[1].nombre} va a ser {self.fichas[1]}")

    def nuevo_juego(self):
        self.ronda = 1
        self.terminado = False
        self.Ganador = None

        self.turno = self.jugadores[0]
        self.tablero = [[' ' for _ in range(7)] for _ in range(6)]

    def cambio_turno(self):
        self.turno = self.jugadores[1] if self.turno == self.jugadores[0] else self.jugadores[0]
        self.ronda += 1

    def sig_movimiento(self):
        if self.ronda > 42:
            self.terminado = True
            return

        movimiento = self.turno.move(self.tablero)

        for i in range(6):
            if self.tablero[i][movimiento] == ' ':
                self.tablero[i][movimiento] = self.turno.ficha
                self.cambio_turno()
                self.check_for_fours()
                self.mostrar_estado()
                return

        print("Movimiento no permitido, la columna se encuentra llena")

    def check_for_fours(self):
        for i in range(6):
            for j in range(7):
                if self.tablero[i][j] != ' ':
                    if self.vertical_check(i, j) or self.horizontal_check(i, j) or self.diagonal_check(i, j)[0]:
                        print(self.vertical_check(i, j), self.horizontal_check(
                            i, j), self.diagonal_check(i, j))
                        self.terminado = True
                        return

    def vertical_check(self, row, col):
        consecutive_count = 0
        for i in range(row, 6):
            if self.tablero[i][col].lower() == self.tablero[row][col].lower():
                consecutive_count += 1
            else:
                break
        return consecutive_count >= 4

    def horizontal_check(self, row, col):
        consecutive_count = 0
        for j in range(col, 7):
            if self.tablero[row][j].lower() == self.tablero[row][col].lower():
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
            elif self.tablero[i][j].lower() == self.tablero[row][col].lower():
                consecutive_count += 1
            else:
                break
            j += 1  # increment column when row is incremented

        if consecutive_count >= 4:
            count += 1
            slope = 'positive'
            if self.jugadores[0].ficha.lower() == self.tablero[row][col].lower():
                self.Ganador = self.jugadores[0]
            else:
                self.Ganador = self.jugadores[1]

        # check for diagonals with negative slope
        consecutive_count = 0
        j = col
        for i in range(row, -1, -1):
            if j > 6:
                break
            elif self.tablero[i][j].lower() == self.tablero[row][col].lower():
                consecutive_count += 1
            else:
                break
            j += 1  # increment column when row is decremented

        if consecutive_count >= 4:
            count += 1
            slope = 'negative'
            if self.jugadores[0].ficha.lower() == self.tablero[row][col].lower():
                self.Ganador = self.jugadores[0]
            else:
                self.Ganador = self.jugadores[1]

        if count > 0:
            four_in_a_row = True
        if count == 2:
            slope = 'both'

        return four_in_a_row, slope

    def diagonal_check_direction(self, row, col, row_step, col_step):
        consecutive_count = 0
        i, j = row, col
        while 0 <= i < 6 and 0 <= j < 7:
            if self.tablero[i][j].lower() == self.tablero[row][col].lower():
                consecutive_count += 1
            else:
                break
            i += row_step
            j += col_step
        return consecutive_count >= 4

    def encontrar_4(self):
        for i in range(6):
            for j in range(7):
                if self.tablero[i][j] != ' ':
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
                self.tablero[row + i][col] = self.tablero[row + i][col].upper()
        elif direction == 'horizontal':
            for i in range(4):
                self.tablero[row][col + i] = self.tablero[row][col + i].upper()
        elif direction == 'diagonal':
            if slope == 'positive' or slope == 'both':
                for i in range(4):
                    self.tablero[row + i][col +
                                          i] = self.tablero[row + i][col + i].upper()
            elif slope == 'negative' or slope == 'both':
                for i in range(4):
                    self.tablero[row - i][col +
                                          i] = self.tablero[row - i][col + i].upper()
        else:
            print("Error - No se pudo encontrar un Conecta 4")

    def mostrar_estado(self):
        # Lista de códigos de fichaa es ANSI para rojo y verde
        codigo_rojo = "\033[1;31;40m"
        codigo_verde = "\033[1;32;40m"
        codigo_azul_negrita = "\033[1;34;40m"
        reset_color = "\033[0m"  # Restablece el ficha a su valor predeterminado

        os.system('cls' if os.name == 'nt' else 'clear')
        print("Conecta 4™!")
        print("Round:", self.ronda)
        for i in range(5, -1, -1):
            print("\t", end="")
            for j in range(7):
                valor = self.tablero[i][j]
                if valor == 'x':
                    # Imprime en verde
                    print(f"| {codigo_verde}{valor}{reset_color}", end=" ")
                elif valor == 'o':
                    # Imprime en rojo
                    print(f"| {codigo_rojo}{valor}{reset_color}", end=" ")
                elif valor == 'X' or valor == 'O':
                    # Imprime en azul negrita
                    print(f"| {codigo_azul_negrita}{valor}{reset_color}", end=" ")
                else:
                    # Sin fichaa
    
                    print(f"| {valor}", end=" ")
            print("|")
        print("\t  1   2   3   4   5   6   7 ")

        if self.terminado:
            print("Game Over!")
            if self.Ganador is not None:
                print(f"{self.Ganador.nombre} es el ganador")
            else:
                print("El juego termina con EMPATE")



class Player:
    def __init__(self, nombre, ficha):
        self.nombre = nombre
        self.ficha = ficha

    def move(self, state):
        print(f"{self.nombre}'s turn. {self.nombre} is {self.ficha}")
        column = None
        while column is None:
            try:
                choice = int(
                    input("Digite el movimiento (por numero de columna): ")) - 1
            except ValueError:
                choice = None
            if 0 <= choice <= 6:
                column = choice
            else:
                print("Columna no existente, digite de nuevo!")
        return column


class AIPlayer(Player):
    def __init__(self, nombre, ficha, algoritmo, difficulty=5):
        super().__init__(nombre, ficha)
        self.difficulty = difficulty
        self.algoritmo = algoritmo

    def move(self, state):
        print(f"Es el turno de {self.nombre}. {self.nombre} es {self.ficha}")

        match self.algoritmo:
            case "minimax":
                m = Minimax(state)
                best_move, _ = m.best_move(self.difficulty, state, self.ficha)
                return best_move
            case "alpha":
                a = AlphaBeta(state)
                best_move, _ = a.best_move(self.difficulty, state, self.ficha, alpha=float('-inf'), beta=float(
                    'inf'))  # alpha y beta se inicializan con esos valores por defecto
                return best_move
            case _:
                print("Algoritmo desconocido, hay problemas.")
