"""validacion-cruzada-1.py - lo que cambia entre KFold, estratificado y por grupos: el
reparto de clases dentro del pliegue y la fuga de entidades. Figura de la pagina de
validación cruzada (fase 6)."""

import numpy as np
from sklearn.model_selection import GroupKFold, KFold, StratifiedKFold

from comun import *

estilo()

# 300 filas de 30 clientes con 10 filas cada una; solo el 15 % son positivos
azar = np.random.default_rng(2)
n = 300
y = (azar.random(n) < 0.15).astype(int)
grupos = np.repeat(np.arange(30), 10)
X = azar.normal(size=(n, 4)) + y[:, None] * 0.8
sin_forma = np.zeros((n, 1))                   # KFold y StratifiedKFold solo miran el tamano

repartos = {
    "KFold": list(KFold(5, shuffle=True, random_state=0).split(sin_forma)),
    "Estratificado": list(StratifiedKFold(5, shuffle=True, random_state=0).split(sin_forma, y)),
    "Por grupos": list(GroupKFold(5).split(sin_forma, y, groups=grupos)),
}
estrategias = [("KFold", ROJO), ("Estratificado", AZUL), ("Por grupos", VERDE)]
positivos = {nombre: [100 * y[te].mean() for _, te in pliegues]
             for nombre, pliegues in repartos.items()}

# Fuga: por cada pliegue, clientes con alguna fila dentro del entrenamiento y alguna fuera.
# Sumando los 5 pliegues sale el numero de la pagina (140 con KFold, 0 por grupos).
def clientes_partidos(pliegues):
    total = 0
    for tr, te in pliegues:
        for g in range(30):
            if (grupos[tr] == g).any() and (grupos[te] == g).any():
                total += 1
    return total

fuga = {nombre: clientes_partidos(pliegues) for nombre, pliegues in repartos.items()}

fig, ejes = plt.subplots(1, 2, figsize=(10.6, 4.4))

# --- Izquierda: cuantos positivos caen en cada pliegue de prueba.
ancho = 0.26
posiciones = np.arange(5)
for k, (nombre, color) in enumerate(estrategias):
    ejes[0].bar(posiciones + (k - 1) * ancho, positivos[nombre], width=ancho, color=color,
                label=nombre)
ejes[0].axhline(15, color=TEXTO, linewidth=1.2, linestyle="--")
# La nota va justo encima de la linea, que es el techo de la zona vacia: cualquier altura
# por debajo cae sobre las barras del primer grupo.
anotar(ejes[0], "la tasa real es el 15 %: el reparto\nequilibrado deja los cinco pliegues ahi",
       xy=(2, 15), xytext=(0.03, 0.88), color=AZUL)
titulo(ejes[0], "Positivos que caen en cada pliegue",
       "barajando filas a lo bruto, un pliegue se queda con el 8,3 % y otro con el 21,7 %")
ejes[0].set_xlabel("pliegue de prueba")
ejes[0].set_ylabel("positivos en el pliegue (%)")
ejes[0].set_xticks(posiciones, ["1", "2", "3", "4", "5"])
ejes[0].set_ylim(0, 27)
rejilla(ejes[0], eje="y")
numeros(ejes[0], ejes="y")

# --- Derecha: la fuga que no se ve en la metrica, pero infla el resultado.
nombres = ["KFold\n(filas barajadas)", "Por grupos\n(por cliente)"]
valores = [fuga["KFold"], fuga["Por grupos"]]
ejes[1].bar(nombres, valores, color=[ROJO, VERDE], width=0.5)
for k, valor in enumerate(valores):
    ejes[1].text(k, valor + 5, str(valor), ha="center", fontsize=10, color=TEXTO)
# La nota va centrada en el hueco que queda por encima de la barra pequena: a la derecha
# se salia del panel y por la izquierda la tapaba la barra alta.
anotar(ejes[1], "cada fila de un cliente cae en un\npliegue distinto: la misma entidad\nqueda a los dos lados",
       xy=(0, fuga["KFold"]), xytext=(0.44, 0.72), color=ROJO)
titulo(ejes[1], "El cliente que aparece en los dos lados",
       "clientes con filas en entrenamiento y en prueba, sumando los 5 pliegues")
ejes[1].set_ylabel("clientes partidos entre los dos lados")
ejes[1].set_ylim(0, 185)
rejilla(ejes[1], eje="y")
numeros(ejes[1], ejes="y")

# Leyenda comun, debajo de los dos paneles: dentro del panel izquierdo tapaba las barras.
ejes[0].legend(loc="upper center", bbox_to_anchor=(1.05, -0.16), ncol=3)

guardar(fig, "validacion-cruzada-reparto-y-fuga")
