# Cuantas veces basta mirar los datos para "encontrar" un efecto que no existe.
for k in (1, 5, 20, 100):
    al_menos_uno = 1 - (1 - 0.05) ** k
    # umbral de Bonferroni: reparte el 5 % entre todas las pruebas hechas
    print(f"{k:>3} pruebas  P(algun falso positivo) = {al_menos_uno:.4f}"
          f"  umbral Bonferroni = {0.05 / k:.4f}")
