# Games:
from blackjack import play as play_blackjack
from hundirLaFlota import play as play_hundir_la_flota
from tresEnRalla import play as play_tres_en_ralla
from piedraPapelTijera import play as play_piedra_papel_tijera
from ahorcado import play as play_ahorcado
from adivinaNumero import play as play_adivina_numero

# Utils:
from utils.console import clear_console

# Other:
from typing import Callable
from sys import exit


opts: dict[str, Callable] = {
    "0": lambda: play_blackjack(),
    "1": lambda: play_hundir_la_flota(),
    "2": lambda: play_tres_en_ralla(),
    "3": lambda: play_piedra_papel_tijera(),
    "4": lambda: play_ahorcado(),
    "5": lambda: play_adivina_numero(),
    "q": lambda: print("¡Gracias por jugar!") or exit(0),
}


while True:
    clear_console()
    
    response = input(
        "¿A qué quieres jugar?\n" + \
        "    0. Blackjack\n" + \
        "    1. Hundir la flota\n" + \
        "    2. Tres en raya\n" + \
        "    3. Piedra papel o tijera\n" + \
        "    4. Ahorcado\n" + \
        "    5. Adivina el número\n" + \
        "    q. Salir\n" + \
        "> "
    ).lower()

    opt: Callable | None = opts.get(response)

    if opt is None:
        input("Opción inválida, presiona Enter para continuar...\n")
        continue

    opt()
