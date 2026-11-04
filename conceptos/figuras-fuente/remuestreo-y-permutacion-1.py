"""remuestreo-y-permutacion-1.py — de donde sale el p-valor de un test de permutación.

Izquierda: la distribución nula, construida barajando las etiquetas 5.000 veces. La cola roja
es lo que cuenta para el p-valor. Derecha: con 3 contra 3 solo existen 20 repartos, así que
los p-valores posibles son multiplos de 0,05 y el más pequeño es 0,10.
La figura de la pagina de tests de permutación (fase 2)."""

import numpy as np

from comun import *

estilo()
azar = np.random.default_rng(7)
n = 25
grupo_a = azar.normal(0.70, 1.0, n)
grupo_b = azar.normal(0.00, 1.0, n)
todos = np.concatenate([grupo_a, grupo_b])
etiquetas = np.array([1] * n + [0] * n)
observado = float(grupo_a.mean() - grupo_b.mean())

B = 5000
nulas = np.empty(B)
for i in range(B):
    azar.shuffle(etiquetas)
    nulas[i] = todos[etiquetas == 1].mean() - todos[etiquetas == 0].mean()
extremos = int(np.sum(np.abs(nulas) >= abs(observado)))
p_valor = (extremos + 1) / (B + 1)
altura, _ = np.histogram(nulas, bins=48)

fig, ejes = plt.subplots(1, 2, figsize=(10.4, 4.4))

# --- Panel 1: la distribucion nula por Monte Carlo ------------------------------------
limite = abs(observado)
ejes[0].hist(nulas, bins=48, color=AZUL, alpha=0.55, zorder=2)
ejes[0].axvspan(nulas.min() - 0.3, -limite, color=ROJO, alpha=0.16, zorder=1)
ejes[0].axvspan(limite, nulas.max() + 0.3, color=ROJO, alpha=0.16, zorder=1)
ejes[0].axvline(observado, color=ROJO, linewidth=1.8, zorder=3)
ejes[0].axvline(0, color=TEXTO, linewidth=0.9, zorder=3)
ejes[0].set_ylim(0, float(altura.max()) * 1.22)
anotar(ejes[0], "lo observado", xy=(observado, float(altura.max()) * 0.55),
       xytext=(0.88, 0.34), color=ROJO)
anotar(ejes[0], ("p = %.3f" % p_valor).replace(".", ",") + ": solo el "
       + ("%.1f %%" % (100.0 * p_valor)).replace(".", ",") + " de los barajados\n"
       "llegan tan lejos como el observado",
       xy=(limite * 1.45, float(altura.max()) * 0.05), xytext=(0.34, 0.93), color=TEXTO)
titulo(ejes[0], "La nula se construye barajando las etiquetas",
       "si el grupo no importara, cualquier reparto daría una diferencia parecida")
ejes[0].set_xlabel("diferencia de medias entre los dos grupos barajados")
ejes[0].set_ylabel("veces (de 5.000)")
numeros(ejes[0])
rejilla(ejes[0])

# --- Panel 2: con pocos datos hay muy pocos repartos posibles -------------------------
valores = np.array([12.0, 14.0, 16.0, 20.0, 22.0, 24.0])
sumas = []
for i in range(6):
    for j in range(i + 1, 6):
        for k in range(j + 1, 6):
            sumas.append(valores[i] + valores[j] + valores[k])
sumas = np.array(sumas)
diferencias = (2.0 * sumas - valores.sum()) / 3.0
unicos, cuantos = np.unique(np.round(diferencias, 6), return_counts=True)
colores = [ROJO if abs(u) >= 8.0 - 1e-9 else AZUL for u in unicos]
ejes[1].bar(unicos, cuantos, width=0.34, color=colores, zorder=2)
ejes[1].axvline(-8.0, color=ROJO, linewidth=1.2, linestyle="--", zorder=1)
ejes[1].set_ylim(0, 4.0)
ejes[1].text(0.02, 0.95, "solo 2 repartos de 20 llegan tan lejos",
             transform=ejes[1].transAxes, va="center", color=ROJO, fontsize=9)
ejes[1].text(0.98, 0.85, "el p más pequeño posible: 0,10",
             transform=ejes[1].transAxes, ha="right", va="center", color=TEXTO, fontsize=9)
anotar(ejes[1], "el reparto observado", xy=(-8.0, 1.0), xytext=(0.02, 0.78), color=ROJO)
titulo(ejes[1], "Con 3 contra 3 solo hay 20 repartos",
       "la separación es perfecta y el p-valor no puede bajar de 0,10: falta resolución")
ejes[1].set_xlabel("diferencia de medias de cada reparto posible")
ejes[1].set_ylabel("cuántos repartos dan ese valor")
numeros(ejes[1])
rejilla(ejes[1])

guardar(fig, "permutacion-nula-y-granularidad")
