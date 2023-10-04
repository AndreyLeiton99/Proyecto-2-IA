from connect4 import *
import time


def main():
    g = Game()
    g.mostrar_estado()
    jugador_1 = g.jugadores[0]
    jugador_2 = g.jugadores[1]

    estadisticas = [0, 0, 0]

    inicio_tiempo = time.time()

    done = False

    # Check if the game is already finished at the start
    if g.terminado:
        print("El juego ya ha terminado. No se pueden hacer movimientos.")
        return

    while not done:
        while not g.terminado:
            g.sig_movimiento()

        g.encontrar_4()
        g.mostrar_estado()

        if g.Ganador is None:
            estadisticas[2] += 1
        elif g.Ganador == jugador_1:
            estadisticas[0] += 1
        elif g.Ganador == jugador_2:
            estadisticas[1] += 1

        print_stats(jugador_1, jugador_2, estadisticas)
        tiempo_total = time.time() - inicio_tiempo
        print(f"Tiempo total de juego: {tiempo_total} segundos")

        while True:
            reiniciar_juego = input("Desea jugar nuevamente? Si / No: ")

            if reiniciar_juego.lower() == 's' or reiniciar_juego.lower() == 'si':
                g.nuevo_juego()
                g.mostrar_estado()
                # reiniciar el tiempo
                inicio_tiempo = time.time()
                break
            elif reiniciar_juego.lower() == 'n' or reiniciar_juego.lower() == 'no':
                print("Entendido, gracias por jugar!")
                done = True
                break
            else:
                print("Respuesta desconocida. ")


def print_stats(jugador_1, jugador_2, win_counts):
    print(
        f"{jugador_1.nombre}: {win_counts[0]} victorias, {jugador_2.nombre}: {win_counts[1]} victorias, {win_counts[2]} empate")


if __name__ == "__main__":
    main()
