from random import randint
from time import sleep


deck: list[str] = ["2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K", "A"] * 4

card_values: dict[str, int] = {
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
    "K": 10,
    "A": 11,
}

player_points = 0
bot_points = 0


def get_random_card() -> float:
    """
    Retrieves a card from the deck poping the item out of the list and returns the value associated with the card
    """
    idx: int = randint(0, len(deck) - 1)
    card: str = deck[idx]
    _ = deck.pop(idx)
    points: float = card_values[card]

    print(f"Carta: {card}, {points=}")

    return points


def get_player_card() -> None:
    global player_points
    player_points += get_random_card()

    if player_points > 7.5:
        print(f"Has perdido, has sacado {player_points}, que supera los 7.5 puntos")
    elif player_points == 7.5:
        print("¡Has ganado! Tienes 7.5 puntos")
    else:
        res = input(
            f"Tienes {player_points} puntos, ¿deseas obtener otra carta? (Y/y -> Sí, Default -> No)"
        )

        if res.lower() == "y":
            get_player_card()
        else:
            get_bot_card()


def get_bot_card() -> None:
    global bot_points
    bot_points += get_random_card()

    if bot_points < 5.5:
        print(f"El bot tiene {bot_points} puntos, decide pillar otra carta más")
        get_bot_card()
    elif bot_points > 7.5:
        print(
            f"Has ganado, el bot ha sacado {bot_points} puntos, que supera los 7.5 puntos"
        )
    elif bot_points == 7.5:
        print("Has perdido, el bot ha sacado 7.5 puntos")
    elif is_retrieving_another_card():
        print(f"El bot tiene {bot_points} puntos, decide pillar otra carta más")
        get_bot_card()
    else:
        get_winner()


def is_retrieving_another_card() -> bool:
    return randint(0, 1) == 1


def get_winner() -> None:
    print("\n\nDefiniendo ganador", end="")

    sleep(1)
    print(".", end="")
    sleep(1)
    print(".", end="")
    sleep(1)
    print(".", end="\n\n\n")
    sleep(1)

    if player_points > bot_points:
        print("Has ganado, tienes más puntos que el bot sin superar el 7.5!")
    elif player_points == bot_points:
        print("EMPATE - No hay ganador")
    else:
        print("Has perdido... No has llegado al 7.5 y el bot tiene más puntos")

    print(f"{player_points=}   -   {bot_points=}")


def play() -> None:
    get_player_card()


if __name__ == "__main__":
    play()
