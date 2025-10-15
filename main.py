from blackjack import play as play_blackjack
from hundirLaFlota import play as play_hundir_la_flota
from tresEnRalla import play as play_tres_en_ralla
from typing import Callable
from utils.console import clear_console


opts: dict[str, Callable] = {
    "0": lambda: play_blackjack(),
    "1": lambda: play_hundir_la_flota(),
    "2": lambda: play_tres_en_ralla()
}


while True:
    clear_console()
    
    response = input(
        "¿A qué quieres jugar?\n" + \
        "    0. Blackjack\n" + \
        "    1. Hundir la flota\n" + \
        "    2. Tres en raya\n" + \
        "> "
    )

    opt: Callable | None = opts.get(response)

    if opt is None:
        input("Opción inválida, presiona Enter para continuar...\n")
        continue

    opt()
