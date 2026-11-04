import numpy as np

# Tres axiomas, tres comprobaciones con un dado simulado de forma determinista.
caras = np.arange(1, 7)
p = np.full(6, 1 / 6)

print("axioma 1, todas >= 0 :", bool(np.all(p >= 0)))                 # salida: True
print("axioma 2, suma = 1   :", round(float(p.sum()), 12))            # salida: 1.0

par = caras % 2 == 0                 # {2, 4, 6}
multiplo_de_3 = caras % 3 == 0       # {3, 6}
p_par = float(p[par].sum())
p_mult3 = float(p[multiplo_de_3].sum())
p_ambos = float(p[par & multiplo_de_3].sum())

print("P(par)               :", round(p_par, 4))                      # salida: 0.5
print("P(multiplo de 3)     :", round(p_mult3, 4))                    # salida: 0.3333
print("P(par y multiplo 3)  :", round(p_ambos, 4))                    # salida: 0.1667
print("P(par o multiplo 3)  :", round(p_par + p_mult3 - p_ambos, 4))   # salida: 0.6667
print("complementario       :", round(1 - p_par, 4))                  # salida: 0.5
