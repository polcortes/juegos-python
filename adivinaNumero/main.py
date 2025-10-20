from random import randint
from utils.console import clear_console

def ask_play_again() -> None:
    play_again = input("¿Quieres jugar otra vez? (y/n): ").lower()
    if play_again == "y":
        play()
    elif play_again == "n":
        print("¡Gracias por jugar!")
    else:
        print("Opción inválida. Por favor, introduce 'y' o 'n'.")
        ask_play_again()

def play():
    clear_console()
    number_to_guess = randint(1, 10)
    attempts = 3

    while attempts > 0:
        guess = input(f"Adivina el número entre 1 y 10 (intentos restantes: {attempts}): ")
        if not guess.isdigit():
            print("Por favor, introduce un número válido.")
            continue

        guess_number = int(guess)

        if guess_number == number_to_guess:
            print("¡Felicidades! ¡Has adivinado el número!")
            break
        else:
            print("Número incorrecto.")
            attempts -= 1
            print(f"El número secreto es {'mayor ' if guess_number < number_to_guess else 'menor '} que {guess_number}.")
    else:
        if attempts == 0:
            print(f"¡Has perdido! El número era {number_to_guess}.")

    ask_play_again()

if __name__ == "__main__":
    play()
