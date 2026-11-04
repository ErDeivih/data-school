"""backtesting-vectorizado-1.py — cuatro lineas que parecen la misma estrategia y dan cuatro
capitales distintos: desplazar, pagar costes y componer. La figura de la pagina del
backtesting vectorizado (fase 9)."""

import numpy as np

from comun import *

estilo()
azar = np.random.default_rng(2)
n = 250
ret = azar.normal(0.0004, 0.012, n)          # retornos de una serie con algo de deriva
ret[0] = 0.0                                 # la primera barra no tiene periodo anterior
precio = 100 * np.cumprod(1 + ret)
media = np.convolve(precio, np.ones(20) / 20, mode="full")[: n]   # media movil de 20 barras
senal = (precio > media).astype(float)       # la regla: comprado si el cierre supera su media

posicion = np.concatenate([[0.0], senal[:-1]])   # el desplazamiento: la senal va una barra tarde
coste = 0.002 * np.abs(np.diff(posicion, prepend=0.0))

variantes = [
    ("sin desplazar la señal", float(np.cumprod(1 + senal * ret - coste)[-1]), ROJO),
    ("como se debe hacer", float(np.cumprod(1 + posicion * ret - coste)[-1]), AZUL),
    ("sin costes", float(np.cumprod(1 + posicion * ret)[-1]), NARANJA),
    ("sumando en vez de componer", float(1 + np.cumsum(posicion * ret - coste)[-1]), MORADO),
]
etiquetas = [v[0] for v in variantes]
valores = np.array([v[1] for v in variantes])

fig, ejes = plt.subplots(2, 1, figsize=(7.0, 5.6), sharex=False)

# --- Arriba: la señal y la posición que se mantiene de verdad ---
ejes[0].step(np.arange(n), senal, where="post", color=REJILLA, linewidth=1.4)
ejes[0].step(np.arange(n), posicion, where="post", color=AZUL, linewidth=1.7)
ejes[0].set_ylim(-0.25, 1.45)
ejes[0].set_xlim(0, n)
# El texto naranja que explicaba el retraso se solapaba con la etiqueta gris: lo dice el subtítulo.
titulo(ejes[0], "La señal de la barra t es la posición de t+1",
       "el mismo dato movido una barra: el array no distingue una de otra")
ejes[0].set_xlabel("barra")
ejes[0].set_ylabel("señal / posición")
# A 1,24 el renglón de la rejilla (1,25) le pasaba por encima: se sube al hueco que queda libre.
ejes[0].text(4, 1.31, "señal calculada con el cierre de hoy", color=REJILLA, fontsize=9)
ejes[0].text(4, -0.19, "posición que se mantiene", color=AZUL, fontsize=9)
# Las dos curvas coinciden en el valor; lo que cambia es en qué barra empieza cada tramo.
for barra in (86, 132):
    ejes[0].plot([barra, barra], [0.0, 1.0], color=NARANJA, linewidth=1.0, linestyle=":")
    ejes[0].annotate("", xy=(barra + 1, 1.05), xytext=(barra, 1.05),
                     arrowprops=dict(arrowstyle="->", color=NARANJA, linewidth=1.0))
rejilla(ejes[0])
numeros(ejes[0], "x")

# --- Abajo: lo que acaba en tu cuenta con cada variante ---
colores = [v[2] for v in variantes]
ejes[1].barh(etiquetas, valores, color=colores, height=0.6)
limite = float(valores[1])          # la version que se debe hacer
ejes[1].axvline(limite, color=TEXTO, linewidth=1.0, linestyle="--")
for i, valor in enumerate(valores):
    # La etiqueta de una barra mas corta que la raya de referencia se escribe a su derecha: si no,
    # la raya discontinua la atraviesa (le pasaba a la de 0,73).
    x_etiqueta = max(valor + 0.015, limite + 0.012)
    ejes[1].text(x_etiqueta, i, "%.2f" % valor, va="center", fontsize=9, color=colores[i])
ejes[1].axvline(1.0, color=REJILLA, linewidth=0.9)
ejes[1].text(1.33, 1.55, "un array no avisa de esto:\nlas tres hacen lo mismo\ncon una línea distinta",
             color=NARANJA, fontsize=8.5, va="center")
ejes[1].set_xlim(0.60, max(valores) + 0.16)
titulo(ejes[1], "El capital final: solo una línea está bien",
       "las otras tres hacen lo mismo con una línea de código distinta")
ejes[1].set_xlabel("capital final (empieza en 1)")
ejes[1].invert_yaxis()
ejes[1].text(limite + 0.012, 1.62, "la versión correcta", color=TEXTO, fontsize=8.5)
# Sin rejilla vertical: las barras ya llevan su cifra y las rayas de 0,8 tachaban las etiquetas.
numeros(ejes[1], "x")

guardar(fig, "backtesting-vectorizado-cuatro-curvas")
