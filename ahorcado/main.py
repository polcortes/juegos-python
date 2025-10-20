from utils.console import clear_console
from random import choice

# Constants
WORD_LIST: list[str] = ["aurora", "boreal", "lobo", "luna", "jabali", "cabra", "queso"]


def ask_play_again() -> None:
    play_again = input("¿Quieres jugar otra vez? (y/n): ").lower()
    if play_again == "y":
        play()
    elif play_again == "n":
        print("¡Gracias por jugar!")
    else:
        print("Opción inválida. Por favor, introduce 'y' o 'n'.")
        ask_play_again()


def play() -> None:
    # Game variables
    attempts: int = 6
    word: str = choice(WORD_LIST)
    hidden_word: list[str] = ["_" for _ in word]
    guessed_letters: set[str] = set()
    failed_letters: set[str] = set()

    # Main game loop
    while attempts > 0:
        clear_console()
        print(" ".join(hidden_word))
        print(f"\nIntentos restantes: {attempts}")
        if failed_letters:
            print(f"Letras falladas: {' '.join(sorted(failed_letters))}")
        guess = input("Adivina una letra: ").lower()

        if len(guess) != 1 or not guess.isalpha():
            print("Por favor, introduce una sola letra.")
            continue

        if guess in guessed_letters or guess in failed_letters:
            print("Ya has intentado esa letra.")
            continue

        guessed_letters.add(guess)

        if guess in word:
            print("¡Correcto!")
            for i, letter in enumerate(word):
                if letter == guess:
                    hidden_word[i] = guess
        else:
            print("¡Incorrecto!")
            failed_letters.add(guess)
            attempts -= 1

        if "_" not in hidden_word:
            print(" ".join(hidden_word))
            print("¡Enhorabuena! ¡Has ganado!")
            break
    else:
        print("Game over!")

    ask_play_again()


if __name__ == "__main__":
    play()
