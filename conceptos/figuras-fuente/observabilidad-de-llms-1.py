"""observabilidad-de-llms-1.py — los cuatro paneles que se miran de un sistema con LLM en
producción: la cola de latencia, donde esta el dinero, por qué falla la validación y de que
esta hecha la factura. Los números son los de la pagina, calculados con semilla fija.
Figura de la pagina de observabilidad de LLMs (fase 8)."""

import numpy as np
import matplotlib.pyplot as plt

from comun import *

estilo()

rng = np.random.default_rng(7)
N = 500

# --- Los datos de la pagina ----------------------------------------------------
reintentos = rng.binomial(2, 0.30, size=N)
exito = rng.random(N) < np.where(reintentos == 0, 0.96, np.where(reintentos == 1, 0.90, 0.75))
latencia = rng.lognormal(mean=np.log(1100.0), sigma=0.35, size=N) + reintentos * 1900 \
           + np.where(exito, 0.0, 2500.0)

P_ENTRADA, P_CACHE, P_SALIDA = 3.00, 0.30, 15.00
TEXTO_ENTRADA = rng.integers(1_400, 2_200, size=N)
DOCUMENTOS = rng.integers(0, 8, size=N)
tokens_entrada = TEXTO_ENTRADA + DOCUMENTOS * 420 + reintentos * 3_600
coste = (tokens_entrada * P_ENTRADA + 1_200 * P_CACHE + 250 * P_SALIDA) / 1e6

fig = plt.figure(figsize=(8.8, 6.2))
rejilla_ = fig.add_gridspec(2, 2, hspace=0.48, wspace=0.30)

# --- A: la cola de latencia ----------------------------------------------------
ax = fig.add_subplot(rejilla_[0, 0])
p50, p95 = np.percentile(latencia, [50, 95])
ax.hist(latencia / 1000, bins=34, color=AZUL, alpha=0.85)
for valor, color, etiqueta, pos in ((p50, ROJO, "p50: 2,6 s", (0.03, 0.93)),
                                    (p95, MORADO, "p95: 5,3 s", (0.96, 0.93))):
    ax.axvline(valor / 1000, color=color, linewidth=1.6, linestyle="--")
    # Cada rotulo va a su esquina, con la flecha bajando hasta la linea: encima del histograma
    # se solapaban con las barras y entre ellos.
    ax.annotate(etiqueta, xy=(valor / 1000, ax.get_ylim()[1] * 0.55), xycoords="data",
                xytext=pos, textcoords="axes fraction", fontsize=8.5, color=color,
                ha="left" if pos[0] < 0.5 else "right", va="center",
                arrowprops=dict(arrowstyle="->", color=color, linewidth=0.9,
                                shrinkA=2, shrinkB=3))
ax.set_xlabel("segundos por consulta")
ax.set_ylabel("consultas")
titulo(ax, "El p95 dobla la mediana",
       "casi todas las trazas lentas reintentaron una vez")
rejilla(ax)
numeros(ax, "x")

# --- B: donde esta el dinero ---------------------------------------------------
ax = fig.add_subplot(rejilla_[0, 1])
orden = np.argsort(coste)
acumulado = np.cumsum(coste[orden]) / coste.sum()
fraccion = np.arange(1, N + 1) / N
punto_mitad = int(np.searchsorted(acumulado, 0.5)) + 1
ax.plot(fraccion, acumulado, color=VERDE, linewidth=1.8)
ax.plot([fraccion[punto_mitad - 1]], [acumulado[punto_mitad - 1]], marker="o", markersize=6,
        color=ROJO, zorder=4)
anotar(ax, "la mitad del gasto cabe en 321 de 500", xy=(fraccion[punto_mitad - 1],
      acumulado[punto_mitad - 1]), xytext=(0.06, 0.80), color=ROJO)
anotar(ax, "la cola del 5 % más caro: 9 %", xy=(0.975, acumulado[-1]),
       xytext=(0.97, 0.30), color=MORADO, align="right")
ax.set_xlabel("fracción de consultas, de más barata a más cara")
ax.set_ylabel("fracción del gasto acumulado")
ax.set_ylim(0, 1.02)
titulo(ax, "El gasto esta repartido, no en la cola",
       "recortar de la cola ahorra poco; la entrada es el 80 %")
rejilla(ax)
numeros(ax, "x")

# --- C: por que falla la validacion -------------------------------------------
ax = fig.add_subplot(rejilla_[1, 0])
causas = ["herramienta\nequivocada", "esquema\ninvalido", "documentos\nirrelevantes",
          "respuesta\nvacia"]
conteo = [112, 61, 44, 18]
barras = ax.bar(np.arange(len(causas)), conteo, color=[ROJO, NARANJA, AZUL, MORADO],
                width=0.66)
for barra, valor in zip(barras, conteo):
    ax.text(barra.get_x() + barra.get_width() / 2, valor + 3, str(valor), ha="center",
            va="bottom", fontsize=8.5, color=TEXTO)
ax.set_xticks(np.arange(len(causas)))
ax.set_xticklabels(causas, fontsize=8)
ax.set_ylabel("consultas del dia")
ax.set_ylim(0, 132)
titulo(ax, "La causa más comun es la herramienta",
       "dos entradas solapadas del catalogo bastan para elegir mal")
rejilla(ax)

# --- D: de que esta hecha la factura ------------------------------------------
ax = fig.add_subplot(rejilla_[1, 1])
partidas = [("entrada", (tokens_entrada * P_ENTRADA).sum() / 1e6, AZUL),
            ("salida", (250 * P_SALIDA * N) / 1e6, NARANJA),
            ("cache", (1_200 * P_CACHE * N) / 1e6, VERDE)]
total = sum(p[1] for p in partidas)
# Una barra por partida, no una barra apilada: con la cache en el 2 % su trozo era invisible
# y las etiquetas de los extremos se salian del eje.
for y, (nombre, euros, color) in enumerate(partidas):
    ax.barh(y, euros / total, color=color, height=0.55)
    ax.text(euros / total + 0.02, y, f"{euros / total:.1%}", va="center", ha="left",
            fontsize=8.5, color=color)
ax.set_yticks(range(len(partidas)))
ax.set_yticklabels([p[0] for p in partidas], fontsize=8.5)
ax.invert_yaxis()
ax.set_xlim(0, 1.05)
ax.set_xlabel("fracción del gasto diario")
titulo(ax, "La entrada se lleva el 80,2 %",
       "la cache parecia la palanca y aporta el 2 %")
rejilla(ax, "x")
numeros(ax, "x")

guardar(fig, "observabilidad-que-mirar-en-producción")
