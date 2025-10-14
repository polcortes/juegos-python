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
    def __init__(self, message: str):
        super().__init__(message)

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

def get_cell(who="X"):
    idx = input("¿Qué casilla quieres marcar? (En el tablero de la derecha se muestran los índices de cada casilla)")

    try:
        idx = int(idx)

        if idx < 0 or idx > 8:
            raise IndexError

        if board[idx] != "·":
            raise AlreadyMarkedCellError
    except ValueError:
        print("Carácter inválido...")
        get_cell()
    except IndexError:
        print("Índice fuera de los límites...")
        get_cell()
    except AlreadyMarkedCellError:
        print("Esa casilla ya ha sido marcada...")

def play():
    rounds = 1
    while True:
        print(f"--- RONDA {rounds} ----------------------------------")
        print("Turno de Jugador 1 (X)")
        print_board()
        idx = input("¿Qué casilla quieres marcar?")
        


if __name__ == "__main__":
    play()
    