# Lo que el simulador no cobra, y como cambia el signo de la esperanza
p, ganancia, perdida = 0.55, 1.2, 1.0     # 55 % de aciertos, +1,2 % y -1,0 % de media

for coste in (0.0, 0.10, 0.25, 0.40):
    esperanza = p * ganancia - (1 - p) * perdida - coste
    print(f"coste {coste:.2f} % -> esperanza {esperanza:+.2f} % por operacion")
# -> coste 0.00 % -> esperanza +0.21 % por operacion
# -> coste 0.10 % -> esperanza +0.11 % por operacion
# -> coste 0.25 % -> esperanza -0.04 % por operacion
# -> coste 0.40 % -> esperanza -0.19 % por operacion
