"""ingenieria-de-features-1.py — que ventana es una variable legitima y que gana un
cociente que ninguna columna tiene. La figura de la pagina de ingenieria de variables."""

import numpy as np

from comun import *

estilo()
azar = np.random.default_rng(7)

# --- Izquierda: la misma ventana de 3 dias, con y sin desplazar ------------------
ventas = np.array([100, 120, 90, 140, 160, 130, 110], dtype=float)

sin_shift = np.full(ventas.size, np.nan)   # rolling(3).mean(): incluye el dia actual
con_shift = np.full(ventas.size, np.nan)   # shift(1).rolling(3).mean(): solo el pasado
for t in range(2, ventas.size):
    sin_shift[t] = ventas[t - 2:t + 1].mean()
    if t >= 3:
        con_shift[t] = ventas[t - 3:t].mean()

# --- Derecha: el cociente que separa dos clases solapadas -------------------------
visitas = np.array([10, 20, 30, 40, 12, 24, 36, 48], dtype=float)
# La tasa es lo que separa: 0,2 en la clase 0 y 0,5 en la clase 1, con temblor pequeno.
tasa0 = 0.20 + 0.02 * azar.standard_normal(4)
tasa1 = 0.50 + 0.02 * azar.standard_normal(4)

fig, ejes = plt.subplots(1, 2, figsize=(11.0, 4.3))

# Panel izquierdo
eje = ejes[0]
eje.plot(np.arange(1, 8), ventas, color=AZUL, marker="o", linewidth=1.6,
         label="ventas del dia")
eje.plot(np.arange(1, 8), sin_shift, color=ROJO, linewidth=1.6,
         label="rolling(3): incluye hoy")
eje.plot(np.arange(1, 8), con_shift, color=VERDE, linewidth=1.6,
         label="shift(1) + rolling(3)")
eje.scatter([5], [sin_shift[4]], color=ROJO, s=70, marker="^", zorder=5)
eje.scatter([5], [con_shift[4]], color=VERDE, s=70, marker="v", zorder=5)
eje.set_title("La ventana que incluye hoy ya sabe la respuesta")
eje.set_xlabel("dia")
eje.set_ylabel("ventas")
eje.set_ylim(84, 174)
eje.legend(loc="upper left", fontsize=8)
eje.annotate("prediciendo el dia 5: 130,0, porque la\nventana contiene el propio 160",
             xy=(4.85, sin_shift[4] + 2), xycoords="data",
             xytext=(0.98, 0.95), textcoords="axes fraction",
             fontsize=8.5, color=ROJO, va="top", ha="right",
             arrowprops=dict(arrowstyle="-", color=ROJO, linewidth=0.6, alpha=0.5))
anotar(eje, "116,7: solo 120, 90 y 140", (5, con_shift[4]), (0.34, 0.07), VERDE)
rejilla(eje)
numeros(eje)

# Panel derecho
eje = ejes[1]
eje.scatter(visitas[:4], tasa0, color=AZUL, s=55, label="no compra (clase 0)")
eje.scatter(visitas[4:], tasa1, color=NARANJA, s=55, marker="s", label="compra (clase 1)")
eje.axhline(tasa0.mean(), color=AZUL, linewidth=1.1, linestyle="--")
eje.axhline(tasa1.mean(), color=NARANJA, linewidth=1.1, linestyle="--")
eje.text(12.5, tasa0.mean() + 0.015, "tasa media 0,20", color=AZUL, fontsize=8.5, va="bottom")
eje.text(12.5, tasa1.mean() + 0.015, "tasa media 0,50", color=NARANJA, fontsize=8.5, va="bottom")
eje.set_ylim(0, 0.66)
eje.set_title("El cociente separa las clases; las visitas no")
eje.set_xlabel("visitas de la sesion")
eje.set_ylabel("compras / visitas")
eje.legend(loc="lower right", fontsize=8, bbox_to_anchor=(1.0, 0.16))
anotar(eje, "0,50 con 12 visitas y 0,20 con 40: la columna cruda se solapa",
       (visitas[4], tasa1[0]), (0.05, 0.92), TEXTO)
rejilla(eje)
numeros(eje)

guardar(fig, "ingenieria-de-features-ventana-y-cociente")
