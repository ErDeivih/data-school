# Dos examenes con dificultad distinta: el z-score los pone en la misma escala
facil = (6.5, 1.2)      # media y desviacion tipica del examen facil
dificil = (5.0, 0.8)    # y las del examen dificil

print("facil   8.9 -> z", round((8.9 - facil[0]) / facil[1], 4))       # -> 2.0
print("facil   4.1 -> z", round((4.1 - facil[0]) / facil[1], 4))       # -> -2.0
print("dificil 7.5 -> z", round((7.5 - dificil[0]) / dificil[1], 4))   # -> 3.125
print("dificil 8.9 -> z", round((8.9 - dificil[0]) / dificil[1], 4))   # -> 4.875
