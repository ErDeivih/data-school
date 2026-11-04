"""_tanteo.py — ayudante temporal para mirar números antes de fijar una figura."""

import numpy as np

rng = np.random.default_rng(7)
n = 900
comun = np.cumsum(rng.normal(0, 0.01, n))
desv = np.zeros(n)
for t in range(1, n):
    desv[t] = 0.94 * desv[t - 1] + rng.normal(0, 0.008)
log_a = 4.0 + comun + 0.5 * desv
log_b = 3.5 + 0.8 * comun + rng.normal(0, 0.003, n)

m = n // 2
beta = np.polyfit(log_b[:m], log_a[:m], 1)[0]
spread = log_a - beta * log_b
mu, sd = spread[:m].mean(), spread[:m].std(ddof=1)
z = (spread - mu) / sd
print("beta %.3f  mu %.4f  sd %.4f" % (beta, mu, sd))
print("z fuera de muestra min %+.2f max %+.2f" % (z[m:].min(), z[m:].max()))
print("dias |z|>1.5 en la segunda mitad: %d de %d"
      % (int(np.sum(np.abs(z[m:]) > 1.5)), n - m))


def simula(stop, espera=0.5, entrada=1.5, salida=0.0):
    pos, pnl, bloqueado = 0, 0.0, False
    ops, peor, posicion, marcas = [], [], np.zeros(n), []
    for t in range(m, n - 1):
        zt = (spread[t] - mu) / sd
        if bloqueado and abs(zt) < espera:
            bloqueado = False
        if pos == 0 and not bloqueado:
            if zt > entrada:
                pos, ops, peor = -1, ops + [0.0], peor + [0.0]
                marcas.append((t, -1))
            elif zt < -entrada:
                pos, ops, peor = 1, ops + [0.0], peor + [0.0]
                marcas.append((t, 1))
        if pos != 0:
            cambio = pos * (spread[t + 1] - spread[t])
            ops[-1] += cambio
            peor[-1] = min(peor[-1], ops[-1])
            pnl += cambio
            posicion[t] = pos
            if (pos == 1 and (zt >= salida or zt <= -stop)) or \
               (pos == -1 and (zt <= salida or zt >= stop)):
                pos, bloqueado = 0, True
    return pnl, ops, peor, posicion, marcas


coste = 0.0004
for etiqueta, stop in (("con stop 2,5", 2.5), ("sin stop", 99.0)):
    pnl, ops, peor, posicion, marcas = simula(stop)
    print("%-13s ops %3d  bruto %+7.4f  neto %+7.4f  peor racha %+.4f"
          % (etiqueta, len(ops), pnl, pnl - coste * len(ops), min(peor)))
