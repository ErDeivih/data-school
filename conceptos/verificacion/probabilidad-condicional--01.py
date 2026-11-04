# Dado y moneda simulados sobre una rejilla determinista: 6 caras x 2 lados x 10 repeticiones.
caras = [1, 2, 3, 4, 5, 6] * 20                      # cada cara aparece 20 veces
lados = ["cara", "cruz"] * 60                        # 60 caras y 60 cruces
n = len(caras)
assert n == len(lados) == 120

seis = [c == 6 for c in caras]
pares = [c % 2 == 0 for c in caras]

p_seis = sum(seis) / n
p_par = sum(pares) / n
p_seis_y_par = sum(s and p for s, p in zip(seis, pares)) / n

print("P(seis)          ", round(p_seis, 4))                        # salida: 0.1667
print("P(par)           ", round(p_par, 4))                         # salida: 0.5
print("P(seis y par)    ", round(p_seis_y_par, 4))                  # salida: 0.1667
print("P(seis sabiendo par)", round(p_seis_y_par / p_par, 4))       # salida: 0.3333
