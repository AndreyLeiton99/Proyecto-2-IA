from connect4 import *


def main():
    g = Game()
    g.print_state()
    player1 = g.players[0]
    player2 = g.players[1]

    stats = [0, 0, 0]

    done = False

    # Check if the game is already finished at the start
    if g.finished:
        print("Game is already finished. No moves can be made.")
        return

    while not done:
        while not g.finished:
            g.next_move()

        g.find_fours()
        g.print_state()

        if g.winner is None:
            stats[2] += 1
        elif g.winner == player1:
            stats[0] += 1
        elif g.winner == player2:
            stats[1] += 1

        print_stats(player1, player2, stats)

        while True:
            reset_game = input("Desea jugar nuevamente? Si / No: ")

            if reset_game.lower() == 's' or reset_game.lower() == 'si':
                g.new_game()
                g.print_state()
                break
            elif reset_game.lower() == 'n' or reset_game.lower() == 'no':
                print("Entendido, gracias por jugar!")
                done = True
                break
            else:
                print("Respuesta desconocida. ")


def print_stats(player1, player2, win_counts):
    print(f"{player1.name}: {win_counts[0]} wins, {player2.name}: {win_counts[1]} wins, {win_counts[2]} ties")


if __name__ == "__main__":
    main()
