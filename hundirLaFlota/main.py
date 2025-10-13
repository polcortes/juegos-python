from random import shuffle, randint
from typing import TypedDict
from string import ascii_uppercase


ROWS    = 10
COLUMNS = 10

# Estados
EMPTY_STATE  = "empty"
BOAT_STATE   = "boat"
HIT_STATE    = "hit"
FAIL_STATE   = "fail"
SUNK_STATE   = "sunk"

# Símbolos
EMPTY_SYMBOL = "~"
HIT_SYMBOL   = "X"
FAIL_SYMBOL  = "o"
SUNK_SYMBOL  = "#"

ORIENTATION_HORIZONTAL = 0
ORIENTATION_VERTICAL   = 1


class Cell(TypedDict):
    state: str
    boat_id: int | None
    boat_size: int


type BoardType = list[list[Cell]]

player_board: BoardType = []
bot_board: BoardType    = []

def create_empty_cell() -> Cell:
    return {"state": EMPTY_STATE, "boat_id": None, "boat_size": 0}


def create_boat_cell(boat_id: int, boat_size: int) -> Cell:
    return {"state": BOAT_STATE, "boat_id": boat_id, "boat_size": boat_size}


def get_cell_symbol(cell: Cell, hide_boats: bool = False) -> str:
    if cell["state"] == EMPTY_STATE:
        return EMPTY_SYMBOL
    elif cell["state"] == FAIL_STATE:
        return FAIL_SYMBOL
    elif cell["state"] == HIT_STATE:
        return HIT_SYMBOL
    elif cell["state"] == SUNK_STATE:
        return SUNK_SYMBOL
    elif cell["state"] == BOAT_STATE:
        if hide_boats:
            return EMPTY_SYMBOL
        else:
            return str(cell["boat_size"])
    return EMPTY_SYMBOL


def generate_board() -> BoardType:
    board = [[create_empty_cell() for _ in range(COLUMNS)] for _ in range(ROWS)]
    boats = [4, 3, 3, 2, 2, 2, 1, 1, 1, 1]
    shuffle(boats)

    boat_id = 0
    for boat_size in boats:
        placed = False
        while not placed:
            row = randint(0, ROWS - 1)
            col = randint(0, COLUMNS - 1)
            orientation = randint(0, 1)

            if orientation == ORIENTATION_HORIZONTAL:
                # Verifica que el barco quepa en la fila
                if col + boat_size <= COLUMNS:
                    # Verifica que no haya colisiones
                    if all(board[row][c]["state"] == EMPTY_STATE for c in range(col, col + boat_size)):
                        for c in range(col, col + boat_size):
                            board[row][c] = create_boat_cell(boat_id, boat_size)
                        placed = True
                        boat_id += 1

            elif orientation == ORIENTATION_VERTICAL:
                # Verifica que el barco quepa en la columna
                if row + boat_size <= ROWS:
                    # Verifica que no haya colisiones
                    if all(board[r][col]["state"] == EMPTY_STATE for r in range(row, row + boat_size)):
                        for r in range(row, row + boat_size):
                            board[r][col] = create_boat_cell(boat_id, boat_size)
                        placed = True
                        boat_id += 1

    return board


def check_if_sunk(board: BoardType, row: int, col: int) -> bool:
    cell = board[row][col]
    
    if cell["boat_id"] is None:
        return False
    
    boat_id = cell["boat_id"]
    
    boat_cells = []
    for r in range(ROWS):
        for c in range(COLUMNS):
            if board[r][c]["boat_id"] == boat_id:
                boat_cells.append((r, c))
    
    all_hit = all(board[r][c]["state"] in [HIT_STATE, SUNK_STATE] for r, c in boat_cells)
    
    if all_hit:
        for r, c in boat_cells:
            board[r][c]["state"] = SUNK_STATE
        return True
    
    return False


def print_boards():
    col_headers = "   " + " ".join([str(i).ljust(2) for i in range(COLUMNS)])
    print("\nTU TABLERO".ljust(COLUMNS * 2 + 9) + "    |   " + "TABLERO DEL BOT")
    print(col_headers + "|   " + col_headers)
    print("-" * (COLUMNS * 6 + 7))

    for row_idx in range(ROWS):
        player_row = " ".join(get_cell_symbol(cell, hide_boats=False).ljust(2) for cell in player_board[row_idx])
        bot_row = " ".join(get_cell_symbol(cell, hide_boats=False).ljust(2) for cell in bot_board[row_idx])
        
        print(f"{ascii_uppercase[row_idx]:2} {player_row}|   {ascii_uppercase[row_idx]:2} {bot_row}")
    
    print("\nLeyenda: ~ = Agua, X = Tocado, # = Hundido, o = Fallo, 1-4 = Tus barcos")


def play_again() -> bool:
    while True:
        response = input("¿Quieres jugar de nuevo? (Y/y = Sí, N/n = No):\n> ").strip().lower()
        if response in ['y', 'n']:
            return response == 'y'
        print("Respuesta inválida.")


def play() -> None:
    global player_board, bot_board
    player_board = generate_board()
    bot_board = generate_board()

    while True:
        print_boards()

        # Turno del jugador
        while True:
            try:
                move = input("\nIngresa tu movimiento (ejemplo A5): ").strip().upper()
                if len(move) != 2:
                    raise ValueError("Movimiento inválido. Debe tener 2 caracteres.")
                
                row = ascii_uppercase.index(move[0])
                col = int(move[1:2])

                if row < 0 or row >= ROWS or col < 0 or col >= COLUMNS:
                    raise ValueError("Movimiento fuera de los límites del tablero.")

                cell_state = bot_board[row][col]["state"]
                if cell_state in [HIT_STATE, FAIL_STATE, SUNK_STATE]:
                    raise ValueError("Ya has atacado esa posición. Intenta de nuevo.")

                break
            except (ValueError, IndexError) as e:
                print(e)

        target_cell = bot_board[row][col]
        if target_cell["state"] == BOAT_STATE:
            print("¡TOCADO!")
            bot_board[row][col]["state"] = HIT_STATE
            
            if check_if_sunk(bot_board, row, col):
                print("¡HUNDIDO! Has destruido completamente un barco enemigo.")
        else:
            print("¡AGUA!")
            bot_board[row][col]["state"] = FAIL_STATE

        # Verificar si el jugador ha ganado
        if all(cell["state"] != BOAT_STATE for row in bot_board for cell in row):
            print_boards()
            print("¡Felicidades! Has hundido todos los barcos del bot.")
            if play_again():
                play()
            break

        # -------------------------------------------------------------------------------
        # Turno del bot
        while True:
            bot_row = randint(0, ROWS - 1)
            bot_col = randint(0, COLUMNS - 1)

            bot_cell_state = player_board[bot_row][bot_col]["state"]
            if bot_cell_state not in [HIT_STATE, FAIL_STATE, SUNK_STATE]:
                break

        print(f"\nEl bot ataca en {ascii_uppercase[bot_row]}{bot_col}")

        bot_target = player_board[bot_row][bot_col]
        if bot_target["state"] == BOAT_STATE:
            print("¡El bot ha TOCADO uno de tus barcos!")
            player_board[bot_row][bot_col]["state"] = HIT_STATE
            
            if check_if_sunk(player_board, bot_row, bot_col):
                print("¡El bot ha HUNDIDO completamente uno de tus barcos!")
        else:
            print("¡El bot ha fallado! (AGUA)")
            player_board[bot_row][bot_col]["state"] = FAIL_STATE
        
        # Verificar si el bot ha ganado
        if all(cell["state"] != BOAT_STATE for row in player_board for cell in row):
            print_boards()
            print("El bot ha hundido todos tus barcos. ¡Has perdido!")
            if play_again():
                play()
            break


if __name__ == "__main__":
    play()
