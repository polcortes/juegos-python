from typing import Literal, Callable
from random import randint, shuffle
from time import sleep


card_values: dict[str, int] = {
    "A": 11,
    "2": 2,
    "3": 3,
    "4": 4,
    "5": 5,
    "6": 6,
    "7": 7,
    "8": 8,
    "9": 9,
    "10": 10,
    "J": 10,
    "Q": 10,
    "K": 10
}

deck: list[str] = []

playing: bool = True
INITIAL_MONEY = 1000
MIN_BET = 10
MAX_BET = 500

current_bet: int = 0
player_score: int = 0
bot_score: int = 0
player_money: int = 0


def parse_card(card: str, who: Literal["player", "bot"] = "player") -> int:
    """
    Parse a card. Cards from 2 to 10 returns their number as value. "J", "Q" and "K" will always return 10. "A" will return 11 while the score plus 11 do not overflow 21, otherwise will return 1.
    """
    card_val, _ = card.split("_")

    if card_val == "A":
        if who == "player":
            return 11 if (player_score + 11) < 21 else 1
        else:
            return 11 if (bot_score + 11) < 21 else 1
    else:
        return card_values[card_val]

def generate_deck():
    global deck
    deck.clear()
    values = ["A", "2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K"]
    suits = ['♠', '♥', '♦', '♣']

    for suit in suits:
        for value in values:
            deck.append(f"{value}_{suit}")

    shuffle(deck)

def set_bet():
    """
    Set player's bet restricted by MIN_BET and MAX_BET
    """
    global current_bet
    response = input(f"Tienes {player_money}€. ¿Cuánto quieres apostar? (min: {MIN_BET}€, máx: {MAX_BET}€)\n> ")

    try:
        bet = int(response)

        if bet < MIN_BET:
            print(f"La apuesta mínima es de {MIN_BET}€.")
            set_bet()
        elif bet > MAX_BET:
            print(f"La apuesta máxima es de {MAX_BET}€.")
            set_bet()
        elif bet > player_money:
            print(f"No puedes apostar más de lo que tienes.")
            set_bet()
        else:
            current_bet = bet

    except ValueError:
        print("Por favor, introduzca una cantidad válida")
        set_bet()

def get_card() -> str:
    """
    Get a random card from the deck, pop it out of the deck and return it
    """
    return deck.pop(randint(0, len(deck) - 1))

def print_card(card: str, returns: bool = False):
    values = card.split("_")
    if returns:
        return f"{values[0]} de {values[1]}"
    print(f"{values[0]} de {values[1]}")

def get_first_player_cards():
    global player_score
    card1 = get_card()
    card2 = get_card()

    print("\nHas sacado:")
    print_card(card1)
    print_card(card2)

    player_score += parse_card(card1) + parse_card(card2)

def before_round():
    global player_score, bot_score
    player_score = 0
    bot_score = 0
    generate_deck()

def get_player_card():
    global player_score, player_money
    card = get_card()

    print(f"Has sacado un {print_card(card, returns=True)}")
    player_score += parse_card(card, who='player')
    print(f"Tienes {player_score} puntos")

def double_bet():
    global current_bet

    if current_bet * 2 <= player_money:
        current_bet *= 2
    else:
        print(f"No puedes doblar tu apuesta, no te llega el dinero (apuesta actual: {current_bet}, dinero actual: {player_money})")

def check_blackjacks_and_overflows():
    global playing, player_money

    old_money = player_money
    if player_score == 21:
        print("¡Has ganado, has sacado un blackjack!")
        player_money += int(current_bet * 1.5)
        print(f"Dinero:\n{old_money}€ => {player_money}€")
        return True
    elif player_score > 21:
        print(f"Has perdido, te has pasado de 21 puntos (tienes {player_score} puntos)")
        player_money -= current_bet
        print(f"Dinero:\n{old_money}€ => {player_money}€")
        return True
    elif bot_score == 21:
        print("Has perdido, el bot ha sacado un blackjack.")
        player_money -= current_bet
        print(f"Dinero:\n{old_money}€ => {player_money}€")
        return True
    elif bot_score > 21:
        print(f"¡Has ganado! El bot se ha pasado de 21 puntos ({bot_score} puntos)")
        player_money += current_bet
        print(f"Dinero:\n{old_money}€ => {player_money}€")
        return True
    else:
        return False

def continue_playing() -> bool:
    if player_money == 0:
        print("No tienes dinero, no puedes continuar jugando.")
        return False

    response = input("¿Deseas jugar otra ronda? (Y/y = Sí, N/n = No)\n> ")

    match response.lower():
        case "y": return True
        case "n": return False
        case _: return print("Respuesta inválida") or continue_playing()

def play():
    global player_score, player_money, current_bet, bot_score
    rondas = 1
    player_money = INITIAL_MONEY

    while playing:
        print(f"\n\n\n---  RONDA {rondas}  -----------------------------------------")

        before_round()
        set_bet()

        first_bot_card = get_card()
        print(f"\nEl bot ha sacado un {print_card(first_bot_card, returns=True)}")
        bot_score += parse_card(first_bot_card)
        print(f"Tiene {bot_score} puntos")

        if bot_score == 21:
            print("¡El bot ha sacado un blackjack, has perdido la ronda!")
            player_money -= current_bet
            if continue_playing():
                rondas += 1
                continue
            else:
                print("Adiós 👋")
                break

        else:
            get_first_player_cards()

            if player_score == 21:
                print("¡Has sacado un blackjack, has ganado la ronda!")
                player_money += int(current_bet * 1.5)
                if continue_playing():
                    rondas += 1
                    continue
                else:
                    print("Adiós 👋")
                    break
            
            player_is_gambling = True

            while player_is_gambling:
                option = input(
                    f"\nTienes {player_score} puntos y {player_money}€, estás apostando {current_bet}€\n" + \
                    "¿Qué quieres hacer?\n" + \
                    "   1 - Pedir\n" + \
                    "   2 - Plantarse\n" + \
                    "   3 - Doblar\n" + \
                    "\n> "
                )

                match option:
                    case "1": get_player_card()
                    case "2": player_is_gambling = False
                    case "3": double_bet()
                    case _: print(f"Opción inválida ({option})")

                if player_score == 21:
                    player_is_gambling = False
                elif player_score > 21:
                    player_is_gambling = False

        if check_blackjacks_and_overflows():
            if continue_playing():
                rondas += 1
                continue
            else:
                print("Adiós 👋")
                break

        while True:
            card = get_card()
            bot_score += parse_card(card)
            print(f"El bot ha sacado un {print_card(card, returns=True)}. Total puntos: {bot_score}.")
            sleep(.5)
            if bot_score == 21:
                break
            elif randint(0, 1) == 1 and bot_score < 21:
                print("El bot ha decidido tirar otra carta")
                sleep(.5)
            else:
                print("El bot ha decidido plantarse")
                break

        if check_blackjacks_and_overflows():
            if continue_playing():
                rondas += 1
                continue
            else:
                print("Adiós 👋")
                break

        if player_score > bot_score:
            print("¡Has ganado, tienes más puntos que el bot!")
            if continue_playing():
                rondas += 1
                continue
            else:
                print("Adiós 👋")
                break
        elif player_score < bot_score:
            print("Has perdido, tienes menos puntos que el bot...")
            if continue_playing():
                rondas += 1
                continue
            else:
                print("Adiós 👋")
                break
        else:
            print("EMPATE. No has perdido dinero.")
            if continue_playing():
                rondas += 1
                continue
            else:
                print("Adiós 👋")
                break


if __name__ == "__main__":
    play()


"""
[Inicio del juego]
        ↓
[Mostrar saldo del jugador]
        ↓
[Solicitar apuesta (verificar mínimo/máximo)]
        ↓
[Repartir 2 cartas al jugador y al dealer]
        ↓
[Verificar si hay Blackjack en jugador o dealer]
        ↓
[Si no hay Blackjack:]
    → Mostrar opciones: Pedir / Plantarse / Doblar / Dividir / Rendirse (si aplica)
        ↓
[Jugador toma decisiones hasta plantarse o pasarse]
        ↓
[Dealer juega su turno (automático)]
        ↓
[Evaluar ganador de la ronda]
        ↓
[Ajustar saldo del jugador según el resultado]
        ↓
[Preguntar si desea jugar otra ronda]
        ↓
[Si sí → repetir flujo | Si no → terminar]



Pagos

Resultado  |  Pago
Ganar mano normal  |  1:1
Blackjack  |  3:2
Seguro ganado  |  2:1 sobre el seguro
Push (empate)  |  Se devuelve la apuesta
Perder  |  Pierde apuesta


Doblar

El jugador puede doblar si quiere, solo recibe una carta más y se planta automáticamente.

Se debe verificar si tiene suficiente saldo para cubrir la apuesta duplicada.


Dividir

Se permite dividir solo si las dos cartas iniciales son del mismo valor.

Se requiere una apuesta adicional igual a la original.

Cada mano se juega por separado.

Si se dividen ases, normalmente solo se reparte una carta por mano.


Seguro

Si el dealer muestra un As, se ofrece la opción de apostar el 50% de la apuesta como seguro.

Si el dealer tiene Blackjack, el jugador gana 2:1 sobre el seguro, pero pierde la apuesta original (salvo que también tenga Blackjack → Push).


Rendirse

Si está habilitado, el jugador puede rendirse y recuperar la mitad de la apuesta inicial antes de pedir carta.


PAGOS:
Ganar = saldo += apuesta
Ganar con Blackjack = saldo += int(apuesta * 1.5)
Seguro ganado = saldo += (apuesta / 2) * 2
Empate = saldo += 0
Perder = saldo -= apuesta
"""