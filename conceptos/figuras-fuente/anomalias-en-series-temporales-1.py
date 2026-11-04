"""anomalias-en-series-temporales-1.py — por qué el z-score global no ve nada en una serie
con deriva y estacionalidad, y qué se gana mirando el residuo de la diferencia estacional.
La figura de la página de anomalías en series temporales (fase 5)."""

import numpy as np

from comun import *

estilo()
azar = np.random.default_rng(9)
n = 300
t = np.arange(n)

# Deriva suave, ciclo semanal y ruido; encima, ocho anomalías inyectadas.
y = 120 + 0.45 * t + 9.0 * np.sin(2 * np.pi * t / 7) + azar.normal(0.0, 2.6, n)
pos = np.array([41, 42, 43, 118, 171, 229, 230, 275])
y[pos] += np.array([22.0, 25.0, 21.0, -23.0, 19.0, -26.0, -21.0, 24.0])
es_anomalia = np.zeros(n, dtype=bool)
es_anomalia[pos] = True

# Regla 1: z-score global, con la media y la desviación de toda la serie.
z_global = np.abs((y - y.mean()) / y.std())


def mediana_y_escala(v, w):
    """Mediana y MAD de la ventana centrada, dejando fuera el punto que se evalúa."""
    m = len(v)
    med = np.empty(m)
    esc = np.empty(m)
    for i in range(m):
        a = max(0, i - w // 2)
        b = min(m, i + w // 2 + 1)
        vecinos = np.delete(v[a:b], i - a)
        med[i] = np.median(vecinos)
        esc[i] = np.median(np.abs(vecinos - med[i]))
    return med, esc


# Regla 2: diferencia estacional (mismo día de la semana anterior) y z-score robusto.
d7 = np.zeros(n)
d7[7:] = y[7:] - y[:-7]
med7, esc7 = mediana_y_escala(d7, 29)
z7 = np.abs(d7 - np.median(d7)) / (1.4826 * esc7 + 1e-9)
detectado = z7 > 4.0

fig, ejes = plt.subplots(1, 2, figsize=(7.4, 3.9))

# --- Panel izquierdo: el z-score global, ciego --------------------------------
ax = ejes[0]
ax.plot(t, y, color=REJILLA, linewidth=1.2)
ax.axhline(y.mean(), color=MORADO, linewidth=1.2, linestyle="--")
ax.axhline(y.mean() + 4 * y.std(), color=ROJO, linewidth=1.0, linestyle=":")
ax.scatter(t[es_anomalia], y[es_anomalia], color=ROJO, s=26, zorder=4)
anotar(ax, "la banda del z-score global\nnunca se cruza", (150, y.mean() + 4 * y.std()),
       (0.30, 0.70), color=ROJO)
anotar(ax, "la media de toda la serie", (20, y.mean()), (0.03, 0.90), color=MORADO)
ax.set_xlabel("día")
ax.set_ylabel("valor")
titulo(ax, "El z-score global no marca ninguna", "deriva y ciclo inflan la desviación a 39,5")
rejilla(ax)
numeros(ax)

# --- Panel derecho: el residuo de la diferencia estacional --------------------
ax = ejes[1]
ax.plot(t, d7, color=REJILLA, linewidth=1.1)
limite = 4.0 * 1.4826 * np.median(esc7[7:])
ax.axhspan(-limite, limite, color=AZUL, alpha=0.07)
ax.axhline(limite, color=AZUL, linewidth=1.0, linestyle="--")
ax.axhline(-limite, color=AZUL, linewidth=1.0, linestyle="--")
ax.scatter(t[detectado & es_anomalia], d7[detectado & es_anomalia], color=ROJO, s=26, zorder=4)
ax.scatter(t[detectado & ~es_anomalia], d7[detectado & ~es_anomalia], color=NARANJA, s=26,
           marker="s", zorder=4)
anotar(ax, "la anomalía sale dos veces:\nal entrar y al salir de la ventana",
       (48, d7[48]), (0.34, 0.18), color=NARANJA)
ax.set_xlabel("día")
ax.set_ylabel("diferencia respecto al día 7 anterior")
titulo(ax, "El residuo sí las separa del ciclo", "seguimiento perfecto, con ecos a siete días")
rejilla(ax)
numeros(ax)

guardar(fig, "anomalias-deriva-z-global-frente-a-diferencia-estacional")
