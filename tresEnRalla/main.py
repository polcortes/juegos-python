from utils.console import clear_console


WINNER_COMBOS: list[list[int]] = [
    [0, 1, 2],
    [3, 4, 5],
    [6, 7, 8],
    [0, 3, 6],
    [1, 4, 7],
    [2, 5, 8],
    [0, 4, 8],
    [2, 4, 6],
]


class AlreadyMarkedCellError(Exception):
    def __init__(self):
        super().__init__()


PLAYER_ONE_SYMBOL = "X"
PLAYER_TWO_SYMBOL = "O"

board = ["·", "·", "·", "·", "·", "·", "·", "·", "·"]


def print_board():
    print("  ".join(board[:3]), end="")
    print((" " * 10) + "0  1  2")

    print("  ".join(board[3:6]), end="")
    print((" " * 10) + "3  4  5")

    print("  ".join(board[6:]), end="")
    print((" " * 10) + "6  7  8")


def check_winner(mark):
    for combo in WINNER_COMBOS:
        if all(board[i] == mark for i in combo):
            return True
    return False


def get_cell(mark: str):
    idx = input(
        "¿Qué casilla quieres marcar? (En el tablero de la derecha se muestran los índices de cada casilla)"
    )

    try:
        idx = int(idx)

        if idx < 0 or idx > 8:
            raise IndexError

        if board[idx] != "·":
            raise AlreadyMarkedCellError

        board[idx] = mark
    except ValueError:
        print("Carácter inválido...")
        get_cell(mark)
    except IndexError:
        print("Índice fuera de los límites...")
        get_cell(mark)
    except AlreadyMarkedCellError:
        print("Esa casilla ya ha sido marcada...")


def ask_play_again():
    response = input("¿Quieres jugar otra vez? (y/Y = Sí, n/N = No): ").strip().lower()
    if response == "y":
        play()
    elif response == "n":
        print("Gracias por jugar. ¡Hasta la próxima!")
    else:
        print("Respuesta inválida. Por favor, responde con 's' o 'n'.")
        ask_play_again()


def play():
    global board
    board = ["·", "·", "·", "·", "·", "·", "·", "·", "·"]
    clear_console()
    while True:
        print("Turno de Jugador 1 (X)")
        print_board()

        get_cell(PLAYER_ONE_SYMBOL)
        if check_winner(PLAYER_ONE_SYMBOL):
            print_board()
            print("¡Ha ganado el Jugador 1!")
            ask_play_again()
            break

        # Si check_winner devuelve False, comprobamos que el tablero siga teniendo casillas libres
        if all(cell != "·" for cell in board):
            print_board()
            print("¡Empate!")
            ask_play_again()
            break

        print("Turno de Jugador 2 (O)")
        print_board()
        get_cell(PLAYER_TWO_SYMBOL)

        if check_winner(PLAYER_TWO_SYMBOL):
            print_board()
            print("¡Ha ganado el Jugador 2!")
            ask_play_again()
            break


if __name__ == "__main__":
    play()
