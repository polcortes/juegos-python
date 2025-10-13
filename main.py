from blackjack import play as play_blackjack
from hundirLaFlota import play as play_hundir_la_flota
from typing import Callable
import os


def clear_console():
    os.system('cls' if os.name=='nt' else 'clear')


opts: dict[str, Callable] = {
    "0": lambda: play_blackjack(),
    "1": lambda: play_hundir_la_flota()
}


while True:
    clear_console()
    
    response = input(
        "¿A qué quieres jugar?\n" + \
        "    0. Blackjack\n" + \
        "    1. Hundir la flota\n" + \
        "> "
    )

    opt: Callable | None = opts.get(response)

    if opt is None:
        print("Opción inválida...\n")
        continue

    opt()
