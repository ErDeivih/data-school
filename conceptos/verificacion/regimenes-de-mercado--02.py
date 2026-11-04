import numpy as np

rng = np.random.default_rng(5)
n = 3000
P = np.array([[0.95, 0.05], [0.10, 0.90]])       # la misma cadena de la pagina
estado = np.zeros(n, dtype=int)
for t in range(1, n):
    if rng.random() < P[estado[t - 1], 1 - estado[t - 1]]:
        estado[t] = 1 - estado[t - 1]
    else:
        estado[t] = estado[t - 1]

media = np.where(estado == 0, 0.0005, -0.0008)
vol = np.where(estado == 0, 0.008, 0.020)
r = rng.normal(media, vol)

# Volatilidad movil de 20 dias: en t solo se usan datos hasta t (nada de futuro)
v = np.zeros(n)
for t in range(19, n):
    v[t] = r[t - 19:t + 1].std(ddof=1)
alerta = v > 0.012

print("dias en tension %.0f%%" % (100 * (estado == 1).mean()))
print("acierto del filtro      %.3f" % (alerta == (estado == 1)).mean())
print("acierto de decir calma  %.3f" % (estado == 0).mean())
print("precision en tension    %.3f" % ((alerta & (estado == 1)).sum() / alerta.sum()))

retardos = []
for t in range(1, n):
    if estado[t] == 1 and estado[t - 1] == 0 and alerta[t:].any():
        retardos.append(int(np.argmax(alerta[t:])))
print("episodios %d  retardo mediano %.0f dias" % (len(retardos), np.median(retardos)))

# Donde esta el golpe: retorno medio de los primeros cuatro dias frente al resto
primeros, resto = [], []
for t in range(1, n):
    if estado[t] == 1 and estado[t - 1] == 0:
        primeros.append(r[t:t + 4].mean())
        fin = t
        while fin < n and estado[fin] == 1:
            fin += 1
        if fin - t > 4:
            resto.append(r[t + 4:fin].mean())
print("retorno medio primeros 4 dias %+.5f" % np.mean(primeros))
print("retorno medio del resto       %+.5f" % np.mean(resto))
# -> dias en tension 30%
# -> acierto del filtro      0.681
# -> acierto de decir calma  0.705
# -> precision en tension    0.473
# -> episodios 108  retardo mediano 2 dias
# -> retorno medio primeros 4 dias -0.00043
# -> retorno medio del resto       -0.00054
