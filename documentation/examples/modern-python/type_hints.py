from collections import namedtuple
from typing import Optional, Iterable

Elemento = namedtuple("Elemento", "voce, prezzo")
# named tuple = tuple con indici basati su nomi 

costo_massimo_normal = None
costo_massimo_hints: Optional[int] = None


def calcola_costo_normal(elementi):
    global costo_massimo
    total = 0

    for e in elementi:
        total += e.prezzo

    if not costo_massimo_normal or total > costo_massimo_normal:
        costo_massimo = total

    return total


def calcola_costo_hints(elementi: Iterable[Elemento]) -> int:
    global costo_massimo_hints
    total = 0

    for e in elementi:
        total += e.prezzo

    if not costo_massimo_hints or total > costo_massimo_hints:
        costo_massimo_hints = total

    return total


def main():
    print("Inseriamo i pasti consumati nel giorno")

    cena = [Elemento('Pizza', 20), Elemento('Birra', 9), Elemento('Birra', 9)]
    colazione = [Elemento('Pancakes', 11), Elemento('Bacon', 4), Elemento('Caffè', 3), Elemento('Caffè', 3), Elemento('Brioche', 2)]

    totale_cena_normal = calcola_costo_normal(cena)
    totale_cena_hints = calcola_costo_hints(cena)
    print(f"Costo cena EUR {totale_cena_hints:,.02f}")

    totale_colazione_normal = calcola_costo_normal(colazione)
    totale_colazione_hints = calcola_costo_hints(colazione)
    print(f"Costo colazione EUR {totale_colazione_hints:,.02f}")

    print(f"Oggi il costo più elevato è stato EUR {costo_massimo:.02f}")


if __name__ == '__main__':
    main()