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

def simula(stop, espera=0.5, entrada=1.5, salida=0.0):
    """Tras cerrar no se vuelve a entrar hasta que el z vuelve a la zona de espera."""
    pos, pnl, bloqueado = 0, 0.0, False
    ops, peor = [], []
    for t in range(m, n - 1):
        z = (spread[t] - mu) / sd
        if bloqueado and abs(z) < espera:
            bloqueado = False
        if pos == 0 and not bloqueado:
            if z > entrada:
                pos, ops, peor = -1, ops + [0.0], peor + [0.0]
            elif z < -entrada:
                pos, ops, peor = 1, ops + [0.0], peor + [0.0]
        if pos != 0:
            cambio = pos * (spread[t + 1] - spread[t])
            ops[-1] += cambio
            peor[-1] = min(peor[-1], ops[-1])
            pnl += cambio
            if (pos == 1 and (z >= salida or z <= -stop)) or (pos == -1 and (z <= salida or z >= stop)):
                pos, bloqueado = 0, True
    return pnl, ops, peor

coste = 0.0004          # dos patas, 2 pb por pata y operacion
for etiqueta, stop in (("con stop 2,5", 2.5), ("sin stop", 99.0)):
    pnl, ops, peor = simula(stop)
    print("%-12s operaciones %3d  bruto %+7.4f  neto %+7.4f  peor racha %+.4f"
          % (etiqueta, len(ops), pnl, pnl - coste * len(ops), min(peor)))
# -> con stop 2,5 operaciones  12  bruto +0.2128  neto +0.2080  peor racha -0.0122
# -> sin stop     operaciones  12  bruto +0.2395  neto +0.2347  peor racha -0.0229
