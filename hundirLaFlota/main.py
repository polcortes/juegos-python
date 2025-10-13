from random import shuffle, randint, choice
from typing import Literal, Union
from string import ascii_uppercase


ROWS    = 10
COLUMNS = 10

EMPTY_CELL:      Literal["~"] = "~" 
HIT_CELL:        Literal["X"] = "X"
FAIL_CELL:       Literal["o"] = "o"
BOAT_CELL:       Literal["1"] = "1"     # 1
CRUISE_CELL:     Literal["2"] = "2"     # 2
SUBMARINE_CELL:  Literal["3"] = "3"     # 3
BOUQUET_CELL:    Literal["4"] = "4"     # 4

type CellType = Union[
    type(EMPTY_CELL), type(HIT_CELL), type(FAIL_CELL), type(BOAT_CELL), 
    type(CRUISE_CELL), type(SUBMARINE_CELL), type(BOUQUET_CELL)
]

type BoardType = list[list[CellType]]

player_board: BoardType = []
bot_board: BoardType    = []

ORIENTATION_HORIZONTAL = 0
ORIENTATION_VERTICAL   = 1

class Parser():
    @staticmethod
    def parse_boat(boat: CellType) -> int:
        global BOAT_CELL, CRUISE_CELL, SUBMARINE_CELL, BOUQUET_CELL

        match boat:
            case "1": return 1
            case "2": return 2
            case "3": return 3
            case "4": return 4
            case _:    return 0


    @staticmethod
    def parse_number(number: int) -> CellType:
        global BOAT_CELL, CRUISE_CELL, SUBMARINE_CELL, BOUQUET_CELL

        match number:
            case 1: return BOAT_CELL
            case 2: return CRUISE_CELL
            case 3: return SUBMARINE_CELL
            case 4: return BOUQUET_CELL
            case _: return EMPTY_CELL


def generate_board():
    board = [[EMPTY_CELL for _ in range(COLUMNS)] for _ in range(ROWS)]
    boats = [4, 3, 3, 2, 2, 2, 1, 1, 1, 1]
    shuffle(boats)

    for boat in boats:
        placed = False
        while not placed:
            row = randint(0, ROWS - 1)
            col = randint(0, COLUMNS - 1)
            orientation = randint(0, 1)

            if orientation == ORIENTATION_HORIZONTAL:
                # Verifica que el barco quepa en la fila
                if col + boat <= COLUMNS:
                    # Verifica que no haya colisiones
                    if all(board[row][c] == EMPTY_CELL for c in range(col, col + boat)):
                        for c in range(col, col + boat):
                            board[row][c] = Parser.parse_number(boat)
                        placed = True

            elif orientation == ORIENTATION_VERTICAL:
                # Verifica que el barco quepa en la columna
                if row + boat <= ROWS:
                    # Verifica que no haya colisiones
                    if all(board[r][col] == EMPTY_CELL for r in range(row, row + boat)):
                        for r in range(row, row + boat):
                            board[r][col] = Parser.parse_number(boat)
                        placed = True

    
    return board


def print_board(board: BoardType, who: str="player"):
    print(f"Tablero de {who}")

    for row in board:
        print(" ".join(row))


def print_boards():
    col_headers = "   " + " ".join([str(i).ljust(2) for i in range(COLUMNS)])
    print("   TU TABLERO".ljust(COLUMNS * 2 + 9) + "   |   " + "TABLERO DEL BOT")
    print(col_headers + "|   " + col_headers)
    print("-" * (COLUMNS * 6 + 7))

    for row_idx in range(ROWS):
        player_row = " ".join(cell.ljust(2) for cell in player_board[row_idx])
        bot_row = " ".join(EMPTY_CELL if cell.ljust(2) in [BOAT_CELL, CRUISE_CELL, SUBMARINE_CELL, BOUQUET_CELL] else cell.ljust(2) for cell in bot_board[row_idx])
        
        print(f"{ascii_uppercase[row_idx]:2} {player_row}|   {ascii_uppercase[row_idx]:2} {bot_row}")



def play() -> None:
    global player_board, bot_board
    player_board = generate_board()
    bot_board = generate_board()

    print_boards()


if __name__ == "__main__":
    play()
