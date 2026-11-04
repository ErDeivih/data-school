# La esperanza y el coste de una racha, todo en unidades de R.
p, gana, pierde = 0.45, 2.0, 1.0
esperanza = p * gana - (1 - p) * pierde
print("esperanza por operacion:", round(esperanza, 2), "R")     # -> esperanza por operacion: 0.35 R
print("en 200 operaciones:", round(200 * esperanza, 1), "R")    # -> en 200 operaciones: 70.0 R
print("diez perdidas seguidas:", 10 * pierde, "R")              # -> diez perdidas seguidas: 10.0 R
doblada = 3 * pierde + sum(pierde * 2 ** i for i in range(1, 8))   # duplicar tras la tercera
print("la misma racha doblando el tamano:", doblada, "R")       # -> la misma racha doblando el tamano: 257.0 R
