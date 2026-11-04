"""cuantiles-y-percentiles-1.py — que aguanta un percentil y que no.

Arriba: cuantos datos deja por debajo cada umbral de latencia (la escalera acumulada). El p90
es el corte que deja al 90 % por debajo y el p95 el que deja al 95 %: leerlos como porcentajes
y no como "95 ms" es lo que se aprende aqui.
Abajo: los percentiles 50, 75, 90, 95 y 99 de la misma serie, primero con las diez peticiones
limpias y después con la última en 1.000 ms. El p50 y el p75 no se mueven; por encima del p90
el corte lo decide el valor raro.
"""

import numpy as np

from comun import *

estilo()

limpia = np.array([10, 20, 30, 40, 50, 60, 70, 80, 90, 100], dtype=float)
sucia = limpia.copy()
sucia[-1] = 1000.0

etiquetas = ["p50", "p75", "p90", "p95", "p99"]
# Los percentiles pares (p50, p90) son valores observados con cualquiera de las dos
# convenciones; p75, p95 y p99 dependen del metodo. Aqui se usa el rango mas cercano
# (method="nearest"), que es el que solo devuelve valores presentes en los datos.
valores_limpios = np.percentile(limpia, [50, 75, 90, 95, 99], method="nearest")
valores_sucios = np.percentile(sucia, [50, 75, 90, 95, 99], method="nearest")

fig = plt.figure(figsize=(9.6, 6.6))
rejilla_paneles = fig.add_gridspec(2, 1, height_ratios=[1.0, 1.0])
arriba = fig.add_subplot(rejilla_paneles[0, 0])
abajo = fig.add_subplot(rejilla_paneles[1, 0])

# --- Arriba: la escalera acumulada ---------------------------------------------------------
bordes = [0.0] + list(limpia)
porcentaje = [0.0] + [100.0 * (i + 1) / limpia.size for i in range(limpia.size)]
arriba.step(bordes, porcentaje, where="post", color=AZUL, linewidth=1.8)
arriba.axhline(90, color=NARANJA, linewidth=1.3, linestyle="--")
arriba.axhline(95, color=MORADO, linewidth=1.3, linestyle=":")
arriba.axvline(90, color=NARANJA, linewidth=1.3, linestyle="--")
arriba.axvline(95, color=MORADO, linewidth=1.3, linestyle=":")
arriba.set_xlim(0, 108)
arriba.set_ylim(0, 108)
arriba.set_xticks([0, 20, 40, 60, 80, 100])
arriba.set_yticks([0, 25, 50, 75, 100])

anotar(arriba, "el salto del 90 % al 95 % solo a\u00f1ade una petici\u00f3n",
       xy=(95, 92.5), xytext=(0.30, 0.72), color=MORADO)
anotar(arriba, "aqu\u00ed el p90 es un corte real:\nqueda un 10 % a la derecha",
       xy=(90, 20), xytext=(0.05, 0.20), color=NARANJA)

titulo(arriba, "Un percentil es una posici\u00f3n, no una magnitud",
       "con 10 datos y sin interpolaci\u00f3n, el p90 es el 9.\u00ba valor y el p95 el 10.\u00ba")
arriba.set_xlabel("latencia (ms)")
arriba.set_ylabel("% de peticiones por debajo")
numeros(arriba)
rejilla(arriba)

# --- Abajo: que percentiles se mueven cuando un dato se dispara ---------------------------
posiciones = np.arange(len(etiquetas))
ancho = 0.36
abajo.bar(posiciones - ancho / 2, valores_limpios, width=ancho, color=AZUL,
          label="las diez peticiones limpias")
abajo.bar(posiciones + ancho / 2, valores_sucios, width=ancho, color=ROJO,
          label="la \u00faltima tarda 1.000 ms")
for i, (limpio, sucio) in enumerate(zip(valores_limpios, valores_sucios)):
    abajo.text(posiciones[i] - ancho / 2, limpio + 26, ("%g" % limpio).replace(".", ","),
               ha="center", color=AZUL, fontsize=8.5)
    abajo.text(posiciones[i] + ancho / 2, sucio + 26, ("%g" % sucio).replace(".", ","),
               ha="center", color=ROJO, fontsize=8.5)
abajo.set_xticks(posiciones)
abajo.set_xticklabels(etiquetas)
abajo.set_ylim(0, 1420)
abajo.set_yticks([0, 250, 500, 750, 1000])
abajo.legend(loc="upper right", fontsize=9)

anotar(abajo, "el valor raro decide el corte en cuanto\nla cola mira m\u00e1s all\u00e1 del 10 %",
       xy=(3.9, 1120), xytext=(0.24, 0.94), color=ROJO)

titulo(abajo, "La mediana aguanta; la cola alta no",
       "hasta el p75 los dos grupos dicen lo mismo: un valor raro de cada diez contamina lo que cae por encima del p90")
abajo.set_xlabel("percentil")
abajo.set_ylabel("latencia (ms)")
numeros(abajo, ejes="y")
rejilla(abajo)

guardar(fig, "percentiles-que-aguantan-y-que-no")
