"""pairs-trading-1.py — de dos precios que se mueven juntos a una regla operable: el
diferencial, su z-score y lo que cuesta el stop. Figura de la pagina de trading de pares
(fase 9).

Tres paneles, en el orden del argumento: (1) los dos precios en logaritmos comparten un
factor comun y por eso su diferencia tiene nivel estable; (2) el diferencial con la banda
de ±1,5 desviaciones, que es la que dispara la operación; (3) el resultado acumulado de
las 12 operaciones, con y sin stop, para ver lo que el stop cuesta y lo que evita."""

import numpy as np

from comun import *

estilo()
azar = np.random.default_rng(7)
n = 900

comun = np.cumsum(azar.normal(0, 0.01, n))               # paseo comun: el "mercado"
desv = np.zeros(n)
for t in range(1, n):
    desv[t] = 0.94 * desv[t - 1] + azar.normal(0, 0.008)  # diferencial que revierte
log_a = 4.0 + comun + 0.5 * desv
log_b = 3.5 + 0.8 * comun + azar.normal(0, 0.003, n)      # ruido propio de la segunda pata

# La primera mitad estima; la segunda se opera. Nunca al reves.
m = n // 2
beta = np.polyfit(log_b[:m], log_a[:m], 1)[0]             # ratio de cobertura
spread = log_a - beta * log_b
mu, sd = spread[:m].mean(), spread[:m].std(ddof=1)
z = (spread - mu) / sd

entrada, salida, stop = 1.5, 0.0, 2.5
coste_operacion = 0.0004                                  # dos patas a 2 pb cada una


def simula(tope):
    """Opera el diferencial desde m hasta n. `tope` es el stop en desviaciones.

    Devuelve la curva acumulada (una cifra por dia, para poder dibujarla), el resultado
    de cada operación y la peor excursión de cada una."""
    pos, bruto, bloqueado = 0, 0.0, False
    ops, peor, posicion, curva = [], [], np.zeros(n), np.zeros(n)
    for t in range(m, n - 1):
        zt = (spread[t] - mu) / sd
        if bloqueado and abs(zt) < 0.5:
            bloqueado = False                             # no se reentra hasta volver al centro
        if pos == 0 and not bloqueado:
            if zt > entrada:
                pos, ops, peor = -1, ops + [0.0], peor + [0.0]
            elif zt < -entrada:
                pos, ops, peor = 1, ops + [0.0], peor + [0.0]
        if pos != 0:
            cambio = pos * (spread[t + 1] - spread[t])
            ops[-1] += cambio
            peor[-1] = min(peor[-1], ops[-1])
            bruto += cambio
            posicion[t] = pos
            if (pos == 1 and (zt >= salida or zt <= -tope)) or \
               (pos == -1 and (zt <= salida or zt >= tope)):
                pos, bloqueado = 0, True
        curva[t + 1] = bruto
    return curva, ops, peor, posicion


curva_con, ops_con, peor_con, pos_con = simula(stop)
curva_sin, ops_sin, peor_sin, _ = simula(99.0)
bruto_con, bruto_sin = float(curva_con[-1]), float(curva_sin[-1])
neto_con = bruto_con - coste_operacion * len(ops_con)
neto_sin = bruto_sin - coste_operacion * len(ops_sin)

fig, ejes = plt.subplots(3, 1, figsize=(7.0, 7.4), sharex=True)

# ── 1. Dos precios, un factor comun: la diferencia es lo que tiene nivel ──────
eje = ejes[0]
eje.plot(log_a, color=AZUL, linewidth=1.2, label="ln(P_A): el activo que se quedó atrás")
eje.plot(log_b, color=NARANJA, linewidth=1.2, label="ln(P_B): su pareja")
eje.axvline(m, color=TEXTO, linewidth=0.9, linestyle=":" )
titulo(eje, "En logaritmos, la distancia entre los dos es comparable en el tiempo",
       "A la izquierda se estima; a la derecha se opera. Nunca con los mismos datos")
eje.set_ylabel("logaritmo\ndel precio")
eje.legend(loc="lower left", fontsize=8)
rejilla(eje)
eje.text(m + 12, 2.70, "→ fuera de muestra", fontsize=8.5, color=TEXTO)

# ── 2. El diferencial: la banda decide cuando hay operacion ───────────────────
eje = ejes[1]
eje.plot(spread, color=MORADO, linewidth=1.2)
eje.axhline(mu, color=TEXTO, linewidth=1.0, linestyle="--")
eje.axhline(mu + entrada * sd, color=ROJO, linewidth=1.0, linestyle=":")
eje.axhline(mu - entrada * sd, color=ROJO, linewidth=1.0, linestyle=":")
eje.axvspan(m, n, color=REJILLA, alpha=0.10, zorder=0)
# Se sombrea cada operacion segun su direccion: comprado el diferencial o vendido.
tramos, inicio = [], None
for t in range(m, n):
    if pos_con[t] != 0 and inicio is None:
        inicio = t
    elif pos_con[t] == 0 and inicio is not None:
        tramos.append((inicio, t, pos_con[inicio]))
        inicio = None
for ini, fin, sentido in tramos:
    eje.axvspan(ini, fin, color=VERDE if sentido == 1 else ROSA, alpha=0.16, zorder=0)
titulo(eje, "El z-score dispara la operación cuando sale de la banda de ±1,5",
       "Lo sombreado son las 12 operaciones: verde comprando el diferencial, rosa vendiéndolo")
eje.set_ylabel("diferencial\nln(P_A) − 1,271·ln(P_B)")
rejilla(eje)
eje.text(20, mu + entrada * sd + 0.0030,
         f"banda de entrada: {mu + entrada * sd:.3f} y {mu - entrada * sd:.3f}",
         fontsize=8.5, color=ROJO, zorder=4,
         bbox=dict(boxstyle="round,pad=0.15", facecolor="white", edgecolor="none"))
eje.text(0.62, 0.12, f"media estimada {mu:.3f}", transform=eje.transAxes,
         fontsize=8.5, color=TEXTO, zorder=4,
         bbox=dict(boxstyle="round,pad=0.15", facecolor="white", edgecolor="none"))

# ── 3. Lo que cuesta el stop y lo que evita ───────────────────────────────────
eje = ejes[2]
x = np.arange(n)
eje.plot(x, curva_sin, color=NARANJA, linewidth=1.6, linestyle="--",
         label=f"sin stop: bruto {bruto_sin:+.4f}, peor racha {min(peor_sin):+.4f}")
eje.plot(x, curva_con, color=AZUL, linewidth=1.8,
         label=f"con stop 2,5: bruto {bruto_con:+.4f}, peor racha {min(peor_con):+.4f}")
eje.axhline(0, color=TEXTO, linewidth=0.9, linestyle="--")
eje.axvline(m, color=TEXTO, linewidth=0.9, linestyle=":")
titulo(eje, "El stop cuesta resultado bruto y compra tamaño",
       "Menos excursión adversa permite dimensionar la posición más grande")
eje.set_xlabel("día")
eje.set_ylabel("resultado\nacumulado")
eje.set_xlim(0, n - 1)
rejilla(eje)
numeros(eje, "y")
eje.legend(loc="upper left", fontsize=8)
# El peor momento de cada curva: es la cifra con la que se dimensiona la posicion.
anotar(eje, f"peor racha sin stop {min(peor_sin):+.4f}",
       (float(np.argmin(curva_sin)), float(curva_sin.min())), (0.06, 0.42), color=NARANJA)
eje.text(0.30, 0.30, f"coste de las dos patas: {coste_operacion*len(ops_con):.4f} "
                     f"({len(ops_con)} operaciones)\n"
                     f"neto con stop {neto_con:+.4f} · neto sin stop {neto_sin:+.4f}",
         transform=eje.transAxes, fontsize=8.5, color=MORADO, va="top")

guardar(fig, "pairs-trading-diferencial-y-stop")
