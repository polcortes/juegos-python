from random import choice
from utils.console import clear_console


options = ["piedra", "papel", "tijera"]


def ask_play_again() -> None:
    play_again = input("¿Quieres jugar de nuevo? (y/Y = Sí, n/N = No): ").lower()

    if play_again == "y":
        play()
    elif play_again == "n":
        print("¡Gracias por jugar!")
    else:
        print("Opción inválida. Intenta de nuevo...")
        ask_play_again()

def play() -> None:
    clear_console()
    user_option = input("Elige piedra, papel o tijera: ").lower()

    if user_option not in options:
        print("Opción inválida. Intenta de nuevo...")
        return play()

    bot_option = choice(options)
    print(f"El bot eligió {bot_option}")

    if user_option == bot_option:
        print("¡Empate!")
    elif (user_option == "piedra" and bot_option == "tijera") or \
         (user_option == "papel" and bot_option == "piedra") or \
         (user_option == "tijera" and bot_option == "papel"):
        print("¡Ganaste!")
    else:
        print("¡Perdiste!")

    ask_play_again()


if __name__ == "__main__":
    play()
