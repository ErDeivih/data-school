"""git-avanzado-1.py — por qué git bisect es una busqueda binaria: cada sonda parte el
intervalo por la mitad, así que 64 commits se resuelven en 6 comprobaciones en vez de 42. La
figura de la pagina de Git avanzado (fase 11)."""

import numpy as np

from comun import *

estilo()

n_commits, primer_malo = 64, 41
izquierda, derecha = 0, n_commits - 1


def esta_malo(commit):
    return commit >= primer_malo


# Se reproduce la misma busqueda del codigo, guardando tambien donde cae cada sonda.
internos, anchos, puntos = [izquierda], [derecha - izquierda], []
while derecha - izquierda > 1:
    medio = (izquierda + derecha) // 2
    puntos.append(medio)
    if esta_malo(medio):
        derecha = medio
    else:
        izquierda = medio
    internos.append(izquierda)
    anchos.append(derecha - izquierda)
n_sondas = len(puntos)

# Dos filas en vez de dos columnas: con los rotulos de cada barra ("intervalo 63", "sonda 47
# -> malo") la columna se queda estrecha y el texto se sale del eje.
fig, (arriba, abajo) = plt.subplots(2, 1, figsize=(8.4, 8.2))

# --- Arriba: como se encoge el intervalo en cada sonda ------------------------------
pasos = np.arange(len(anchos))
etiquetas = [f"intervalo {a}" for a in anchos[:-1]] + ["1 commit: el culpable"]
colores = [MORADO] + [AZUL if esta_malo(p) else VERDE for p in puntos]
barras = arriba.barh(pasos, anchos, color=colores, height=0.6)
# La etiqueta dice cual fue la sonda y que respondio: sin eso, la barra no explica nada.
rotulos = [f"{anchos[0]} commits candidatos"] + [f"sonda {p} -> {'malo' if esta_malo(p) else 'bueno'}"
                                                for p in puntos]
arriba.bar_label(barras, labels=rotulos, padding=3, fontsize=8)
arriba.set_yticks(pasos, etiquetas)
arriba.invert_yaxis()
arriba.set_xlim(0, max(anchos) * 1.55)
titulo(arriba, "Cada sonda parte el intervalo por la mitad",
       "64 commits se quedan en uno solo en seis pasos")
arriba.set_xlabel("commits que siguen siendo candidatos")
rejilla(arriba, eje="x")
numeros(arriba)

# --- Abajo: lo que cuesta cada estrategia ------------------------------------------
etiquetas_abajo = ["todos los\ncommits", "bisección\n6 sondas", "busqueda lineal\n42 sondas"]
valores = [n_commits, n_sondas, primer_malo + 1]
colores_abajo = [CIAN, VERDE, ROJO]
barras_abajo = abajo.bar(etiquetas_abajo, valores, color=colores_abajo, width=0.55)
abajo.bar_label(barras_abajo, padding=3, fontsize=9)
abajo.set_ylim(0, n_commits * 1.25)
titulo(abajo, "Comprobaciones necesarias para hallar el commit 41")
abajo.set_ylabel("comprobaciones de la suite")
rejilla(abajo)
# Solo el eje y: el eje x lleva nombres de texto, no numeros.
numeros(abajo, ejes="y")

guardar(fig, "git-avanzado-bisect")
