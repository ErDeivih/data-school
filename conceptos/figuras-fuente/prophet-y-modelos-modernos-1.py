"""prophet-y-modelos-modernos-1.py — el regimen de Prophet: regresión sobre el calendario.

Prophet no mira los valores pasados: ajusta una tendencia y un patron de calendario. Cuando la
serie tiene deriva, el naive estacional —repetir el mismo mes del año pasado— falla justo por eso.
La figura de la pagina de Prophet y modelos modernos (fase 5)."""

import numpy as np

from comun import *

estilo()
azar = np.random.default_rng(7)

n_hist = 48
n_fut = 3
todos = np.arange(n_hist + n_fut)
# Facturacion mensual: tendencia de +0,8 al mes y un ciclo anual fuerte
serie = (100 + 0.8 * todos + 6 * np.sin(2 * np.pi * todos / 12)
         + 2 * np.cos(2 * np.pi * todos / 12) + azar.normal(0, 1.5, todos.size))
hist = serie[:n_hist]
t_hist = todos[:n_hist]
t_fut = todos[n_hist:]


def diseno(t, periodo=12, k=2):
    """Base de Fourier de orden k: la estacionalidad tal como la escribe Prophet."""
    columnas = [np.ones_like(t, dtype=float), t.astype(float)]
    for j in range(1, k + 1):
        columnas += [np.sin(2 * np.pi * j * t / periodo), np.cos(2 * np.pi * j * t / periodo)]
    return np.column_stack(columnas)


beta, *_ = np.linalg.lstsq(diseno(t_hist), hist, rcond=None)
modelo = diseno(t_fut) @ beta
naive = hist[n_hist - 12:n_hist - 12 + n_fut]      # el mismo mes del año anterior
real = serie[n_hist:]

rmse_modelo = float(np.sqrt(np.mean((real - modelo) ** 2)))
rmse_naive = float(np.sqrt(np.mean((real - naive) ** 2)))

# Los dos paneles NO comparten el eje x: arriba va una serie de 51 meses y abajo tres meses
# comparados de dos en dos. Con sharex, las tres parejas de barras se apilaban en el 6 % de la
# izquierda del eje (xlim 0..52) y las etiquetas de valor «11,3» y «11,6» se pisaban entre sí
# (medido: 10,6 px de solape en horizontal). Sin sharex cada panel usa todo el ancho.
fig, ejes = plt.subplots(2, 1, figsize=(9.4, 6.6))

# --- Panel 1: que pronostica cada metodo --------------------------------------
ejes[0].plot(t_hist, hist, color=AZUL, linewidth=1.5)
ejes[0].plot(t_fut, real, color=TEXTO, linewidth=1.5, linestyle=":", zorder=2)
ejes[0].plot(t_fut, modelo, color=VERDE, linewidth=2.2, marker="o", markersize=5,
             label="Prophet: tendencia + calendario")
ejes[0].plot(t_fut, naive, color=NARANJA, linewidth=2.2, marker="s", markersize=5,
             label="naive estacional: el mismo mes del año pasado")
ejes[0].axvline(t_hist[-1], color=REJILLA, linewidth=1.0)
titulo(ejes[0], "Los tres meses siguientes: dos pronósticos",
       "lo que promete cada método para los tres meses que vienen")
ejes[0].set_xlabel("mes")
ejes[0].set_ylabel("facturación")
ejes[0].legend(loc="upper left")
rejilla(ejes[0])
numeros(ejes[0])
# La nota de la frontera caía justo encima de la rejilla del 100 y la línea le pasaba por
# dentro (medido: 74 px, gris sobre gris). Baja al hueco entre las rejillas de 100 y 110, que
# está vacío: por ahí la curva azul va entre 104 y 110.
anotar(ejes[0], "aquí empieza el futuro", xy=(t_hist[-1], 101),
      xytext=(0.50, 0.15), color=REJILLA)
# El aviso del naive va en la franja entre las rejillas de 120 y 130 (caja de 121,9 a 128,1): en
# (0,22, 0,60) la rejilla de 130 le cruzaba la primera línea (128 px medidos) y en (0,22, 0,72)
# la flecha salía a la altura del 135 y se pegaba al lomo de la curva azul (que llega a 137,6)
# durante 60 px. Desde aquí la cruza una sola vez y de través.
anotar(ejes[0], "el naive repite un dato de hace un año:\n"
                "se deja fuera diez puntos de tendencia",
      xy=(t_fut[1], naive[1]), xytext=(0.22, 0.53), color=NARANJA)

# --- Panel 2: el error de cada uno --------------------------------------------
ancho = 0.35
pos = np.arange(n_fut)
error_modelo = np.abs(real - modelo)
error_naive = np.abs(real - naive)
ejes[1].bar(pos - ancho / 2, error_modelo, width=ancho, color=VERDE,
            label="error de Prophet, RMSE %.2f" % rmse_modelo)
ejes[1].bar(pos + ancho / 2, error_naive, width=ancho, color=NARANJA,
            label="error del naive, RMSE %.2f" % rmse_naive)
ejes[1].set_ylim(0, max(error_naive.max(), error_modelo.max()) * 1.35)
# Las rejillas van de 5 en 5 y no de 2 en 2: con el paso de 2, la rejilla del 12 partía por la
# mitad las etiquetas de valor de los dos últimos meses (medido: 15 px de línea dentro de
# «11.3» y otros 15 dentro de «11.6»). No hay rejilla por encima del 10 a propósito: la del 15
# caía dentro de la leyenda, que vive en el hueco de arriba a la derecha (medido: 101 px de
# línea dentro de «error de Prophet, RMSE 2.14»).
ejes[1].set_yticks([0, 5, 10])
for i in range(n_fut):
    ejes[1].text(pos[i] + ancho / 2, error_naive[i] + 0.25, "%.1f" % error_naive[i],
                 ha="center", fontsize=8.5, color=NARANJA)
ejes[1].set_xticks(pos)
ejes[1].set_xticklabels(["mes +1", "mes +2", "mes +3"])
titulo(ejes[1], "La diferencia no es de precisión",
       "es que el naive ignora la deriva de la serie")
ejes[1].set_ylabel("error absoluto")
ejes[1].legend(loc="upper right")
rejilla(ejes[1])
# El eje x de este panel es de tres categorías, no una escala numérica: se formatea solo el y.
# Con numeros(ejes[1]) a secas, el formateador de la coma sustituía las etiquetas «mes +1»,
# «mes +2» y «mes +3» por 0, 1 y 2 (es lo que salía dibujado antes).
numeros(ejes[1], "y")
# La nota pasa de dos líneas a una y se queda en la franja de arriba, por encima de la última
# rejilla (la del 10) y a la izquierda de la leyenda: en dos líneas y en (0,10, 0,94) la rejilla
# del 14 le cruzaba la primera (124 px medidos) y la segunda se salía por arriba del eje.
anotar(ejes[1], "el modelo de calendario es una regresión de seis columnas",
      xy=(pos[1], error_naive[1]), xytext=(0.03, 0.883), color=TEXTO, flecha=False)

guardar(fig, "prophet-calendario-frente-a-naive")
