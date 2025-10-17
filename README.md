# Exercicis d'Anivellació Python
Repositori que conté els jocs demanats al mòdul de Python pel curs d'especialització de Big Data i Intel·ligència Artificial.

## Com jugar
A l'arrel del projecte es troba el fitxer `main.py`, aquest és l'arxiu a executar utilitzant el terminal.
```ps1
python .\main.py
```

## Estructura del projecte
El projecte s'organitza utilitzant mòduls de Python. Cada joc és dins d'un mòdul.

L'arxiu `main.py` del projecte s'encarrega d'importar cada joc de cada mòdul per agrupar-los i enllistar-los.

Així, l'estructura del projecte seria semblant a:
```
juegos-python
└──── blackjack
│     └──── __init__.py
│     └──── main.py
└──── hundirLaFlota
│     └──── __init__.py
│     └──── main.py
└──── La resta de jocs...
└──── utils
│     └──── __init__.py
│     └──── console.py
└─ main.py
```
